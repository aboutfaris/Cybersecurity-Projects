# Secure Cloud Configuration

Lock down the Cloud SOC lab and measure the result. You work through Microsoft Defender for Cloud recommendations, put Azure Key Vault and the storage account behind Private Link with public access disabled, attach an NSG to the subnet to satisfy NIST 800-53 SC-7 (Boundary Protection), and then compare 24 hours of attack data before and after.

Private Link gives a PaaS service a private IP inside your own virtual network, so traffic to it never crosses the public internet.

## What you'll use

- Microsoft Azure: Microsoft Defender for Cloud (secure score, recommendations, regulatory compliance), Private Link and private endpoints, private DNS zones, Network Security Groups, Network Watcher, Cost Management
- Azure Key Vault and an Azure Storage account
- Microsoft Sentinel workbooks backed by the Log Analytics workspace `law-cyber-lab-05`
- VMs: `windows-vm` (Windows 10 Pro 21H2) and `linux-vm` (Ubuntu Server 20.04) on `Lab-VNet`

## Prerequisites

- The Cloud SOC lab from the earlier projects: `RG-Cyber-Lab` with `Lab-VNet`, both VMs, the Key Vault, the storage account, Sentinel with the GeoIP watchlists, and the four attack-map workbooks.
- The previous lab's basic NSG lockdown already in place (secure score 54%).

## Steps

### Part 1: Check the baseline after the NSG lockdown

1. Open each Sentinel workbook with Time Range set to Last 24 hours.
   Expected result: Linux SSH Auth Failure, MySQL Authentication Failures, and Windows RDP & SMB Authentication Failure all return "The query returned no results." The nsg-malicious-allowed-in map is still busy, with malicious inbound flows from North America, Europe, and East Asia (top sources included London, China, and several US cities).
2. Note the 24-hour counts for the five tables. After the basic NSG lockdown they were:

   | Metric | Count (change) |
   | --- | --- |
   | SecurityEvent | 2401 (-93.85%) |
   | Syslog | 730 (-6.65%) |
   | SecurityAlert | 0 (-100.00%) |
   | SecurityIncident | 185 (-16.67%) |
   | AzureNetworkAnalytics_CL | 68 (-94.96%) |

   Malicious inbound NSG flows are still the main problem, which the rest of this lab addresses.

### Part 2: Work through Defender for Cloud recommendations

Check your subscription's Cost analysis before and after this part. Some remediations, such as DDoS Protection, are expensive.

3. Open Microsoft Defender for Cloud > Overview.
   Expected result: secure score 54%, 40 active recommendations, and regulatory compliance of 48 of 62 Microsoft cloud security benchmark controls, Azure CIS 1.4.0 91/109, NIST SP 800-53 R5 301/333, and R4 391/424.
4. Open Recommendations. Sort by Potential score increase. The largest gains are Secure management ports (+14%), Remediate vulnerabilities (+11%), Enable encryption at rest (+7%), and Restrict unauthorized network access (+7%).
5. Open a recommendation and follow its Remediation steps. Azure links you to the right blade for each one. For example, Azure DDoS Protection Standard should be enabled:
   1. Select a virtual network (`Lab-VNet` or `Lab-VNet-Attacker`).
   2. Under DDoS protection, select Enable. If "No DDoS protection plan was found" appears, click Create a DDoS protection plan first.
   3. Click Save.
6. Repeat for the other recommendations you want to address. Score updates can take a while to appear.

A later project asks whether a 100% secure score is really the best security measure. Here the goal is the network-boundary work in Part 3.

### Part 3: Private Link and firewall for Key Vault and Storage (NIST SC-7)

Defender for Cloud > Regulatory compliance lets you inspect each NIST 800-53 control. This part implements SC-7 Boundary Protection. Use the same region (East US 2) and virtual network (`Lab-VNet`) as the VMs.

7. Open your Key Vault (`<your-key-vault>`) > Networking > Firewalls and virtual networks. Select Disable public access, check Allow trusted Microsoft services to bypass this firewall, and save the change.
   The trusted services list only covers services where Microsoft controls all of the code. Services that run customer code, such as Azure DevOps, are not on it. That does not make them insecure; it just means they are not given a blanket bypass.
8. Switch to Private endpoint connections > + Private endpoint. On Basics, set Resource group `RG-Cyber-Lab`, Name `PE-AKV`, Network Interface Name `PE-AKV-nic`, and Region East US 2.
9. On Resource, choose Connect to an Azure resource in my directory, Resource type `Microsoft.KeyVault/vaults`, your Key Vault, and Target sub-resource `vault`.
10. On Virtual Network, choose `Lab-VNet (RG-Cyber-Lab)`, subnet `default`, and Dynamically allocate IP address.
11. On DNS, set Integrate with private DNS zone to Yes in `RG-Cyber-Lab`. Click Review + create, then Create.
    Expected result: validation passes and the summary shows private DNS zone `privatelink.vaultcore.azure.net`.
12. Open your storage account (`<your-storage-account>`) > Networking. Disable public access and create a private endpoint the same way: Name `EP-SA`, Network Interface Name `EP-SA-nic`, East US 2, `Lab-VNet`/`default`, private DNS integration Yes, Target sub-resource `blob`.
13. In the storage account, go to Settings > Configuration, set Allow Blob public access to Disabled, and click Save.
14. Open Network Watcher > Topology for `RG-Cyber-Lab`.
    Expected result: under `Lab-VNet` > `default`, the topology shows `EP-SA-nic` and `PE-AKV-nic` next to the `linux-vm` and `windows-vm` network interfaces. The private DNS zone now maps each service name to a private IP in the subnet.

### Part 4: Verify the private endpoints

15. RDP into `windows-vm`, open PowerShell, and look up the Key Vault. Use the host name only; `nslookup` fails with "Non-existent domain" if you include `https://`.

    ```powershell
    nslookup <your-key-vault>.vault.azure.net
    ```

    Expected result: the answer is `<your-key-vault>.privatelink.vaultcore.azure.net` with a private address in the subnet (10.0.0.5 in my lab). A private IP inside your own subnet range is what proves the endpoint works.
16. Run the same lookup on your own computer, outside Azure.
    Expected result: it resolves to a public Azure IP (the alias still mentions `privatelink.vaultcore.azure.net`), but you cannot reach the vault, because your computer is not on `Lab-VNet` and public access is disabled.
17. In the storage account, open Endpoints and copy the Blob service URL, `https://<your-storage-account>.blob.core.windows.net/`.
18. On your own computer, look up the blob host name:

    ```powershell
    nslookup <your-storage-account>.blob.core.windows.net
    ```

    Expected result: a public IP with the alias `<your-storage-account>.privatelink.blob.core.windows.net`, and no access because public blob access is off.
19. Run the same lookup inside `windows-vm`.
    Expected result: `<your-storage-account>.privatelink.blob.core.windows.net` at a private address in the subnet (10.0.0.7 in my lab).

If the VM lookup returns a public IP instead:

- DNS may still be propagating. Wait a few minutes and try again.
- The private endpoint and the VM may be in different virtual networks, or the private DNS zone is not linked to `Lab-VNet`.
- You can delete the private endpoint and its DNS configuration and recreate it. This is optional; the rest of the lab still works because public access is already disabled.

### Part 5: Attach an NSG to the subnet

20. Create a network security group named `NSG-Subnet` in `RG-Cyber-Lab`, East US 2.
21. Go to Virtual networks > `Lab-VNet` > Subnets > `default`, set Network security group to `NSG-Subnet`, and click Save.
    Expected result: Network Watcher topology now shows `NSG-SUBNET` attached to the `default` subnet.
22. Return to Defender for Cloud > Overview.
    Expected result: the secure score rises from 54% to 75% (24 assessed resources, 37 active recommendations, Microsoft cloud security benchmark 50 of 62 controls, NIST SP 800-53 R5 305/333).
23. Open Regulatory compliance > NIST SP 800-53 > SC-7 Boundary Protection. Most of SC-7 is now satisfied. Some assessments, such as "Subnets should be associated with a network security group", can still show as failed for a while because compliance data refreshes on a delay.

### Part 6: Run the secured environment for 24 hours

24. Leave the environment running for 24 hours, then open each workbook with Last 24 hours.
    Expected result: Linux SSH Auth Failure, MySQL Authentication Failures, nsg-malicious-allowed-in, and Windows RDP & SMB Authentication Failure all return "The query returned no results."
25. Record the 24-hour counts and compare them with the 24 hours before hardening:

    | Metric | Before securing | After securing | Change |
    | --- | --- | --- | --- |
    | Security Events (Windows VMs) | 39046 | 676 | -98.27% |
    | Syslog (Linux VMs) | 782 | 0 | -100.00% |
    | SecurityAlert (Defender for Cloud) | 1 | 0 | -100.00% |
    | SecurityIncident (Sentinel incidents) | 222 | 0 | -100.00% |
    | NSG inbound malicious flows allowed | 1350 | 0 | -100.00% |

26. Check Defender for Cloud > Overview one last time.
    Expected result: the secure score is 77% with 34 active recommendations and 52 of 62 Microsoft cloud security benchmark controls passing.

## What I learned

- Private endpoints plus private DNS make a PaaS service resolve to a private IP inside the VNet, while outside clients still resolve a public name they can no longer use.
- Disabling public access on Key Vault and Storage, and putting an NSG on the subnet, satisfied most of NIST 800-53 SC-7 and lifted the secure score from 54% to 75%.
- After hardening, 24 hours of data showed malicious inbound flows, Syslog failures, alerts, and incidents all dropping to zero, and Windows security events dropping by 98%.
- Secure score and compliance views lag behind changes, so verify with real tests like `nslookup` instead of waiting on the dashboard.

## Next steps / cleanup

- Check Cost Management > Cost analysis. In my run the subscription reached about $136 for April 2023, and Azure DDoS Protection was the largest single line (about $63), ahead of Storage and Virtual Machines. Disable DDoS Protection and remove its plan when you finish.
- Delete `RG-Cyber-Lab` and `RG-Cyber-Lab-Attacker` when you no longer need the lab.
- For a recap of the whole series, see [Summary of Cloud SOC Project: final results](../01-cloud-soc-project-summary/#final-results-and-metrics).

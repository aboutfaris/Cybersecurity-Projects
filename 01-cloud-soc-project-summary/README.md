# Summary of Cloud SOC Project

Build a small cloud SOC and honeynet in Azure: deliberately exposed VMs, Azure AD, SQL, and Key Vault send their logs to a Log Analytics workspace, and Microsoft Sentinel turns those logs into attack maps, alerts, and incidents. You measure attacks for 24 hours, harden the environment, then measure the same 24-hour window again.

This section is the series overview and the final results. It also holds the shared files the labs use (attack scripts, Sentinel workbook maps, analytics rules, and KQL queries).

In the finished design, attackers on the internet reach Azure AD, a SQL database, and two VMs behind NSGs. Those resources, plus Blob Storage, Key Vault, and the Activity Log, all send logs to one Log Analytics workspace. Sentinel reads that workspace and turns it into maps, incidents, and alerts.

## What you'll use

- An Azure subscription (the free trial credit covers the labs if you clean up afterwards; watch Cost Analysis, since several labs run resources for 24 hours or more)
- Azure Virtual Network (VNet) and Network Security Groups (NSGs)
- Virtual machines: 2 Windows, 1 Linux
- Azure SQL, Azure Key Vault, and an Azure Storage account
- Log Analytics workspace, Microsoft Sentinel, and Microsoft Defender for Cloud
- KQL with GeoIP watchlists for the attack maps
- The workbook, analytics rule, KQL, and PowerShell files in this folder

## Part 1: Follow the labs in order

Each lab builds on the previous one.

1. Set up the prerequisites: VMs, network, SQL, failed authentication, Active Directory, and the attack VM. Follow [Cloud SOC Pre-requisites](../02-cloud-soc-prerequisites/).
2. Turn on logging and monitoring so tenant, subscription, and resource logs reach the workspace, and load the GeoIP watchlists. Follow [Logging and Monitoring](../03-logging-and-monitoring/).
3. Build the Sentinel attack-map workbooks and analytics rules, generate attack traffic, and work the incidents. Follow [Microsoft Sentinel SIEM](../04-microsoft-sentinel-siem/).
4. Harden the environment with NSG lockdown, private endpoints, and firewalls. Follow [Secure Cloud Configuration](../05-secure-cloud-configuration/).
5. Use the saved workbook JSON, analytics rules, KQL queries, and attack scripts in this folder (see [Folder contents](#folder-contents)).
6. Come back here and work through the final results below.

## Final results and metrics

### Part 2: Measure the insecure environment for 24 hours

7. Leave everything exposed. Both VMs have wide-open NSGs and wide-open host firewalls, and the storage account and key vault have public endpoints. No private endpoints are in use.
8. Open each Sentinel workbook with Time Range Last 24 hours and Visualization Map. Each one joins its log table with the `geo_ipv4` and `geo_ipv4_cities` watchlists through `ipv4_lookup` to place each source IP on the map.
   Expected result (Linux SSH Auth Failure, `Syslog` where Facility is `auth` and the message starts with `Failed password for`): clusters in the US, Europe, Russia, and East and Southeast Asia. Top sources were North Bergen (US) 34, Moscow 32, Singapore 31, Nuremberg 31, and Tappahannock (US) 31.
   Expected result (SQL Server authentication failures, `Event` where EventLog is `Application` and EventID is `18456`; the workbook was titled "MySQL Authentication Failures"): Russia 4.17K, Netherlands 2.12K, Meppel (Netherlands) 2.11K, Moscow 1.51K, St Petersburg 89, United States 3.
   Expected result (nsg-malicious-allowed-in, `AzureNetworkAnalytics_CL` where FlowType_s is `MaliciousFlow`): points across North America, Europe, Russia, and Asia. Top sources were Ukraine 185, Moscow 164, Panama 148, Tappahannock (US) 123, and China 117.
   Expected result (Windows RDP and SMB Authentication Failure, `SecurityEvent` where EventID is `4625`): Ukraine 4.5K, Panama 3K, Toronto 989, Ipoh (Malaysia) 613, Nizhniy Novgorod (Russia) 522.
9. Record the 24-hour counts for each table.
   Expected result:

   | Metric | Count |
   | --- | --- |
   | SecurityEvent | 39046 |
   | Syslog | 782 |
   | SecurityAlert | 1 |
   | SecurityIncident | 222 |
   | AzureNetworkAnalytics_CL | 1350 |

### Part 3: Harden and measure again for 24 hours

10. Lock down the NSGs to block all inbound traffic except your admin workstation, then re-open the four workbooks.
    Expected result: the Linux SSH, SQL Server, and Windows RDP and SMB workbooks return no results. The NSG malicious-flows map is still populated worldwide in that 24-hour window, led by London (125), China (98), and the United States (94).
11. Put the storage account and key vault behind their built-in firewalls and private endpoints inside the VNet subnet, and finish hardening the systems.
12. Re-run every workbook over the next 24 hours.
    Expected result: all four workbooks (Linux SSH, SQL Server, nsg-malicious-allowed-in, Windows RDP and SMB) show "The query returned no results." In one snapshot the NSG legend listed a single source (Tromso, Norway: 1 flow) while the map still drew older bubbles.
13. Record the counts again for the window from 2023-03-18 15:37 to 2023-03-19 15:37.
    Expected result:

    | Metric | Count |
    | --- | --- |
    | SecurityEvent | 0 (-100%) |
    | Syslog | 0 (-100%) |
    | SecurityAlert | 0 (-100%) |
    | SecurityIncident | 0 (-100%) |
    | AzureNetworkAnalytics_CL | 0 (-100%) |

## Folder contents

- `Attack-Scripts/`: PowerShell scripts that simulate brute force and malware activity against the lab (Azure AD, SQL, Key Vault, EICAR test file).
- `Sentinel-Maps(JSON)/` and `Sentinel-Analytics-Rules/`: Sentinel workbook map definitions and the analytics rule export used in the labs.
- `KQL-Queries`: saved Kusto queries used during investigation.
- `Top 300 Azure Sentinel Used Cases KQL (Kusto Query Language).pdf`: reference sheet of Sentinel KQL use cases.
- The before and after workbook screenshots are described in the results above. The original image files remain in the git history.

## What I learned

- How the pieces of a cloud SOC connect: resources send logs to Log Analytics, and Sentinel turns them into maps, alerts, and incidents.
- Internet-exposed VMs and databases draw thousands of brute-force attempts within a day, from all over the world.
- Restricting NSGs is the change that clears the authentication-failure maps. Moving PaaS services behind private endpoints and firewalls then dropped every measured metric to zero for the next 24 hours.
- GeoIP watchlists plus `ipv4_lookup` turn raw IPs in logs into attack maps that are easy to read.
- With real users on the network, some events and alerts would still appear after hardening, so zero here reflects an idle lab rather than a production baseline.

## Next steps / cleanup

- Delete the lab resource groups when you finish to stop charges from VMs, Defender plans, and Sentinel.

## Sources

This section combines two earlier repos: `Cloud-SOC-Project-Directory` (series overview and shared files) and `Cloud-SOC-Final` (series recap and final metrics). Both histories are preserved in this repo.

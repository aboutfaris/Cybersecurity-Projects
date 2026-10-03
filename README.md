# Building a SOC and Honeynet in Azure (Live Traffic): Series Recap

This is the wrap-up of a five-lab series. I built a small honeynet in Azure, sent its logs to a Log Analytics workspace, used Microsoft Sentinel to build attack maps, alerts, and incidents, then measured attack metrics for 24 hours before and 24 hours after hardening the environment.

In the finished design, attackers on the internet reach Azure AD, a SQL database, and two VMs behind NSGs. Those resources, plus Blob Storage, Key Vault, and the Activity Log, all send logs to one Log Analytics workspace. Sentinel reads that workspace and turns it into maps, incidents, and alerts.

## What you'll use

- Azure Virtual Network (VNet) and Network Security Groups (NSGs)
- Virtual machines: 2 Windows, 1 Linux
- Log Analytics workspace and Microsoft Sentinel
- Azure Key Vault and an Azure Storage account
- Microsoft Defender for Cloud
- KQL with GeoIP watchlists for the attack maps

## Prerequisites

- An Azure subscription (the free trial credit covers the labs if you clean up afterwards).
- The five lab repos below, done in order.

## Steps

### Part 1: Follow the labs in order

1. Build the VMs, network, and attack VM: [Cloud-SOC-PreReq](https://github.com/aboutfaris/Cloud-SOC-PreReq).
2. Send tenant, subscription, and resource logs into the workspace and load the GeoIP watchlists: [Logging-and-Monitoring](https://github.com/aboutfaris/Logging-and-Monitoring).
3. Build the Sentinel attack-map workbooks, analytics rules, and incidents: [Microsoft-Sentinel-SIEM](https://github.com/aboutfaris/Microsoft-Sentinel-SIEM).
4. Harden the environment with NSG lockdown, private endpoints, and firewalls: [Secure-Cloud-Configuration](https://github.com/aboutfaris/Secure-Cloud-Configuration).
5. Use the saved workbook JSON, analytics rules, and KQL queries: [Cloud-SOC-Project-Directory](https://github.com/aboutfaris/Cloud-SOC-Project-Directory).

### Part 2: Measure the insecure environment for 24 hours

6. Leave everything exposed. Both VMs have wide-open NSGs and wide-open host firewalls, and the storage account and key vault have public endpoints. No private endpoints are in use.
7. Open each Sentinel workbook with Time Range Last 24 hours and Visualization Map. Each one joins its log table with the `geo_ipv4` and `geo_ipv4_cities` watchlists through `ipv4_lookup` to place each source IP on the map.
   Expected result (Linux SSH Auth Failure, `Syslog` where Facility is `auth` and the message starts with `Failed password for`): clusters in the US, Europe, Russia, and East and Southeast Asia. Top sources were North Bergen (US) 34, Moscow 32, Singapore 31, Nuremberg 31, and Tappahannock (US) 31.
   Expected result (SQL Server authentication failures, `Event` where EventLog is `Application` and EventID is `18456`; the workbook was titled "MySQL Authentication Failures"): Russia 4.17K, Netherlands 2.12K, Meppel (Netherlands) 2.11K, Moscow 1.51K, St Petersburg 89, United States 3.
   Expected result (nsg-malicious-allowed-in, `AzureNetworkAnalytics_CL` where FlowType_s is `MaliciousFlow`): points across North America, Europe, Russia, and Asia. Top sources were Ukraine 185, Moscow 164, Panama 148, Tappahannock (US) 123, and China 117.
   Expected result (Windows RDP and SMB Authentication Failure, `SecurityEvent` where EventID is `4625`): Ukraine 4.5K, Panama 3K, Toronto 989, Ipoh (Malaysia) 613, Nizhniy Novgorod (Russia) 522.
8. Record the 24-hour counts for each table.
   Expected result:

   | Metric | Count |
   | --- | --- |
   | SecurityEvent | 39046 |
   | Syslog | 782 |
   | SecurityAlert | 1 |
   | SecurityIncident | 222 |
   | AzureNetworkAnalytics_CL | 1350 |

### Part 3: Harden and measure again for 24 hours

9. Lock down the NSGs to block all inbound traffic except your admin workstation.
10. Put the storage account and key vault behind their built-in firewalls and private endpoints inside the VNet subnet.
11. Re-run every workbook over the next 24 hours.
    Expected result: all four workbooks (Linux SSH, SQL Server, nsg-malicious-allowed-in, Windows RDP and SMB) show "The query returned no results."
12. Record the counts again for the window from 2023-03-18 15:37 to 2023-03-19 15:37.
    Expected result:

    | Metric | Count |
    | --- | --- |
    | SecurityEvent | 0 (-100%) |
    | Syslog | 0 (-100%) |
    | SecurityAlert | 0 (-100%) |
    | SecurityIncident | 0 (-100%) |
    | AzureNetworkAnalytics_CL | 0 (-100%) |

## What I learned

- Internet-exposed VMs draw thousands of brute-force attempts within a day, from all over the world.
- Closing NSGs and moving PaaS services behind private endpoints and firewalls dropped every measured metric to zero for the next 24 hours.
- GeoIP watchlists plus `ipv4_lookup` turn raw IPs in logs into attack maps that are easy to read.
- With real users on the network, some events and alerts would still appear after hardening, so zero here reflects an idle lab rather than a production baseline.

## Next steps / cleanup

- Delete the lab resource groups when you finish to stop charges from VMs, Defender plans, and Sentinel.

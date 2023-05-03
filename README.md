# Building a SOC + Honeynet in Azure (Live Traffic) Comprehensive Summary

![68747470733a2f2f692e696d6775722e636f6d2f5a5778653033652e6a7067](https://user-images.githubusercontent.com/109401839/236074219-a957c5f2-21e9-4501-9d9d-ed879e01558f.jpg)


## Introduction

In this project, I build a mini honeynet in Azure and ingest log sources from various resources into a Log Analytics workspace, which is then used by Microsoft Sentinel to build attack maps, trigger alerts, and create incidents. I measured some security metrics in the insecure environment for 24 hours, apply some security controls to harden the environment, measured metrics for another 24 hours, and then show the results below. The metrics we will show are:

- SecurityEvent (Windows Event Logs)
- Syslog (Linux Event Logs)
- SecurityAlert (Log Analytics Alerts Triggered)
- SecurityIncident (Incidents created by Sentinel)
- AzureNetworkAnalytics_CL (Malicious Flows allowed into our honeynet)

## Architecture Before Hardening / Security Controls
![Architecture Diagram](https://i.imgur.com/aBDwnKb.jpg)

## Architecture After Hardening / Security Controls
![Architecture Diagram](https://i.imgur.com/YQNa9Pp.jpg)

The architecture of the mini honeynet in Azure consists of the following components:

- Virtual Network (VNet)
- Network Security Group (NSG)
- Virtual Machines (2 Windows, 1 Linux)
- Log Analytics Workspace
- Azure Key Vault
- Azure Storage Account
- Microsoft Sentinel

## Attack Maps Before Hardening / Security Controls

For the "BEFORE" metrics, all resources were originally deployed, and exposed to the internet. The Virtual Machines had both their Network Security Groups and built-in firewalls wide open, and all other resources are deployed with public endpoints visible to the Internet; aka, no use for Private Endpoints.

![Linux SSH Auth Failure (Before)](https://user-images.githubusercontent.com/109401839/235823253-36926afe-3fbb-4292-a47b-69b3224f48fb.png)

![MySQL Authentication Failures(Before)](https://user-images.githubusercontent.com/109401839/235823254-a3fb0c78-d5b0-4bf2-81b1-6ed1b85dead3.png)

![nsg-malicious-allowed-in (before)](https://user-images.githubusercontent.com/109401839/235823255-188f63c4-9d83-445b-9400-ca44041e7f2c.png)

![Windows RDP   SMB Authentication Failure(Before)](https://user-images.githubusercontent.com/109401839/235823259-ba8c71e4-3a75-4120-849e-7d9292b410a7.png)


## Metrics Before Hardening / Security Controls

For the "AFTER" metrics, Network Security Groups were hardened by blocking ALL traffic except for my admin workstation, and all other resources were protected by their built-in firewalls as well as Private Endpoint


![Windows RDP   SMB Authentication Failure](https://user-images.githubusercontent.com/109401839/235823321-8e9e3872-e7e7-4522-a35f-575f6e1ff0de.png)

![Linux SSH Auth Failure](https://user-images.githubusercontent.com/109401839/235823323-235a76cb-f94d-4855-adcf-edeb181a0982.png)

![MySQL Authentication Failures](https://user-images.githubusercontent.com/109401839/235823324-ef77ef97-c763-4f3b-a17c-9847d9504c51.png)

![nsg-malicious-allowed-in](https://user-images.githubusercontent.com/109401839/235823325-6efbd17d-06e1-4003-957c-a9fbed4570bd.png)

```All map queries returned no results due to no instances of malicious activity for the 24-hour period after hardening.```

The following table shows the metrics we measured in our insecure environment for 24 hours:
<div>

| Metric                   | Count
| ------------------------ | -----
| SecurityEvent            | 39046
| Syslog                   | 782
| SecurityAlert            | 1
| SecurityIncident         | 222
| AzureNetworkAnalytics_CL | 1350


## Metrics After Hardening / Security Controls

The following table shows the metrics we measured in our environment for another 24 hours, but after we applied security controls:
Start Time 2023-03-18 15:37
Stop Time	2023-03-19 15:37

| Metric                   | Count
| ------------------------ | -----
| SecurityEvent            | 0 (-100%)
| Syslog                   | 0 (-100%)
| SecurityAlert            | 0 (-100%) 
| SecurityIncident         | 0 (-100%)
| AzureNetworkAnalytics_CL | 0 (-100%)

## Conclusion

In this project, a mini honeynet was constructed in Microsoft Azure and log sources were integrated into a Log Analytics workspace. Microsoft Sentinel was employed to trigger alerts and create incidents based on the ingested logs. Additionally, metrics were measured in the insecure environment before security controls were applied, and then again after implementing security measures. It is noteworthy that the number of security events and incidents was drastically reduced after the security controls were applied, demonstrating their effectiveness.

It is worth noting that if the resources within the network were heavily utilized by regular users, it is likely that more security events and alerts may have been generated within the 24 hours following the implementation of the security controls.

# Building a SOC + Honeynet in Azure (Live Traffic) Comprehensive Summary
![Cloud Honeynet / SOC](https://i.imgur.com/ZWxe03e.jpg)

## Introduction

In this project, I build a mini honeynet in Azure and ingest log sources from various resources into a Log Analytics workspace, which is then used by Microsoft Sentinel to build attack maps, trigger alerts, and create incidents. I measured some security metrics in the insecure environment for 24 hours, apply some security controls to harden the environment, measure metrics for another 24 hours, then show the results below. The metrics we will show are:

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
- Virtual Machines (2 windows, 1 linux)
- Log Analytics Workspace
- Azure Key Vault
- Azure Storage Account
- Microsoft Sentinel

For the "BEFORE" metrics, all resources were originally deployed, exposed to the internet. The Virtual Machines had both their Network Security Groups and built-in firewalls wide open, and all other resources are deployed with public endpoints visible to the Internet; aka, no use for Private Endpoints.

![Linux SSH Auth Failure (Before)](https://user-images.githubusercontent.com/109401839/235729193-7b789d7e-2b2e-4f70-ba19-c9f7cfb6f369.png)

![MySQL Authentication Failures(Before)](https://user-images.githubusercontent.com/109401839/235729194-cf4c4918-2953-447c-a945-406b358c5a00.png)

![nsg-malicious-allowed-in (before)](https://user-images.githubusercontent.com/109401839/235729209-c4b5216c-9d0c-43e1-b270-1f6da8ca2845.png)

![Windows RDP   SMB Authentication Failure(Before)](https://user-images.githubusercontent.com/109401839/235729210-0c0f6c47-6db7-41a7-9c12-a41861b00f9e.png)


For the "AFTER" metrics, Network Security Groups were hardened by blocking ALL traffic with the exception of my admin workstation, and all other resources were protected by their built-in firewalls as well as Private Endpoint

![Linux SSH Auth Failure](https://user-images.githubusercontent.com/109401839/235729264-56cdce9b-5c9a-46ee-bd76-d291faa7fbf8.png)

![MySQL Authentication Failures](https://user-images.githubusercontent.com/109401839/235729270-99323804-9328-41c9-b25b-59e63e7a101c.png)

![nsg-malicious-allowed-in](https://user-images.githubusercontent.com/109401839/235729275-dfa0f88b-49ac-4fd2-9842-89396d8a67fb.png)

![Windows RDP   SMB Authentication Failure](https://user-images.githubusercontent.com/109401839/235729282-8afeb409-fd5c-4fa9-8ac7-cf311a711807.png)


## Attack Maps Before Hardening / Security Controls
![NSG Allowed Inbound Malicious Flows](Insert ref Image
![Linux Syslog Auth Failures]Insert ref Image
![Windows RDP/SMB Auth Failures] Insert ref Image

## Metrics Before Hardening / Security Controls

The following table shows the metrics we measured in our insecure environment for 24 hours:
<div>

| Metric                   | Count
| ------------------------ | -----
| SecurityEvent            | 39046
| Syslog                   | 782
| SecurityAlert            | 1
| SecurityIncident         | 222
| AzureNetworkAnalytics_CL | 1350

## Attack Maps Before Hardening / Security Controls

```All map queries actually returned no results due to no instances of malicious activity for the 24 hour period after hardening.```

## Metrics After Hardening / Security Controls

The following table shows the metrics we measured in our environment for another 24 hours, but after we have applied security controls:
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

In this project, a mini honeynet was constructed in Microsoft Azure and log sources were integrated into a Log Analytics workspace. Microsoft Sentinel was employed to trigger alerts and create incidents based on the ingested logs. Additionally, metrics were measured in the insecure environment before security controls were applied, and then again after implementing security measures. It is noteworthy that the number of security events and incidents were drastially reduced after the security controls were applied, demonstrating their effectiveness.

It is worth noting that if the resources within the network were heavily utilized by regular users, it is likely that more security events and alerts may have been generated within the 24-hour period following the implementation of the security controls.

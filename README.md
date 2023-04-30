# Securing The Cloud Configuration

## We are simply going to reduce the risks as much as possible by the following sections: 

<div>

### Objectives: 

- Regulatory Compliance (NIST 800-53, PCI DSS, CIS) and MDC Recommendations

- Azure Private Link & Firewall for Resources

- Run SECURE Environment for 24 Hours and Capture Analytics

### Environments and Technologies Used:

- Microsoft Azure
- Microsoft Sentinel
- Microsoft Cloud Defender

### Operating Systems Used:

- VM Windows 10 PRO (21H2)
- VM Linux Ubuntu 20.12

#### Regulatory Compliance (NIST 800-53, PCI DSS, CIS) and MDC Recommendations 
<details close>

<div>

</summary>

Reminder: Check your Subscription’s Cost Analysis

### Actions and Observations<b>

- Overview Currently 

![vivaldi_ILnTZamtya](https://user-images.githubusercontent.com/109401839/235340696-8d247dcd-e45f-4e6c-ba90-a6f1d4257766.png)

Click on Recommendations. 
Ideally we want to get to 100%. 

![vivaldi_sKRdqBEO7l](https://user-images.githubusercontent.com/109401839/235340928-3ad8b009-b1e7-46cd-920c-1b168c094904.png)

Currently, I am at 54%. So go through each, apply each remediation steps according to Azure and get your score up. 

I will start with the DDos Protection and I wont show everything. However, take your time with this and Azure redirects you to everything. 

![vivaldi_GYcRzsJZK3](https://user-images.githubusercontent.com/109401839/235341029-feb752ee-2793-4a72-b2d0-99c710a27413.png)

![vivaldi_bLyC34Yftz](https://user-images.githubusercontent.com/109401839/235341064-6f41ab48-2787-4e66-8cdf-c00ad7941996.png)


### Azure Private Link & Firewall for Resources
<details close>

<div>

</summary>




### Run SECURE Environment for 24 Hours and Capture Analytics
<details close>

<div>

</summary>



After 24 Hours: 
<div>

| Metric                   | Count
| ------------------------ | -----
| SecurityEvent            | 0
| Syslog                   | 0
| SecurityAlert            | 0
| SecurityIncident         | 0
| AzureNetworkAnalytics_CL | 0


Well, this series of projects in Microsoft Azure is finally at its conclusion. Over time there will be updates and cleaning up. However, whoever is viewing this. I hope  you learned a lot because I have learned a lot. Thank you.

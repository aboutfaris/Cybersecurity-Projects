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

After 24 Hours of Configuring NSG: 
<div>

| Metric                   | Count
| ------------------------ | -----
| SecurityEvent            | 2401 (-93.85%)
| Syslog                   | 730 (-6.65%)
| SecurityAlert            | 0 (-100.00%)
| SecurityIncident         | 185 (-16.67%)
| AzureNetworkAnalytics_CL | 68 (-94.96%)

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

Currently, I am at 54%, apply each remediation steps according to Azure and get your score up. 

I will start with the DDos Protection and I wont show everything. However, take your time with this and Azure redirects you to everything. 

![vivaldi_GYcRzsJZK3](https://user-images.githubusercontent.com/109401839/235341029-feb752ee-2793-4a72-b2d0-99c710a27413.png)

![vivaldi_bLyC34Yftz](https://user-images.githubusercontent.com/109401839/235341064-6f41ab48-2787-4e66-8cdf-c00ad7941996.png)

In the next lab, we will go over the important Recommendations to secure our environment. Another project will show case getting the score to near 100 or at 100%. The question I will pose for that project is, "Having a 100% secure lab the best security measure?".

Now, let enter the final phase of the Cloud SOC Projects. 

### Azure Private Link & Firewall for Resources
<details close>

<div>

</summary>

![image](https://user-images.githubusercontent.com/109401839/235408787-7acc45e8-904f-4bfb-b4ec-7c6668f4453f.png)

### Goals for this lab:

- Inspect MDC Regulatory Compliance (Available and Implemented)
- NIST 800-53 (Ref)
- We will Implement SC-7

1. Configure Azure Private Link and Firewall for your Azure Key Vault Instance.
> Ensure you use the same region and VNet the rest of your VMs are located. 

![vivaldi_9kA8hVnhML](https://user-images.githubusercontent.com/109401839/235410803-679cf671-0110-41fd-b8be-973f7ccfd1ef.png)

1a. In the Firewalls, we will disable public access. 
> Allow trusted Miscrosoft services to bypass this firewall. 

``` When you enable the Key Vault Firewall, you'll be given an option to 'Allow Trusted Microsoft Services to bypass this firewall.' The trusted services list does not cover every single Azure service. For example, Azure DevOps isn't on the trusted services list. This does not imply that services that do not appear on the trusted services list are not trusted or are insecure. The trusted services list encompasses services where Microsoft controls all of the code that runs on the service. Since users can write custom code in Azure services such as Azure DevOps, Microsoft does not provide the option to create a blanket approval for the service. Furthermore, just because a service appears on the trusted service list, doesn't mean it is allowed for all scenarios.```

1b. Configure Private EndPoint Connections

![vivaldi_llF7NrXeNU](https://user-images.githubusercontent.com/109401839/235411138-05197fc9-624a-468a-ab20-ad808c69a5ef.png)

![vivaldi_IrwcXIE1uZ](https://user-images.githubusercontent.com/109401839/235411183-457d39ff-35f8-4e5e-baab-49a837b68374.png)

![vivaldi_cJOoHn4kRF](https://user-images.githubusercontent.com/109401839/235411232-1548ec0e-7b55-45f7-9a47-b06e61d0faa8.png)

![vivaldi_Cn9neeLZKd](https://user-images.githubusercontent.com/109401839/235411264-b876bf35-6a51-42e7-886b-c13b8c518e10.png)

![vivaldi_vDj1nUhARA](https://user-images.githubusercontent.com/109401839/235411275-0b16cd2a-b161-4fd2-b1df-683bfbfae3cf.png)

	
2. Configure Azure Private Link and Firewall for your Azure Storage Account instance

2a. Disable Public Access and configure EndPoint, repeat the steps above. 

![vivaldi_PjlZ3MgRi4](https://user-images.githubusercontent.com/109401839/235411592-2bd15e1a-7cbc-4686-8953-9c54c496ea27.png)

2b. This is done on the network tab as well as the Settings -> configuration “Allow Blob public access → Disabled” as well

![image](https://user-images.githubusercontent.com/109401839/235411467-3ed9c0d9-5e93-4800-bcc5-2d38bbcbcc89.png)

> The DNS will assign a private IP Address and resources will resolve to this IP.

3. Observe Network Watcher Topology

![vivaldi_fQ3YVFUNu1](https://user-images.githubusercontent.com/109401839/235411888-fadc37ab-db2b-4d4c-bc26-80bc95713900.png)

4. Observe the Key Vault and Storage Account Private Endpoints

5. Login to “windows-vm” and check the IP addresses of your Key Vault and Storage Account instances.

5a. My keyvault address, ```https://akv-cyber-lab5.vault.azure.net/``` 

![mstsc_fxQfHckld4](https://user-images.githubusercontent.com/109401839/235413357-0963704d-9468-49ca-a17c-b45c80d13314.png)

We can see it is resolving to a private IP address which means out Endpoint is working! Not solely because of the IP address, but because it is resolving to a private IP address within out subnet range. 
If it was not working, we would have to troubleshoot.

Now, lets try this but on our own computers, not the virtual machines. 

![image](https://user-images.githubusercontent.com/109401839/235414783-fb98d0c3-2339-4f25-a017-7f6f53f927a1.png)

We can resolve it and it shows a public IP address but we do not have access to it. 

This is an important distinction because my home computer is not on the VNET that the keyvault is located on. 

5b. Storage account address, ```https://sacyberlab05.blob.core.windows.net/``` <- This comes from the Blob service. If you remember moments ago, this was turned off to disconnect access from the public web to our services. 

Lets try this on our non-azure computer:

![image](https://user-images.githubusercontent.com/109401839/235414638-2113a6d0-5bdf-476d-997f-430a5c876b21.png)


![Discord_Q2mMinCHmZ](https://user-images.githubusercontent.com/109401839/235414029-26c69c5d-3bfb-44e8-8c43-45e24714370d.png)


### Troubleshooting Methods:

> They should be private addresses, indicating the resources have been probably integrated into private VNet.

> If you see a public IP address, either it’s not done propagating yet, or it’s not configured correctly.

> Possible causes for this are your resources and VM are actually in different Virtual Networks, or something is just not setup right.

> The good news is, you don’t need to fix this for the rest of the lab, we are just trying to lock down the environment. 

> However, if you want to fix it, you can try deleting the Private Endpoints/config and trying again.

### Run SECURE Environment for 24 Hours and Capture Analytics
<details close>

<div>

</summary>

<div>

After 24 Hours of Locking - Down Environment: 

| Metric                   | Count
| ------------------------ | -----
| SecurityEvent            | 0
| Syslog                   | 0
| SecurityAlert            | 0 
| SecurityIncident         | 0
| AzureNetworkAnalytics_CL | 0

<div>

Well, this series of projects in Microsoft Azure is finally at its conclusion.

Over time there will be updates and cleaning up. 

However, whoever is viewing this. 

I hope  you learned a lot because I have learned a lot. 

I started this project April 9th, 2023 and completed it May 1st, 2023.
Overall it took roughly two weeks to complete everything. 
Handling personal matters, took time away from this project.

Next project, which is optional, will be a Business Data Analysis project of project. 

Thank you.

# Microsoft Sentinel (SIEM)

## Objectives for the next 8 Labs that will create our Logging and Monitoring System.

- World Attach Maps Constructions
- Analytics, Alerting, and Incident Generation
- Attack Traffic Generation
- Run Insecure Environment for 24 hours and Capture Analytics
- Incident 1 - Brute Force Success (Windows) | Working Incidents and Incident Response
- Incident 2 - Possible Privilege Escalating | Incident Response
- Incident 3 - Brute Force Success (Linux) | MS Sentinel working Incident Response
- Incident 4 - Possible Malware Outbreak | Incident Response

### Environments and Technologies Used:

- Microsoft Azure
- Microsoft Sentinel
- Microsoft Cloud Defender

### Operating Systems Used:

- VM Windows 10 PRO (21H2)
- VM Linux Ubuntu 20.12
<details close>

<div>

</summary>

Reminder: Check your Subscription’s Cost Analysis

#### Actions and Observations<b>

- We are going to create 4 different workbooks in Sentinel that show different types of malicious traffic from around the world, targeting our resources.
- We will use pre-built JSON maps to reduce the number of errors/questions, but will explain the process.

--- 

In Microsoft Sintinel | Workbooks , we will add a new workbook in order to create our map. JSON Files - Remember, Sentinel uses our Log Analytics Workspace where we ingested the logs.

![vivaldi_kLOHZRFPhj](https://user-images.githubusercontent.com/109401839/235279747-01e3bf0c-428d-4b71-b6f8-9e9dc99bae8d.png)

- Remove the pre-included reports. 
- Add Query
- Advanced Editor > Paste the [KQL .JSON Information](https://github.com/fnabeel/Cloud-SOC-Project-Directory/blob/main/Sentinel-Maps(JSON)/linux-ssh-auth-fail.json)

After running your query , your graph should populate! 

![vivaldi_1SnjH3R8Ip](https://user-images.githubusercontent.com/109401839/235279945-1eef8a2b-e778-4811-be63-3c9bf4c1e619.png)
 
> Note that each graph everyone makes will be different since this is based on the attacks I recieved in a certain timeframe! 

The KQL code we used shows us the Linux VM Authentication SSH Failures. 

- Edit > Settings > Map Settings > 

![heatmap](https://user-images.githubusercontent.com/109401839/235281773-e002056e-9f07-4082-9721-59c3f002f74f.PNG)

- Here you can customise the map and the details even further to your desire. I will keep it default. 

- Save Workbooks & Let us repeat the steps for the other maps. 

![vivaldi_YBA2LIqUJg](https://user-images.githubusercontent.com/109401839/235284830-a5b1ff91-cfd5-4381-a459-e6315be8f22d.png)

- Next we will create a graph for [MS SQL Authentication Fail](https://github.com/fnabeel/Cloud-SOC-Project-Directory/blob/main/Sentinel-Maps(JSON)/mssql-auth-fail.json)

![vivaldi_laXpbNeo86](https://user-images.githubusercontent.com/109401839/235286153-e23a0f2e-3b96-498b-a557-6d70f82e31c6.png)

- Now we will repeat it for the subsequent maps by entering the KQL code. 

- [NSG Malicious Allowed Firewall In](https://github.com/fnabeel/Cloud-SOC-Project-Directory/blob/main/Sentinel-Maps(JSON)/nsg-malicious-allowed-in.json)

![vivaldi_No4emgWydH](https://user-images.githubusercontent.com/109401839/235286714-73d14971-e942-479b-aa36-04c083dc86d5.png)

- [Windows RDP & SMB Authentication Failures](https://github.com/fnabeel/Cloud-SOC-Project-Directory/blob/main/Sentinel-Maps(JSON)/windows-rdp-auth-fail.json)

![vivaldi_hMnU9a0ydS](https://user-images.githubusercontent.com/109401839/235286919-0ae35ece-b7c4-436b-a581-71c92169fb6b.png)

> We can edit and change the timeframe to see where and what attacks happened at a certain time. I will do 30 minutes as an example: 

![vivaldi_OyzflFZq3q](https://user-images.githubusercontent.com/109401839/235287139-9b47bb91-4efe-4b37-a498-6fd9d3fadd99.png)

- You should have 4 custom made workbooks like this:

![vivaldi_Ay5xt00GJN](https://user-images.githubusercontent.com/109401839/235287326-0fbd8e95-6d31-4032-bed2-112d4b8daac1.png)

In subsequent labs, we will create our own attacks at add to these maps. For example, say I create a VM in Malaysia and attack the homebase VM, a dot should be added to our graphs depending on our attack method. 
——————————————————————————————————————

Troubleshooting: 

- If it’s been 24 hours since you created the resources being tracked on this map and you don’t see traffic to them, make sure of the following:
First, generate traffic on your own to see if any logs show up

- Ensure both VMs are on

- Ensure Microsoft Defender for Cloud and the Data Collection Rules are configured correct to collect logs from the VMs (from section: Logging and Monitoring: Enable MDC and Configure Log Collection for Virtual Machines)

- Ensure Logging is correctly configured for MS SQL Server (from section: Azure Intro: Creating our Subscription and First Resources)

- If NSG FLow Logs are empty, ensure they are configured correctly (from section: Logging and Monitoring: Enable MDC and Configure Log Collection for Virtual Machines)

- Alternatively, you can skip ahead to the “Azure Sentinel: Attack Traffic Generation” section to generate some traffic, but we need to make sure logging is configured correctly and showing up before that will work.
——————————————————————————————————————



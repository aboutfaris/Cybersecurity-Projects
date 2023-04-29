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

#### World Attach Maps Constructions
<details close>

<div>

</summary>

Reminder: Check your Subscription’s Cost Analysis

### Actions and Observations<b>

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
<div>

Troubleshooting: 

- If it’s been 24 hours since you created the resources being tracked on this map and you don’t see traffic to them, make sure of the following:
First, generate traffic on your own to see if any logs show up

- Ensure both VMs are on

- Ensure Microsoft Defender for Cloud and the Data Collection Rules are configured correct to collect logs from the VMs (from section: Logging and Monitoring: Enable MDC and Configure Log Collection for Virtual Machines)

- Ensure Logging is correctly configured for MS SQL Server (from section: Azure Intro: Creating our Subscription and First Resources)

- If NSG FLow Logs are empty, ensure they are configured correctly (from section: Logging and Monitoring: Enable MDC and Configure Log Collection for Virtual Machines)

- Alternatively, you can skip ahead to the “Azure Sentinel: Attack Traffic Generation” section to generate some traffic, but we need to make sure logging is configured correctly and showing up before that will work.

<div> 

### Analytics, Alerting, and Incident Generation
<details close>

---

</summary>

In this lab we will be working on Analytics, Alerting, and Incident Generation.

- We are going to manually going to add the rules, and then trigger the alerts. We will dissect the alert and really understand what is happening. 

![image](https://user-images.githubusercontent.com/109401839/235291419-36c75299-c9a9-4b64-a51c-f4b10ce43164.png)

- First will be a brute force attempt by windows machine. 

``` 
SecurityEvent
| where EventID == 4625
| where TimeGenerated > ago(60m)
| summarize FailureCount = count() by SourceIP = IpAddress, EventID, Activity
| where FailureCount >= 10
```

> So we enter this Query under our Log Analytic workspace. Run it. It will show the EventID of 4625 in the given timeframe you selected. In this case, 60 minutes. Then the next like will be our categories and show us the Failure count. Was it all the same attacks or 10 instances of the same IP, EventID and Activity trying to attack. Thats what the failure count does. 

> So we do not want to create an alert based on a user making a mistake a few times, but over ten times is a little suspicious and we can create an alert based on that. 

![vivaldi_hQThPXrMWs](https://user-images.githubusercontent.com/109401839/235291881-b7fe654d-cdeb-4cc3-91c5-95119ab87169.png)

> Feel free to use ChatGPT to have a more in depth explanation if the one above was insufficient. 

![analytics query](https://user-images.githubusercontent.com/109401839/235292182-1ddd325e-a980-4422-99e5-02b6f35a3985.PNG)

We will add a query rule now, that is the same as the previous KQL query. 

Tactics and Techniques:
Credential Access > Brute Force
Enter it in and run it again: 

![mqFhzU2BOQ](https://user-images.githubusercontent.com/109401839/235292423-4695e167-f043-4680-af60-02da62454464.png)

- In Alert enrichment > Entity Mapping 

Set up IP Entity | Address | AttackerIP

- Add new entity:

Set up Host | Hostname | DestinationHostName 

![vivaldi_G4GbbxRRLc](https://user-images.githubusercontent.com/109401839/235292538-96a1b891-dbf7-4466-8234-bf9eb3aa1dfb.png)

> So say that an attacker with an IP address 1.1.1.1 attacks our network, we will get an alert.. however Sentinel will track that IP Address and correlate that addresses further action and map it to other alerts. 

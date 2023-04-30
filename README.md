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

- We will use pre-built JSON maps to reduce the number of errors/questions but will explain the process.

--- 

> In Microsoft Sentinel | Workbooks, we will add a new workbook in order to create our map. JSON Files - Remember, Sentinel uses our Log Analytics Workspace where we ingested the logs.

![vivaldi_kLOHZRFPhj](https://user-images.githubusercontent.com/109401839/235279747-01e3bf0c-428d-4b71-b6f8-9e9dc99bae8d.png)

- Remove the pre-included reports. 
- Add Query
- Advanced Editor > Paste the [KQL .JSON Information](https://github.com/fnabeel/Cloud-SOC-Project-Directory/blob/main/Sentinel-Maps(JSON)/linux-ssh-auth-fail.json)

> After running your query, your graph should populate! 

![vivaldi_1SnjH3R8Ip](https://user-images.githubusercontent.com/109401839/235279945-1eef8a2b-e778-4811-be63-3c9bf4c1e619.png)
 
> Note that each graph everyone makes will be different since this is based on the attacks I received in a certain timeframe! 

> The KQL code we used shows us the Linux VM Authentication SSH Failures. 
 Edit > Settings > Map Settings > 

![heatmap](https://user-images.githubusercontent.com/109401839/235281773-e002056e-9f07-4082-9721-59c3f002f74f.PNG)

> Here you can customise the map and the details even further to your desire. I will keep it default. 

> Save Workbooks & Let us repeat the steps for the other maps. 

![vivaldi_YBA2LIqUJg](https://user-images.githubusercontent.com/109401839/235284830-a5b1ff91-cfd5-4381-a459-e6315be8f22d.png)

> Next, we will create a graph for [MS SQL Authentication Fail](https://github.com/fnabeel/Cloud-SOC-Project-Directory/blob/main/Sentinel-Maps(JSON)/mssql-auth-fail.json)

![vivaldi_laXpbNeo86](https://user-images.githubusercontent.com/109401839/235286153-e23a0f2e-3b96-498b-a557-6d70f82e31c6.png)

> Now we will repeat it for the subsequent maps by entering the KQL code. 

- [NSG Malicious Allowed Firewall In](https://github.com/fnabeel/Cloud-SOC-Project-Directory/blob/main/Sentinel-Maps(JSON)/nsg-malicious-allowed-in.json)

![vivaldi_No4emgWydH](https://user-images.githubusercontent.com/109401839/235286714-73d14971-e942-479b-aa36-04c083dc86d5.png)

- [Windows RDP & SMB Authentication Failures](https://github.com/fnabeel/Cloud-SOC-Project-Directory/blob/main/Sentinel-Maps(JSON)/windows-rdp-auth-fail.json)

![vivaldi_hMnU9a0ydS](https://user-images.githubusercontent.com/109401839/235286919-0ae35ece-b7c4-436b-a581-71c92169fb6b.png)

> We can edit and change the timeframe to see where and what attacks happened at a certain time. I will do 30 minutes as an example: 

![vivaldi_OyzflFZq3q](https://user-images.githubusercontent.com/109401839/235287139-9b47bb91-4efe-4b37-a498-6fd9d3fadd99.png)

> You should have 4 custom-made workbooks like this:

![vivaldi_Ay5xt00GJN](https://user-images.githubusercontent.com/109401839/235287326-0fbd8e95-6d31-4032-bed2-112d4b8daac1.png)

> In subsequent labs, we will create our own attacks at add to these maps. For example, say I create a VM in Malaysia and attack the home base VM, a dot should be added to our graphs depending on our attack method. 
<div>

### Troubleshooting: 

> If it’s been 24 hours since you created the resources being tracked on this map and you don’t see traffic to them, make sure of the following:
First, generate traffic on your own to see if any logs show up

> Ensure both VMs are on

> Ensure Microsoft Defender for Cloud and the Data Collection Rules are configured correctly to collect logs from the VMs (from the section: Logging and Monitoring: Enable MDC and Configure Log Collection for Virtual Machines)

> Ensure Logging is correctly configured for MS SQL Server (from the section: Azure Intro: Creating our Subscription and First Resources)

> If NSG Flow Logs are empty, ensure they are configured correctly (from the section: Logging and Monitoring: Enable MDC and Configure Log Collection for Virtual Machines)

> Alternatively, you can skip ahead to the “Azure Sentinel: Attack Traffic Generation” section to generate some traffic, but we need to make sure logging is configured correctly and showing up before that will work.

<div> 

### Analytics, Alerting, and Incident Generation
<details close>

---

</summary>

- In this lab, we will be working on Analytics, Alerting, and Incident Generation.

- We are going to manually go to add the rules, and then trigger the alerts. We will dissect the alert and really understand what is happening. 

![image](https://user-images.githubusercontent.com/109401839/235291419-36c75299-c9a9-4b64-a51c-f4b10ce43164.png)

> First will be a brute force attempt by a Windows machine. 

``` 
SecurityEvent
| where EventID == 4625
| where TimeGenerated > ago(60m)
| summarize FailureCount = count() by SourceIP = IpAddress, EventID, Activity
| where FailureCount >= 10
```

> So we enter this Query under our Log Analytic workspace. Run it. It will show the EventID of 4625 in the given timeframe you selected. In this case, 60 minutes. Then the next like will be our categories and show us the Failure count. Was it all the same attacks or 10 instances of the same IP, EventID and Activity trying to attack? That's what the failure count does. 

> So we do not want to create an alert based on a user making a mistake a few times, but over ten times is a little suspicious and we can create an alert based on that. 

![vivaldi_hQThPXrMWs](https://user-images.githubusercontent.com/109401839/235291881-b7fe654d-cdeb-4cc3-91c5-95119ab87169.png)

> Feel free to use ChatGPT to have a more in-depth explanation if the one above was insufficient. 

![analytics query](https://user-images.githubusercontent.com/109401839/235292182-1ddd325e-a980-4422-99e5-02b6f35a3985.PNG)

> We will add a query rule now, that is the same as the previous KQL query. 

- Tactics and Techniques:
Credential Access > Brute Force
Enter it in and run it again: 

![mqFhzU2BOQ](https://user-images.githubusercontent.com/109401839/235292423-4695e167-f043-4680-af60-02da62454464.png)

> In Alert enrichment > Entity Mapping 

> Set up IP Entity | Address | AttackerIP

> Add new entity:

> Set up Host | Hostname | DestinationHostName 

![vivaldi_G4GbbxRRLc](https://user-images.githubusercontent.com/109401839/235292538-96a1b891-dbf7-4466-8234-bf9eb3aa1dfb.png)

> So say that an attacker with an IP address 1.1.1.1 attacks our network, we will get an alert.. however, Sentinel will track that IP Address and correlate that addresses further action and map it to other alerts. 

![vivaldi_qZYMU18mjY](https://user-images.githubusercontent.com/109401839/235292695-ed06b0e7-18c4-4dd4-8f33-44199cee9674.png)

![vivaldi_5FJZt75Ouo](https://user-images.githubusercontent.com/109401839/235292727-848a05fb-234b-4a61-9d11-9ce4b35af5c6.png)

> Our rule is ready to roll ~ validate & create. 

> We should see any incidents that it creates.

> And almost immediately we got an incident! 

![vivaldi_NgGrQCTZd8](https://user-images.githubusercontent.com/109401839/235292787-85b9164a-c584-4e35-b013-527551daae27.png)

![4MDWsCNOfs](https://user-images.githubusercontent.com/109401839/235292805-0fac1e01-6461-471b-98e6-c98ead18fdbe.png)


> On the bottom left, we can click "Investigation"  and it will show us a nice infographic of the attack on the host. 

![FZIXPOncAT](https://user-images.githubusercontent.com/109401839/235293224-ad6cf8a4-3069-42b0-b83b-a20adf271e6d.png)

- Now, we can delete that test incident alert and the test alert, we are going to import a bunch of the real queries.  

> If this portion did not work for you, as the query did not result in any incidents. You can remote into your VM and purposely fail the login attempt 10x in order to generate the incident! 

- Now download the query rule list to make life easier! 

---

[Sentinel Analytics Rules](https://github.com/fnabeel/Cloud-SOC-Project-Directory/blob/main/Sentinel-Analytics-Rules/Sentinel-Analytics-Rules(KQL%20Alert%20Queries).json)

---

> After importing the rules, we already have 4 incidents generated. Nothing like work. 

![vivaldi_AhVZHFFOyF](https://user-images.githubusercontent.com/109401839/235294286-eead3162-d19f-475f-a07b-aedd23433dec.png)

- Here are the active rules imported: 

![vivaldi_0qjWA3CiOA](https://user-images.githubusercontent.com/109401839/235294313-140f164c-e698-4425-9925-b238cf73b4ca.png)

- Play around and learn each part.

> For example CUSTOM: Possible Privilege Escalation (Global Admin Role Assignment)

> Under Set Rule Logic we can see the Rule Query. 

- We can break down this query: 

```
AuditLogs
| where OperationName == "Add member to role" and Result == "success"
| where TargetResources[0].modifiedProperties[1].newValue == '"Company Administrator"' and TargetResources[0].type == "User"
| project TimeGenerated, OperationName, AssignedRole = TargetResources[0].modifiedProperties[1].newValue, InitiatorId = InitiatedBy.user.id, InitiatorUpn = InitiatedBy.user.userPrincipalName, TargetAccountId = TargetResources[0].id, TargetAccountUpn = TargetResources[0].userPrincipalName, InitiatorIpAddress = InitiatedBy.user.ipAddress, Status = Result
```
---

- Here is a breakdown of each line:

> AuditLogs: This is the name of the table being queried. It likely contains logs of actions taken within a Microsoft Azure environment.

``` | where OperationName == "Add a member to role" and Result == "success": ```

> This line filters the results to only show entries where the operation name is "Add a member to the role" and the result was "success". This is likely used to narrow down the results to only show successful attempts to add a user to a role.

``` | where TargetResources[0].modifiedProperties[1].newValue == '"Company Administrator"' and TargetResources[0].type == "User": ``` 

> This line further filters the results to only show entries where the modified property at index 1 of the first TargetResource (a resource involved in the operation) is equal to the string "Company Administrator" and the type of the first TargetResource is "User". This is likely used to only show successful attempts to add a user to the "Company Administrator" role.

``` | project TimeGenerated, OperationName, AssignedRole = TargetResources[0].modifiedProperties[1].newValue, InitiatorId = InitiatedBy.user.id, InitiatorUpn = InitiatedBy.user.userPrincipalName, TargetAccountId = TargetResources[0].id, TargetAccountUpn = TargetResources[0].userPrincipalName, InitiatorIpAddress = InitiatedBy.user.ipAddress, Status = Result: ``` 

> This line projects (i.e., selects) specific columns from the filtered results and renames them for readability. 

> The selected columns include the time the log was generated (TimeGenerated), the operation name (OperationName), the assigned role (AssignedRole, which is the value of the modified property at index 1 of the first TargetResource), the ID of the user who initiated the operation (InitiatorId), the user principal name of the user who initiated the operation (InitiatorUpn), the ID of the target account (TargetAccountId, which is the ID of the first TargetResource), the user principal name of the target account (TargetAccountUpn, which is the user principal name of the first TargetResource), the IP address of the user who initiated the operation (InitiatorIpAddress, which is the IP address of the user who initiated the operation), and the status of the operation (Status, which is the result of the operation).

- Let us see what happened while you were reading this and I was typing this out. 

![Frq11TIXzC](https://user-images.githubusercontent.com/109401839/235294920-a287141b-00b4-4005-9c3d-4be26dffd13d.png)

> We got a brute force attempt on MS SQL Server.
Similar incidents are notified at the bottom. 

- Let us investigate:

![vivaldi_K8gJz7V9DX](https://user-images.githubusercontent.com/109401839/235294982-8e539741-227f-469d-b3c1-d31454a8d533.png)

> This is the spiral of despair...

> Let us revise the workbooks since these are relatively new and should reflect on the geolocation map within the timeframe of the attacks. 

![vivaldi_sbJlTVzF7M](https://user-images.githubusercontent.com/109401839/235295157-7cba01ca-2c81-4c49-b03d-7cab1c81fb77.png)

> In the last 30 minutes, 

![image](https://user-images.githubusercontent.com/109401839/235295217-06574230-fcb2-408e-b415-428896d83fe9.png)

> The entities show us the IP Address information. 

### Attack Traffic Generation Lab
<details close>

<div>

</summary>

#### Attacker Mode (pretend you are an attacker), perhaps a world-renowned Blackhat Hacker, let us cosplay this lab:

- First, let us generate some attack traffic to trigger alerts & incident generation, which the Internet (Thank you) has already done since the writing of the last lab. 

![vivaldi_BAtjUMJqrd](https://user-images.githubusercontent.com/109401839/235329080-bd59d747-8ef9-4947-8d91-5bf6d80dbf79.png)

> 73 Open Incidents. 2 High Alerts, oh boy. Let us make it 74.

- Log into “attack-vm” from our previous labs. 

- Open PowerShell as an Admin and install the Az Module if you haven’t already

- Download SSMS, Previous Lab (Optional)

- Download Visual Studio Code (Mandatory)

- Run PS Command ```Install-Module Az```

> "Yes to All "

![mstsc_au4u5GMQEb](https://user-images.githubusercontent.com/109401839/235329774-464dbb88-f6f9-4e2c-bd1e-a058f73a8fa1.png)

- Download the “Attack-Scripts” PowerShell Scripts and put the folder on your desktop

![mstsc_sDIJGG4fvK](https://user-images.githubusercontent.com/109401839/235329916-3f6f7f56-ba74-4fb1-bad9-af575f687056.png)

- Open the folder in VS Code

![mstsc_9oaG0rg5iC](https://user-images.githubusercontent.com/109401839/235329942-9306092d-fd87-4d5b-ab5d-0a21c03fa9a9.png)

 > Trust the authors, you are the author. Maybe... 

| Notice: You can do what these scripts do manually, however, it is good to get some experience using scripts to be more efficient with time and versatile. If you are unsure what each line in the script does, feel free to copy and paste it into ChatGPT. Then, request it to explain each line at XYZ age group so you can dissect, marinate that knowledge and then be able to comprehend further. All in due time, right? 

> VSC may ask you to install an extension for PowerShell, go ahead and install it. Now...

- Run each of the following scripts, observing the results in Log Analytics Workspace AND Sentinel Incident Creation:

- AAD-Brute-Force-Success-Simulator.ps1
(this can be done manually by trying to log into the portal)

Let us break down the main function for this: 

Line 1: ```$tenantId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" ```

> # Your Tenant ID, you can find on the AAD Blade in the Azure Portal...

Line 2: ``` $username = "attacker@[your user name].onmicrosoft.com" ```

> # Some Username that exists in your AAD Tenant.. in my case that is "attacker@fnabeelpm.onmicrosoft.com"

Line 3: ``` $correct_password = "LabTest12345" ``` 

> # Enter the correct password for the above user... If you cannot remember your password, you can reset it in your browser's incognito mode and sign on to Azure AD.

Line 4: ``` $wrong_password = "___WRONG PASSWORD___" ``` 

> # This is used to generate auth failures...

Line 5: ``` $max_attempts = 11  ``` 

> # This is the number of times to fail the login before succeeding. 

> So, we will let this run and it will create a loop for 11x failed login attempts, and then 1 successful login attempt, which will create an incident alert. 

![mstsc_O5tMxYk2aJ](https://user-images.githubusercontent.com/109401839/235330515-667d07f2-929d-48d7-9aa5-314e9a491d13.png)

> We can now go to our Log Analytics and view logs. 
Enter the Query 

```
SigninLogs
| order by TimeGenerated desc
```

> This will show us the script attempts. It makes take a moment to update, but this is what it will look like! 

![vivaldi_vGrHhhyVGj](https://user-images.githubusercontent.com/109401839/235330674-81586064-bce1-494a-907f-61e8721ace29.png)

![lgo](https://user-images.githubusercontent.com/109401839/235330713-a8f42e91-8aef-43d2-a987-0539c660ef3c.PNG)

- Key-Vault-Secret-Reader.ps1
(this can be done manually by observing Key Vault Secrets in Azure Portal)
 
> Replace the name for each part of the script with your corresponding information. Run it and see the alert generate! Now you have an idea, I will just show you the results for the next two.  

![mstsc_X219qf3iEc](https://user-images.githubusercontent.com/109401839/235331049-2d9d46c5-47fa-4c5d-b88e-8723a75573db.png)

![mstsc_GVrwLTrcuz](https://user-images.githubusercontent.com/109401839/235331078-43392219-7009-49dc-8051-e1754fe3b8c4.png)

> This may disconnect you in Azure. This is the Admin attempt. 
 If you are having issues, be sure in lines 6 & 7 to add 

```
Disconnect-AzAccount
Connect-AzAccount
``` 

> That solved the issue for me there. Now sign in, and remember that the attacker roles set in previous labs do not have read rights for Azure Key vault... 

> Next is to stop the VM in Azure, this may or may not sign you out, then run it again so everything can marinate perfectly in our pot. Run the.PS1 Key Vault attack again and voila. 

![mstsc_j9qsWIkbGY](https://user-images.githubusercontent.com/109401839/235331907-8028047d-c4f6-4c2f-9a76-0299cd2e1189.png)

![keyvauilt log](https://user-images.githubusercontent.com/109401839/235332071-a6d51d5f-f62a-4022-8f26-a5b408fa6b26.PNG)

> Above we can see that our attempt is successful, and we know it is us by the same IP Address of the VM. For my instance, I was the only one who got into the Key Vault, maybe an outside threat got into yours. You can check the logs and verify, however, we should have an incident alert for all these attempts I did. 
 
![vivaldi_VozPgPs7jQ](https://user-images.githubusercontent.com/109401839/235332143-d88c13a6-97d9-4461-bbed-0fd14fb19aa9.png)

> Here is the alert. 

![vivaldi_msbQ1nQ0D3](https://user-images.githubusercontent.com/109401839/235332230-ad1f9593-4753-4640-bdf7-da33b76f7978.png)

- Malware-Generator-EICAR.ps1
(this can be done manually by creating a text file with the EICAR string in it)

> Run this in Powershell and it will create a Windows Security Alert. Alternatively, you can make a .txt file and combine the two parts of the script and save it to trigger the alert. 

![mstsc_UnFJHU7CGl](https://user-images.githubusercontent.com/109401839/235332812-697bc84c-5e57-4992-b362-d5a4ddfba704.png)

> The script essentially just combines it for us but we can do this manually 

![mstsc_2zVfAJvwpd](https://user-images.githubusercontent.com/109401839/235332785-38c9111b-b35e-4d8f-afe6-567261c2b45b.png)

> For this part, we will use Powershell ISE (Admin) and enter the .ps1 code. Windows security should catch these. 

![vivaldi_c6nIFdtzdJ](https://user-images.githubusercontent.com/109401839/235333107-b844ca39-112e-4f29-87cd-f470b3cf1ce0.png)

> We should see this generated in Defender For Cloud and Sentinel. In Sentinel, it will only show if Windows Security took action! So, depending on the setting. You have to manually take action if it is quarantined. After that is fixed, take a moment (For me a very long time) and wait for the incident or KQL query to view the incident. 

- SQL-Brute-Force-Simulator.ps1
(this can be done manually with SSMS by attempting to log in with bad credentials)


``` Note: It does take a bit of time for the logs to show up in Log Analytics Workspace! "Patience is beautiful." ```

- If you want to trigger Brute Force attempts for Linux and RDP, simply fail to log into these several times (10+), but I assume the internet is doing a good job of that already based on our previous lab, haha. 

### Run Insecure Environment for 24 Hours and Capture Analytics
<details close>

<div>

</summary>

### Dataset 

Before 24 Hours: 
<div>

| Metric                   | Count
| ------------------------ | -----
| SecurityEvent            | 39046
| Syslog                   | 782
| SecurityAlert            | 0
| SecurityIncident         | 222
| AzureNetworkAnalytics_CL | 1350

![Windows RDP   SMB Authentication Failure(Before)](https://user-images.githubusercontent.com/109401839/235335964-ef063912-f0b7-4761-a95b-911c21f240b7.png)

![Linux SSH Auth Failure (Before)](https://user-images.githubusercontent.com/109401839/235335965-63e57ce1-2d54-4256-a86c-4e7962eda71e.png)

![MySQL Authentication Failures(Before)](https://user-images.githubusercontent.com/109401839/235335966-25b63a64-750c-4275-9f54-a5ec72bd0a7c.png)

![nsg-malicious-allowed-in (before)](https://user-images.githubusercontent.com/109401839/235335967-faab4541-ea6c-4276-8b17-1b446613ff9f.png)

HELPER QUERIES	
		
	Helper KQL Queries
		
Start Time	

``` 
"range x from 1 to 1 step 1
| project StartTime = ago(24h), StopTime = now()"
 ``` 
	
![vivaldi_TqMaMGLc0s](https://user-images.githubusercontent.com/109401839/235334642-729e7798-48b3-43ea-870b-85ed6425f3c1.png)
	
Stop Time			
Security Events (Windows VMs)	"SecurityEvent
| where TimeGenerated >= ago(24h)
| count"

		
Syslog (Linux VMs)	"Syslog
| where TimeGenerated >= ago(24h)
| count"	

	
SecurityAlert (Microsoft Defender for Cloud)	"SecurityAlert
| where DisplayName !startswith ""CUSTOM"" and DisplayName !startswith ""TEST""
| where TimeGenerated >= ago(24h)
| count"
		
Security Incident (Sentinel Incidents)	"SecurityIncident
| where TimeGenerated >= ago(24h)
| count"	

	
NSG Inbound Malicious Flows Allowed	"AzureNetworkAnalytics_CL 
| where FlowType_s == ""MaliciousFlow"" and AllowedInFlows_d > 0
| where TimeGenerated >= ago(24h)
| count"

	
NSG Inbound Malicious Flows Blocked	"AzureNetworkAnalytics_CL 
| where FlowType_s == ""MaliciousFlow"" and DeniedInFlows_d > 0
| where TimeGenerated >= ago(24h)
| count"		

![image](https://user-images.githubusercontent.com/109401839/235336299-df51515e-aea1-424d-a880-572722e5627b.png)

### Incident Response & System Hardening

<div>

</summary>

| Check your Subscription’s Cost Analysis

As you work an incident, I would recommend taking notes between each step.

 - Work the incidents being generated within Azure Sentinel, in accordance with the NIST 800-61 Incident Management Lifecycle. Make use of the provided Pl.

- Step 1: Preparation
(We initiated this already by ingesting all of the logs into Log Analytics Workspace and Sentinel and configuring alert rules)

- Step 2: Detection & Analysis (You may have different alerts/incidents)
Set Severity, Status, Owner
View Full Details (New Experience)
Observe the Activity Log (for history of incident)
Observe Entities and Incident Timelines (are they doing anything else?)
“Investigate” the incident and continue trying to determine the scope
Inspect the entities and see if there are any related events
Determine legitimacy of the incident (True Positive, False Positive, etc.)
If True Positive, continue, if False positive, close it out.

- Step 3: Containment, Eradication, and Recovery
Use the simple Incident Response PlayBook

- Step 4: Document Findings/Info and Close out the Incident in Sentinel

Incident 1 - Brute Force Success (Windows) - Working Incidents and Incident Response
<details close>

<div>

</summary>

- Set Severity, Status, Owner

![vivaldi_cuZM38TCe3](https://user-images.githubusercontent.com/109401839/235336573-c38e5325-e4df-4aad-93f8-b04487099a32.png)

- View Full Details (New Experience)

![c5qFJgKgq8](https://user-images.githubusercontent.com/109401839/235336592-2ec5579f-aa33-42f3-9e80-ce549f1b5da6.png)

- Observe the Activity Log (for history of incident)

![vivaldi_8f1Oj6rUd5](https://user-images.githubusercontent.com/109401839/235336637-50bf9a05-b3a5-4266-b009-866991f902de.png)

- Observe Entities and Incident Timelines

![vivaldi_OEaYg3xMGs](https://user-images.githubusercontent.com/109401839/235336701-eca2ef8d-4302-45df-952d-c92d167f082c.png)

If we click this IP Address, we can see their Geo Data. 

![vivaldi_iL5aNXLtVZ](https://user-images.githubusercontent.com/109401839/235336728-c55a52dc-df04-43ac-ab5f-e22bf65265d8.png)

- Investigate & Determine The Scope

![vivaldi_KhX7Mked3T](https://user-images.githubusercontent.com/109401839/235336764-4da5f6ad-5274-4c32-978d-ca5697cb52b2.png)

If we see related alerts based on this attacker we can see what else they have done in correlation to their IP Address. They are related to 41 other events. 

This attacker is related to +26 attempted Brute Force Attacks and over 14 successful Brute Force Attacks. 

![vivaldi_R4miIRFQH2](https://user-images.githubusercontent.com/109401839/235336831-6618b357-320c-4702-918a-7c9f4bbe5ad0.png)

![vivaldi_jzhkTzBq9b](https://user-images.githubusercontent.com/109401839/235336876-f16e6504-adf3-4360-8689-7babb4df3b5e.png)

We can see mroe data if view "All Aggregated Nodes" in KQL

![vivaldi_V7drXD6QZu](https://user-images.githubusercontent.com/109401839/235336905-1323b6df-4223-4b45-a59b-755220a9de9e.png)

We can see this information in KQL. 

```
let GetIPRelatedAlerts = (v_IP_Address: string) {
    SecurityAlert
    | summarize arg_max(TimeGenerated, *) by SystemAlertId
    | extend entities = todynamic(Entities)
    | mv-expand entities
    | project-rename entity=entities
    | where entity['Type'] == 'ip' and entity['Address'] =~ v_IP_Address
    | project-away entity
};
GetIPRelatedAlerts(@'110.167.169.106')
```

- Now Determine the legitimacy of the incident, True Postive or False Positive, etc. 

```

// Brute Force Success Windows
let FailedLogons = SecurityEvent
| where EventID == 4625 and LogonType == 3
| where TimeGenerated > ago(60m)
| summarize FailureCount = count() by AttackerIP = IpAddress, EventID, Activity, LogonType, DestinationHostName = Computer
| where FailureCount >= 5;
let SuccessfulLogons = SecurityEvent
| where EventID == 4624 and LogonType == 3
| where TimeGenerated > ago(60m)
| summarize SuccessfulCount = count() by AttackerIP = IpAddress, LogonType, DestinationHostName = Computer, AuthenticationSuccessTime = TimeGenerated;
SuccessfulLogons
| join kind = leftouter FailedLogons on DestinationHostName, AttackerIP, LogonType
| project AuthenticationSuccessTime, AttackerIP, DestinationHostName, FailureCount, SuccessfulCount

```
Via [Cheat Sheet](https://github.com/fnabeel/Cloud-SOC-Project-Directory/blob/main/KQL-Query-Cheat-Sheet%20(1).md) 

> We will add a clause to see entities that have had successful log ons in the last 24 hours. 

```
SecurityEvent
| where EventID == 4625
| distinct Account
``` 
![vivaldi_dnJSoEyZme](https://user-images.githubusercontent.com/109401839/235337183-cde0f5f1-eec4-4631-b597-6970c06b9a25.png)

We can further specify by using the IP Address of the attacker. 

```
| where ipaddress == "110.167.169.106"
```

and remove: 

``` | distinct Account ```

![vivaldi_JRZZok9EsC](https://user-images.githubusercontent.com/109401839/235337271-a832ca24-7dbd-443c-a2f6-70df71664de2.png)

Based on the results, I willl conclude this to be a False Positive. 

You maybe wondering why? 
It is because even after these "successful" attempts, we can see they kept trying to bruteforce in. In addition, if we filter the activity, there is not any actual successful login attempts. We inspected the action from this IP Address, and the main issue is the persistence of this Threat Actor. With enough time, they could breach into the system.

-   If true positive, continue. If false-positive, close. 

Since it is a false positive, but the network security is bad. We will close this out but continue this by hardening our systems so this sort of incident is reduced greatly. 

Next:  Containment, Eradication, and Recovery.

Let us refer to the Incident Response Playbook. 

" 
### Incident Description
<div>
This incident involves observation of potential brute force attempts against a Windows VM.

### Initial Response Actions
<div>

- Verify the authenticity of the alert or report

- Immediately isolate the machine and change the password of the affected user.

- Identify the origin of the attacks and determine if they are attacking or involved with anything else.

- Determine how and when the attack occurred
Are the NSGs not being locked down? If so, check other NSGs

- Assess the potential impact of the incident.

- What type of account was it? Permissions?

### Containment and Recovery
<div>

- Lock down the NSG assigned to that VM/Subnet, either entirely, or to allow only necessary traffic

- Reset the affected user’s password

- Enable MFA

### Document Findings and Close out Incident
"

 ![hardening ip](https://user-images.githubusercontent.com/109401839/235338083-2806e873-8855-464d-8ec0-fb7706bd1508.PNG)

So we will make the only IP address that can access this VM is our own + /32 <- which means only the specified IP Address.

![vivaldi_CoLvEd6nF3](https://user-images.githubusercontent.com/109401839/235338143-bf9b40b1-79ee-460a-94a7-bc177e2d48d2.png)

We can delete this RDP rule from earlier labs. 

So now there is not a chance they can brute force.

We will do this for all out VM. 


### Incident 2 - Possible Privilege Escalation - Working Incidents and Incident Response
<details close>

<div>

</summary>

We will do the samething again. 

![possible esdc](https://user-images.githubusercontent.com/109401839/235338529-973af8de-1de3-4dec-b6db-ca0c81d30ce0.PNG)

This has 525 Events and 25 alerts.

This was from our Powershell script I left running. We know it is a false positive since it came from my virtual machine by the matching IP address. However, if this is a real incident. We have to investigate something that is generating so many alerts. 

![vivaldi_H4U6CQUlEx](https://user-images.githubusercontent.com/109401839/235338626-7d6c3450-24c8-4821-90e3-5b2e2dbefc27.png)

Since this is within the organisation, I would just call the user and confirm the details with them. Lets pretend the user was just doing normal duties is a pentester, and corobrated with their manager to conduct this. Then we can just close it. False Positive - Inaccurate Data. 

![vivaldi_FTRBwqoRdM](https://user-images.githubusercontent.com/109401839/235338746-d2c7a33f-d1ac-4cd0-ac3d-6b032e2445cc.png)

So far I closed 3 Incidents, 1 Brute Force, 1 Permission Escalating , 1 Duplicate of the Brute force. 

![vivaldi_MjJTET0DBT](https://user-images.githubusercontent.com/109401839/235338870-1c478632-83f8-4777-b593-cb21196276b6.png)

### Incident 3 - Brute Force Success (Linux) - Microsoft Sentinel Working Incidents and Incident Response
<details close>

<div>

</summary>

In my lab, I did not have any successful Linux brute force, but we do have attempts. 

![vivaldi_mEYswyeMRa](https://user-images.githubusercontent.com/109401839/235338903-0c6a9c81-82ea-4838-96d3-f6dfb699aa1f.png)

![vivaldi_aRwcdARuEr](https://user-images.githubusercontent.com/109401839/235338914-a1daed59-f86f-4106-882e-fd8d22626e16.png)

![vivaldi_eKo6RDjcN3](https://user-images.githubusercontent.com/109401839/235338939-aabf588d-120c-410e-b21d-eba1e47ad97b.png)

We can use this KQL query to confirm if they actually Brute Force in or not to do our due diligence. 

![vivaldi_oWXidzLFP1](https://user-images.githubusercontent.com/109401839/235338986-b81f3604-1aaf-4534-aaf6-357e6b638bb8.png)

We did not, we can close this as a Benign- True Positive because there was an attempt, no successful brute forces. We can specify further by grabbing each IP Address and customising the query. First lets get more info. 

This would be good for example, 10,000 IP Addresses in an organisation was attempting to brute force and we wanted to narrow it down to just 1 IP. 

We can reset the passwords. 

![vivaldi_tQnuejPL1A](https://user-images.githubusercontent.com/109401839/235339178-8710f60a-838c-4773-b271-49038fb9bae3.png)

- Refering to the playbook, lets see if they are related to any other event. 

> They are, we remediated this by reseting password of compromsied user viritual machine and locked down NSG. 

Now we can close it as a Benign- True Positive. Closed.

- Impact of Incident

> Account was a non admin account on a linux virtual machine, possibly low impact, however attacker is invovled in many other incidents. These wil be remediated by NSG hardening. 

### Incident 4 - Possible Malware Outbreak - Working Incidents and Incident Response
<details close>

<div>

</summary>

![vivaldi_cmkHl8ibDk](https://user-images.githubusercontent.com/109401839/235339661-ed54b589-0d13-440e-9f8d-d1901c8076dd.png)

![vivaldi_iK4n16GqXA](https://user-images.githubusercontent.com/109401839/235339714-28549a49-b758-40a7-badf-cb90fcd73602.png)

![vivaldi_2ggFSrbzOX](https://user-images.githubusercontent.com/109401839/235339755-a413874f-da99-4781-a076-3cc49bb7a7d8.png)

Here do not know if the extended alerts are actually related to the incident. In thsi case malware, but it can be as typically with a breach, threat actors drop malware in as well. 

> Note: Several other alerts raised. 

We can examine the query that generated this alert. 

![vivaldi_ulG9cGZsXz](https://user-images.githubusercontent.com/109401839/235339859-2eb3d7c1-55a5-4a16-b396-1f1a0d405e3e.png)

This can be filtered by comprised entity category in KQL. 

![vivaldi_7ytY4TuYHb](https://user-images.githubusercontent.com/109401839/235339840-376912f2-8e7f-4cf3-a4ee-8bd6ba4fb9a7.png)

We can add another query to see if there is no action necessary and if the malware was remediated. 

![vivaldi_7aC88zFKiR](https://user-images.githubusercontent.com/109401839/235339918-c3fdaba0-4dc6-427a-a342-dd469a384561.png)

Which looks like it was automatically remidiated. 

We can do our due diligence and make sure by viewing the the file path. 

![vivaldi_8tIZy1xL5Q](https://user-images.githubusercontent.com/109401839/235339965-2fd9de11-2b8e-4011-8a8b-47ccd9708971.png)

It is benign true positive. 

![vivaldi_EPWAjpIU5D](https://user-images.githubusercontent.com/109401839/235340033-f65d3618-a31a-4d8f-810a-3bf5f076cffc.png)

That is it for the SIEM labs, I will mass close the tickets as Benign Positive - Suspicious but expected. 

![vivaldi_pL3PCdQkUO](https://user-images.githubusercontent.com/109401839/235340122-ae0340b3-58bb-482b-9871-0afb6e7cc5af.png)

Next part, we will harden the environment after 24 hours and document it. 

Now lets wait 24 hours. 

![vivaldi_Vbe3M5A01o](https://user-images.githubusercontent.com/109401839/235340150-0b193cd6-dbb7-4c01-b256-e5fc26c0e267.png)

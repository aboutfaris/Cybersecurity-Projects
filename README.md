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

> Set up IP Entity | Address | AttackerIP

- Add new entity:

> Set up Host | Hostname | DestinationHostName 

![vivaldi_G4GbbxRRLc](https://user-images.githubusercontent.com/109401839/235292538-96a1b891-dbf7-4466-8234-bf9eb3aa1dfb.png)

> So say that an attacker with an IP address 1.1.1.1 attacks our network, we will get an alert.. however Sentinel will track that IP Address and correlate that addresses further action and map it to other alerts. 

![vivaldi_qZYMU18mjY](https://user-images.githubusercontent.com/109401839/235292695-ed06b0e7-18c4-4dd4-8f33-44199cee9674.png)

 ![vivaldi_5FJZt75Ouo](https://user-images.githubusercontent.com/109401839/235292727-848a05fb-234b-4a61-9d11-9ce4b35af5c6.png)

Our rule is ready to roll ~ validate & create. 

We should see any incidents that it creates.

And almost immediately we got an incident! 

![vivaldi_NgGrQCTZd8](https://user-images.githubusercontent.com/109401839/235292787-85b9164a-c584-4e35-b013-527551daae27.png)

![4MDWsCNOfs](https://user-images.githubusercontent.com/109401839/235292805-0fac1e01-6461-471b-98e6-c98ead18fdbe.png)


On the bottom left, we can click "Investigation"  and it will show us a nice infographic of the attack to the host. 

![FZIXPOncAT](https://user-images.githubusercontent.com/109401839/235293224-ad6cf8a4-3069-42b0-b83b-a20adf271e6d.png)

- Now, we can delete that test incident alert and the test alert, we are going to import a bunch of the real queries.  

> If this portion did not work for you, as in the query did not result in any incidents. You can remote into your VM and purposely fail the login attempt 10x in order to generate the incident ! 

- Now download the query rule list to make life easier ! 

---

[Sentinel Analytics Rules](https://github.com/fnabeel/Cloud-SOC-Project-Directory/blob/main/Sentinel-Analytics-Rules/Sentinel-Analytics-Rules(KQL%20Alert%20Queries).json)

---

> After importing the rules, we already have 4 incidents generated. Nothing like work. 

![vivaldi_AhVZHFFOyF](https://user-images.githubusercontent.com/109401839/235294286-eead3162-d19f-475f-a07b-aedd23433dec.png)

Here is the active rules imported: 

![vivaldi_0qjWA3CiOA](https://user-images.githubusercontent.com/109401839/235294313-140f164c-e698-4425-9925-b238cf73b4ca.png)

- Play around and learn each part.

For example: CUSTOM: Possible Privilege Escalation (Global Admin Role Assignment)

Under Set Rule Logic we can see the Rule Query. 

We can break down this query: 

```
AuditLogs
| where OperationName == "Add member to role" and Result == "success"
| where TargetResources[0].modifiedProperties[1].newValue == '"Company Administrator"' and TargetResources[0].type == "User"
| project TimeGenerated, OperationName, AssignedRole = TargetResources[0].modifiedProperties[1].newValue, InitiatorId = InitiatedBy.user.id, InitiatorUpn = InitiatedBy.user.userPrincipalName, TargetAccountId = TargetResources[0].id, TargetAccountUpn = TargetResources[0].userPrincipalName, InitiatorIpAddress = InitiatedBy.user.ipAddress, Status = Result
```
---

Here is a breakdown of each line:

AuditLogs: This is the name of the table being queried. It likely contains logs of actions taken within a Microsoft Azure environment.

| where OperationName == "Add member to role" and Result == "success": This line filters the results to only show entries where the operation name is "Add member to role" and the result was "success". This is likely used to narrow down the results to only show successful attempts to add a user to a role.

| where TargetResources[0].modifiedProperties[1].newValue == '"Company Administrator"' and TargetResources[0].type == "User": This line further filters the results to only show entries where the modified property at index 1 of the first TargetResource (a resource involved in the operation) is equal to the string "Company Administrator" and the type of the first TargetResource is "User". This is likely used to only show successful attempts to add a user to the "Company Administrator" role.

| project TimeGenerated, OperationName, AssignedRole = TargetResources[0].modifiedProperties[1].newValue, InitiatorId = InitiatedBy.user.id, InitiatorUpn = InitiatedBy.user.userPrincipalName, TargetAccountId = TargetResources[0].id, TargetAccountUpn = TargetResources[0].userPrincipalName, InitiatorIpAddress = InitiatedBy.user.ipAddress, Status = Result: This line projects (i.e., selects) specific columns from the filtered results and renames them for readability. 

The selected columns include the time the log was generated (TimeGenerated), the operation name (OperationName), the assigned role (AssignedRole, which is the value of the modified property at index 1 of the first TargetResource), the ID of the user who initiated the operation (InitiatorId), the user principal name of the user who initiated the operation (InitiatorUpn), the ID of the target account (TargetAccountId, which is the ID of the first TargetResource), the user principal name of the target account (TargetAccountUpn, which is the user principal name of the first TargetResource), the IP address of the user who initiated the operation (InitiatorIpAddress, which is the IP address of the user who initiated the operation), and the status of the operation (Status, which is the result of the operation).


- Lets see what happened while you was reading this and I was typing this out. 

![Frq11TIXzC](https://user-images.githubusercontent.com/109401839/235294920-a287141b-00b4-4005-9c3d-4be26dffd13d.png)

We got a brute force attempt on MS SQL Server.

Similar incidents are notified at the bottom. 

Lets investigate:

![vivaldi_K8gJz7V9DX](https://user-images.githubusercontent.com/109401839/235294982-8e539741-227f-469d-b3c1-d31454a8d533.png)

This is the spiral of despair..

Lets revist the workbooks since these are relatively new and should reflect on the geolocation map within the timeframe of the attacks. 

![vivaldi_sbJlTVzF7M](https://user-images.githubusercontent.com/109401839/235295157-7cba01ca-2c81-4c49-b03d-7cab1c81fb77.png)

In the last 30 minutes, 

![image](https://user-images.githubusercontent.com/109401839/235295217-06574230-fcb2-408e-b415-428896d83fe9.png)

The entities show us the IP Address information. 


### Attack Traffic Generation Lab
<details close>

<div>

</summary>

#### Attacker Mode (pretend you are an attacker), perhaps a world renown Blackhat Hacker, lets cosplay this lab:

- First, lets generate some attack traffic to trigger alerts & incident generation, which the Internet (Thank you) have already done since the writing of the last lab. 

![vivaldi_BAtjUMJqrd](https://user-images.githubusercontent.com/109401839/235329080-bd59d747-8ef9-4947-8d91-5bf6d80dbf79.png)

> 73 Open Incidents. 2 High Alerts, oh boy. Lets make it 74.

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

 > Trust the authors, you are the author. Maybe.. 

| Notice: You can do what these scripts do manually, however it is good to get some experience using scripts to be more efficient with time and versatile. If you are unsure what each line in the script does, feel free to copy and paste into ChatGPT. Then, request it to explain each line at XYZ age group so you can dissect, marinate that knowledge and then be able to comprehend further. All in due time, right? 

> VSC may ask you to install an extension for powershell, go ahead and install it. Now...

- Run each of the following scripts, observing the results in Log Analytics Workspace AND Sentinel Incident Creation:

- AAD-Brute-Force-Success-Simulator.ps1
(this can be done manually by trying to log into the portal)

Lets break down the main function for this on: 

``` 
Line 1: $tenantId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" 

# Your Tenant ID, you can find on the AAD Blade in the Azure Portal..

Line 2: $username = "attacker@[your user name].onmicrosoft.com"

# Some Username that exists in your AAD Tenant.. in my case that is "attacker@fnabeelpm.onmicrosoft.com"

Line 3: $correct_password = "LabTest12345" 

# Enter the correct password for the above user.. If you can nto remember your password, you can reset it in  your broswer incognito mode and sign-on into Azure AD.

Line 4: $wrong_password = "___WRONG PASSWORD___"

# This is used to generate auth failures..

Line 5: $max_attempts = 11 

# This is the number of times to fail the login before succeeding. 

```

> So, we will let this run and it will create a loop for 11x failed login attempts, and then 1 successful login attempts, which will create an incident alert. 

![mstsc_O5tMxYk2aJ](https://user-images.githubusercontent.com/109401839/235330515-667d07f2-929d-48d7-9aa5-314e9a491d13.png)

> We can now go to out Log Analytics and view logs. 
Enter the Query 
```
SigninLogs
| order by TimeGenerated desc
```

This will show us the script attempts. It make take a moment to update, but this is what it will look like ! 

![vivaldi_vGrHhhyVGj](https://user-images.githubusercontent.com/109401839/235330674-81586064-bce1-494a-907f-61e8721ace29.png)

![lgo](https://user-images.githubusercontent.com/109401839/235330713-a8f42e91-8aef-43d2-a987-0539c660ef3c.PNG)

- Key-Vault-Secret-Reader.ps1
(this can be done manually by observing Key Vault Secrets in Azure Portal)
 
> Replace the name for each part of the script to your corresponding information. Run it and see the alert generate ! Now you have an idea, I will just show you the results for the next two.  

![mstsc_X219qf3iEc](https://user-images.githubusercontent.com/109401839/235331049-2d9d46c5-47fa-4c5d-b88e-8723a75573db.png)

![mstsc_GVrwLTrcuz](https://user-images.githubusercontent.com/109401839/235331078-43392219-7009-49dc-8051-e1754fe3b8c4.png)

> This may disconnect you in Azure. This is the Admin attempt. 
 If you are having issues, be sure in line 6 & 7 to add 
```
Disconnect-AzAccount
Connect-AzAccount
``` 
That solved the issue for me there. Now sign in, remember that the attacker roles set in previous labs do not have read rights for Azure Key vault.. 

> Next is to stop the VM in Azure, this may or may not sign you out, then run it again so everything cna marinate perfectly in our pot. Run the .PS1 Key Vault attack again and voila. 

![mstsc_j9qsWIkbGY](https://user-images.githubusercontent.com/109401839/235331907-8028047d-c4f6-4c2f-9a76-0299cd2e1189.png)

![keyvauilt log](https://user-images.githubusercontent.com/109401839/235332071-a6d51d5f-f62a-4022-8f26-a5b408fa6b26.PNG)


> Above we can see that our attempt is successful, and we know it is us by the same IP Address of the VM. For my instance, I was the only one who got into the Key Vault, maybe an outside threat got into yours. You can check the logs and verify, however we should have an incident alert for all these attempts I did. 
 
![vivaldi_VozPgPs7jQ](https://user-images.githubusercontent.com/109401839/235332143-d88c13a6-97d9-4461-bbed-0fd14fb19aa9.png)

> Here is the alert. 

![vivaldi_msbQ1nQ0D3](https://user-images.githubusercontent.com/109401839/235332230-ad1f9593-4753-4640-bdf7-da33b76f7978.png)

- Malware-Generator-EICAR.ps1
(this can be done manually by creating a text file with the EICAR string in it)

> Run this in powershell and it will create a Windows Security Alert. Alernatively, you can make a .txt file and combine the two parts of the script and save it to trigger the alert. 

![mstsc_UnFJHU7CGl](https://user-images.githubusercontent.com/109401839/235332812-697bc84c-5e57-4992-b362-d5a4ddfba704.png)

> The script essentially just combines it for us but we can do this manually 

![mstsc_2zVfAJvwpd](https://user-images.githubusercontent.com/109401839/235332785-38c9111b-b35e-4d8f-afe6-567261c2b45b.png)

> For this part, we will use Powershell ISE (Admin) and enter the .ps1 code. Windows security should catch these. 

![vivaldi_c6nIFdtzdJ](https://user-images.githubusercontent.com/109401839/235333107-b844ca39-112e-4f29-87cd-f470b3cf1ce0.png)

> We should see this generated in 365 For Cloud and Sentinel. In Sentinel, it will only show if Windows Security took action! So, depending on the setting. You have to manually take action if it is quarantined. After that is fixed, take a moment andwait for the incident or KQL query to view the incident. 

- SQL-Brute-Force-Simulator.ps1
(this can be done manually with SSMS by attempting to login with bad credentials)


``` Note: It does take a bit of time for the logs to show up in Log Analytics Workspace! "Patience is beautiful." ```

- If you want to trigger Brute Force attempts for Linux and RDP, simply fail logging into these several times (10+), but I assume the internet is doing a good job of that already based on our previous lab, haha. 




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
``` 
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "workspace": {
            "type": "String"
        }
    },
    "resources": [
        {
            "id": "[concat(resourceId('Microsoft.OperationalInsights/workspaces/providers', parameters('workspace'), 'Microsoft.SecurityInsights'),'/alertRules/62680e5a-d24e-4537-a28f-f6e90125c7bb')]",
            "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/62680e5a-d24e-4537-a28f-f6e90125c7bb')]",
            "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
            "kind": "Scheduled",
            "apiVersion": "2022-09-01-preview",
            "properties": {
                "displayName": "CUSTOM: Possible Privilege Escalation (Global Admin Role Assignment)",
                "description": "",
                "severity": "High",
                "enabled": true,
                "query": "AuditLogs\n| where OperationName == \"Add member to role\" and Result == \"success\"\n| where TargetResources[0].modifiedProperties[1].newValue == '\"Company Administrator\"' and TargetResources[0].type == \"User\"\n| project TimeGenerated, OperationName, AssignedRole = TargetResources[0].modifiedProperties[1].newValue, InitiatorId = InitiatedBy.user.id, InitiatorUpn = InitiatedBy.user.userPrincipalName, TargetAccountId = TargetResources[0].id, TargetAccountUpn = TargetResources[0].userPrincipalName, InitiatorIpAddress = InitiatedBy.user.ipAddress, Status = Result\n",
                "queryFrequency": "PT10M",
                "queryPeriod": "PT5H",
                "triggerOperator": "GreaterThan",
                "triggerThreshold": 0,
                "suppressionDuration": "PT5H",
                "suppressionEnabled": false,
                "startTimeUtc": null,
                "tactics": [
                    "PrivilegeEscalation"
                ],
                "techniques": [
                    "T1548",
                    "T1546",
                    "T1078",
                    "T0890"
                ],
                "alertRuleTemplateName": null,
                "incidentConfiguration": {
                    "createIncident": true,
                    "groupingConfiguration": {
                        "enabled": true,
                        "reopenClosedIncident": false,
                        "lookbackDuration": "PT1H",
                        "matchingMethod": "AllEntities",
                        "groupByEntities": [],
                        "groupByAlertDetails": [],
                        "groupByCustomDetails": []
                    }
                },
                "eventGroupingSettings": {
                    "aggregationKind": "AlertPerResult"
                },
                "alertDetailsOverride": null,
                "customDetails": null,
                "entityMappings": [
                    {
                        "entityType": "Account",
                        "fieldMappings": [
                            {
                                "identifier": "AadUserId",
                                "columnName": "InitiatorId"
                            }
                        ]
                    },
                    {
                        "entityType": "Account",
                        "fieldMappings": [
                            {
                                "identifier": "AadUserId",
                                "columnName": "TargetAccountId"
                            }
                        ]
                    },
                    {
                        "entityType": "IP",
                        "fieldMappings": [
                            {
                                "identifier": "Address",
                                "columnName": "InitiatorIpAddress"
                            }
                        ]
                    }
                ],
                "sentinelEntitiesMappings": null,
                "templateVersion": null
            }
        },
        {
            "id": "[concat(resourceId('Microsoft.OperationalInsights/workspaces/providers', parameters('workspace'), 'Microsoft.SecurityInsights'),'/alertRules/2ba75994-1fbe-4ec0-b312-015b47e10576')]",
            "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/2ba75994-1fbe-4ec0-b312-015b47e10576')]",
            "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
            "kind": "Scheduled",
            "apiVersion": "2022-09-01-preview",
            "properties": {
                "displayName": "CUSTOM: Brute Force ATTEMPT - Azure Key Vault",
                "description": "",
                "severity": "Medium",
                "enabled": true,
                "query": "// Failed access attempts\nAzureDiagnostics\n| where ResourceProvider == \"MICROSOFT.KEYVAULT\" \n| where ResultSignature == \"Forbidden\"\n\n",
                "queryFrequency": "PT5M",
                "queryPeriod": "PT5H",
                "triggerOperator": "GreaterThan",
                "triggerThreshold": 9,
                "suppressionDuration": "PT5H",
                "suppressionEnabled": false,
                "startTimeUtc": null,
                "tactics": [
                    "CredentialAccess"
                ],
                "techniques": [
                    "T1110"
                ],
                "alertRuleTemplateName": null,
                "incidentConfiguration": {
                    "createIncident": true,
                    "groupingConfiguration": {
                        "enabled": true,
                        "reopenClosedIncident": false,
                        "lookbackDuration": "PT5H",
                        "matchingMethod": "AllEntities",
                        "groupByEntities": [],
                        "groupByAlertDetails": [],
                        "groupByCustomDetails": []
                    }
                },
                "eventGroupingSettings": {
                    "aggregationKind": "SingleAlert"
                },
                "alertDetailsOverride": null,
                "customDetails": null,
                "entityMappings": [
                    {
                        "entityType": "IP",
                        "fieldMappings": [
                            {
                                "identifier": "Address",
                                "columnName": "CallerIPAddress"
                            }
                        ]
                    }
                ],
                "sentinelEntitiesMappings": null,
                "templateVersion": null
            }
        },
        {
            "id": "[concat(resourceId('Microsoft.OperationalInsights/workspaces/providers', parameters('workspace'), 'Microsoft.SecurityInsights'),'/alertRules/dbab268c-6906-4e22-a632-8fe263025f2b')]",
            "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/dbab268c-6906-4e22-a632-8fe263025f2b')]",
            "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
            "kind": "Scheduled",
            "apiVersion": "2022-09-01-preview",
            "properties": {
                "displayName": "CUSTOM: Brute Force SUCCESS - Linux Syslog",
                "description": "",
                "severity": "High",
                "enabled": true,
                "query": "// Brute Force Success Linux\nlet FailedLogons = Syslog\n| where Facility == \"auth\" and SyslogMessage startswith \"Failed password for\"\n| where TimeGenerated > ago(1h)\n| project TimeGenerated, SourceIP = extract(@\"\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b\", 0, SyslogMessage), DestinationHostName = HostName, DestinationIP = HostIP, Facility, SyslogMessage, ProcessName, SeverityLevel, Type\n| summarize FailureCount = count() by AttackerIP = SourceIP, DestinationHostName\n| where FailureCount >= 5;\nlet SuccessfulLogons = Syslog\n| where Facility == \"auth\" and SyslogMessage startswith \"Accepted password for\"\n| where TimeGenerated > ago(1h)\n| project TimeGenerated, SourceIP = extract(@\"\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b\", 0, SyslogMessage), DestinationHostName = HostName, DestinationIP = HostIP, Facility, SyslogMessage, ProcessName, SeverityLevel, Type\n| summarize SuccessfulCount = count() by SuccessTime = TimeGenerated, AttackerIP = SourceIP, DestinationHostName\n| where SuccessfulCount >= 1\n| project DestinationHostName, SuccessfulCount, AttackerIP, SuccessTime;\nlet BruteForceSuccesses = SuccessfulLogons \n| join kind = inner FailedLogons on AttackerIP, DestinationHostName;\nBruteForceSuccesses",
                "queryFrequency": "PT59M",
                "queryPeriod": "PT1H",
                "triggerOperator": "GreaterThan",
                "triggerThreshold": 0,
                "suppressionDuration": "PT5H",
                "suppressionEnabled": false,
                "startTimeUtc": null,
                "tactics": [
                    "CredentialAccess"
                ],
                "techniques": [
                    "T1110"
                ],
                "alertRuleTemplateName": null,
                "incidentConfiguration": {
                    "createIncident": true,
                    "groupingConfiguration": {
                        "enabled": true,
                        "reopenClosedIncident": false,
                        "lookbackDuration": "PT1H",
                        "matchingMethod": "AllEntities",
                        "groupByEntities": [],
                        "groupByAlertDetails": [],
                        "groupByCustomDetails": []
                    }
                },
                "eventGroupingSettings": {
                    "aggregationKind": "AlertPerResult"
                },
                "alertDetailsOverride": null,
                "customDetails": null,
                "entityMappings": [
                    {
                        "entityType": "IP",
                        "fieldMappings": [
                            {
                                "identifier": "Address",
                                "columnName": "AttackerIP"
                            }
                        ]
                    },
                    {
                        "entityType": "Host",
                        "fieldMappings": [
                            {
                                "identifier": "HostName",
                                "columnName": "DestinationHostName"
                            }
                        ]
                    }
                ],
                "sentinelEntitiesMappings": null,
                "templateVersion": null
            }
        },
        {
            "id": "[concat(resourceId('Microsoft.OperationalInsights/workspaces/providers', parameters('workspace'), 'Microsoft.SecurityInsights'),'/alertRules/e95fd1bb-b03a-4046-843b-1453a0a95482')]",
            "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/e95fd1bb-b03a-4046-843b-1453a0a95482')]",
            "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
            "kind": "Scheduled",
            "apiVersion": "2022-09-01-preview",
            "properties": {
                "displayName": "CUSTOM: Brute Force SUCCESS - Azure Active Directory",
                "description": "",
                "severity": "High",
                "enabled": true,
                "query": "// Failed AAD logon\nlet FailedLogons = SigninLogs\n| where Status.failureReason == \"Invalid username or password or Invalid on-premise username or password.\"\n| where TimeGenerated > ago(1h)\n| project TimeGenerated, Status = Status.failureReason, UserPrincipalName, UserId, UserDisplayName, AppDisplayName, AttackerIP = IPAddress, IPAddressFromResourceProvider, City = LocationDetails.city, State = LocationDetails.state, Country = LocationDetails.country, Latitude = LocationDetails.geoCoordinates.latitude, Longitude = LocationDetails.geoCoordinates.longitude\n| summarize FailureCount = count() by AttackerIP, UserPrincipalName;\nlet SuccessfulLogons = SigninLogs\n| where Status.errorCode == 0 \n| where TimeGenerated > ago(1h)\n| project TimeGenerated, Status = Status.errorCode, UserPrincipalName, UserId, UserDisplayName, AppDisplayName, AttackerIP = IPAddress, IPAddressFromResourceProvider, City = LocationDetails.city, State = LocationDetails.state, Country = LocationDetails.country, Latitude = LocationDetails.geoCoordinates.latitude, Longitude = LocationDetails.geoCoordinates.longitude\n| summarize SuccessCount = count() by AuthenticationSuccessTime = TimeGenerated, AttackerIP, UserPrincipalName, UserId, UserDisplayName;\nlet BruteForceSuccesses = SuccessfulLogons\n| join kind = inner FailedLogons on AttackerIP, UserPrincipalName;\nBruteForceSuccesses\n| project AttackerIP, TargetAccount = UserPrincipalName, UserId, FailureCount, SuccessCount, AuthenticationSuccessTime",
                "queryFrequency": "PT5M",
                "queryPeriod": "PT5H",
                "triggerOperator": "GreaterThan",
                "triggerThreshold": 0,
                "suppressionDuration": "PT5H",
                "suppressionEnabled": false,
                "startTimeUtc": null,
                "tactics": [],
                "techniques": [],
                "alertRuleTemplateName": null,
                "incidentConfiguration": {
                    "createIncident": true,
                    "groupingConfiguration": {
                        "enabled": true,
                        "reopenClosedIncident": false,
                        "lookbackDuration": "PT5H",
                        "matchingMethod": "AllEntities",
                        "groupByEntities": [],
                        "groupByAlertDetails": [],
                        "groupByCustomDetails": []
                    }
                },
                "eventGroupingSettings": {
                    "aggregationKind": "AlertPerResult"
                },
                "alertDetailsOverride": null,
                "customDetails": null,
                "entityMappings": [
                    {
                        "entityType": "IP",
                        "fieldMappings": [
                            {
                                "identifier": "Address",
                                "columnName": "AttackerIP"
                            }
                        ]
                    },
                    {
                        "entityType": "Account",
                        "fieldMappings": [
                            {
                                "identifier": "AadUserId",
                                "columnName": "UserId"
                            }
                        ]
                    }
                ],
                "sentinelEntitiesMappings": null,
                "templateVersion": null
            }
        },
        {
            "id": "[concat(resourceId('Microsoft.OperationalInsights/workspaces/providers', parameters('workspace'), 'Microsoft.SecurityInsights'),'/alertRules/4891fd6a-75e3-4b43-a5ae-33dbaaf2342e')]",
            "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/4891fd6a-75e3-4b43-a5ae-33dbaaf2342e')]",
            "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
            "kind": "Scheduled",
            "apiVersion": "2022-09-01-preview",
            "properties": {
                "displayName": "CUSTOM: Brute Force ATTEMPT - Azure Active Directory",
                "description": "",
                "severity": "Medium",
                "enabled": true,
                "query": "SigninLogs\n| where ResultDescription == \"Invalid username or password or Invalid on-premise username or password.\"\n| project TimeGenerated, ResultDescription, UserPrincipalName, UserId, AppDisplayName, IPAddress, IPAddressFromResourceProvider, City = LocationDetails.city, State = LocationDetails.state, Country = LocationDetails.country, Latitude = LocationDetails.geoCoordinates.latitude, Longitude = LocationDetails.geoCoordinates.longitude",
                "queryFrequency": "PT10M",
                "queryPeriod": "PT1H",
                "triggerOperator": "GreaterThan",
                "triggerThreshold": 9,
                "suppressionDuration": "PT5H",
                "suppressionEnabled": false,
                "startTimeUtc": null,
                "tactics": [
                    "CredentialAccess"
                ],
                "techniques": [
                    "T1110"
                ],
                "alertRuleTemplateName": null,
                "incidentConfiguration": {
                    "createIncident": true,
                    "groupingConfiguration": {
                        "enabled": true,
                        "reopenClosedIncident": false,
                        "lookbackDuration": "PT1H",
                        "matchingMethod": "AllEntities",
                        "groupByEntities": [],
                        "groupByAlertDetails": [],
                        "groupByCustomDetails": []
                    }
                },
                "eventGroupingSettings": {
                    "aggregationKind": "SingleAlert"
                },
                "alertDetailsOverride": null,
                "customDetails": null,
                "entityMappings": [
                    {
                        "entityType": "Account",
                        "fieldMappings": [
                            {
                                "identifier": "AadUserId",
                                "columnName": "UserId"
                            }
                        ]
                    },
                    {
                        "entityType": "IP",
                        "fieldMappings": [
                            {
                                "identifier": "Address",
                                "columnName": "IPAddress"
                            }
                        ]
                    }
                ],
                "sentinelEntitiesMappings": null,
                "templateVersion": null
            }
        },
        {
            "id": "[concat(resourceId('Microsoft.OperationalInsights/workspaces/providers', parameters('workspace'), 'Microsoft.SecurityInsights'),'/alertRules/5b3b873a-3204-4983-9533-88b4a9c71c2d')]",
            "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/5b3b873a-3204-4983-9533-88b4a9c71c2d')]",
            "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
            "kind": "Scheduled",
            "apiVersion": "2022-09-01-preview",
            "properties": {
                "displayName": "CUSTOM: Brute Force SUCCESS - Windows",
                "description": "If you see a SUCCESS but the Account is \"NT AUTHORITY\\ANONYMOUS LOGON\", check out this article: https://www.inversecos.com/2020/04/successful-4624-anonymous-logons-to.html",
                "severity": "High",
                "enabled": true,
                "query": "// Brute Force Success Windows\nlet FailedLogons = SecurityEvent\n| where EventID == 4625 and LogonType == 3\n| where TimeGenerated > ago(1h)\n| summarize FailureCount = count() by AttackerIP = IpAddress, EventID, Activity, LogonType, DestinationHostName = Computer\n| where FailureCount >= 5;\nlet SuccessfulLogons = SecurityEvent\n| where EventID == 4624 and LogonType == 3\n| where TimeGenerated > ago(1h)\n| summarize SuccessfulCount = count() by AttackerIP = IpAddress, LogonType, DestinationHostName = Computer, AuthenticationSuccessTime = TimeGenerated;\nSuccessfulLogons\n| join kind = inner FailedLogons on DestinationHostName, AttackerIP, LogonType\n| project AuthenticationSuccessTime, AttackerIP, DestinationHostName, FailureCount, SuccessfulCount\n",
                "queryFrequency": "PT59M",
                "queryPeriod": "PT1H",
                "triggerOperator": "GreaterThan",
                "triggerThreshold": 0,
                "suppressionDuration": "PT5H",
                "suppressionEnabled": false,
                "startTimeUtc": null,
                "tactics": [
                    "CredentialAccess"
                ],
                "techniques": [
                    "T1110"
                ],
                "alertRuleTemplateName": null,
                "incidentConfiguration": {
                    "createIncident": true,
                    "groupingConfiguration": {
                        "enabled": true,
                        "reopenClosedIncident": false,
                        "lookbackDuration": "PT1H",
                        "matchingMethod": "AllEntities",
                        "groupByEntities": [],
                        "groupByAlertDetails": [],
                        "groupByCustomDetails": []
                    }
                },
                "eventGroupingSettings": {
                    "aggregationKind": "AlertPerResult"
                },
                "alertDetailsOverride": null,
                "customDetails": null,
                "entityMappings": [
                    {
                        "entityType": "IP",
                        "fieldMappings": [
                            {
                                "identifier": "Address",
                                "columnName": "AttackerIP"
                            }
                        ]
                    },
                    {
                        "entityType": "Host",
                        "fieldMappings": [
                            {
                                "identifier": "HostName",
                                "columnName": "DestinationHostName"
                            }
                        ]
                    }
                ],
                "sentinelEntitiesMappings": null,
                "templateVersion": null
            }
        },
        {
            "id": "[concat(resourceId('Microsoft.OperationalInsights/workspaces/providers', parameters('workspace'), 'Microsoft.SecurityInsights'),'/alertRules/afe7b0a7-d84f-462d-b751-548861bc0c5d')]",
            "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/afe7b0a7-d84f-462d-b751-548861bc0c5d')]",
            "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
            "kind": "Scheduled",
            "apiVersion": "2022-09-01-preview",
            "properties": {
                "displayName": "CUSTOM: Brute Force ATTEMPT - Windows",
                "description": "",
                "severity": "Medium",
                "enabled": true,
                "query": "// Failed logon \nSecurityEvent\n| where EventID == 4625\n| where TimeGenerated > ago(60m)\n| summarize FailureCount = count() by AttackerIP = IpAddress, EventID, Activity, DestinationHostName = Computer\n| where FailureCount >= 10",
                "queryFrequency": "PT15M",
                "queryPeriod": "PT1H",
                "triggerOperator": "GreaterThan",
                "triggerThreshold": 0,
                "suppressionDuration": "PT5H",
                "suppressionEnabled": false,
                "startTimeUtc": null,
                "tactics": [
                    "CredentialAccess"
                ],
                "techniques": [
                    "T1110"
                ],
                "alertRuleTemplateName": null,
                "incidentConfiguration": {
                    "createIncident": true,
                    "groupingConfiguration": {
                        "enabled": true,
                        "reopenClosedIncident": false,
                        "lookbackDuration": "PT5H",
                        "matchingMethod": "AllEntities",
                        "groupByEntities": [],
                        "groupByAlertDetails": [],
                        "groupByCustomDetails": []
                    }
                },
                "eventGroupingSettings": {
                    "aggregationKind": "SingleAlert"
                },
                "alertDetailsOverride": null,
                "customDetails": null,
                "entityMappings": [
                    {
                        "entityType": "IP",
                        "fieldMappings": [
                            {
                                "identifier": "Address",
                                "columnName": "AttackerIP"
                            }
                        ]
                    },
                    {
                        "entityType": "Host",
                        "fieldMappings": [
                            {
                                "identifier": "HostName",
                                "columnName": "DestinationHostName"
                            }
                        ]
                    }
                ],
                "sentinelEntitiesMappings": null,
                "templateVersion": null
            }
        },
        {
            "id": "[concat(resourceId('Microsoft.OperationalInsights/workspaces/providers', parameters('workspace'), 'Microsoft.SecurityInsights'),'/alertRules/c220acf2-b8bb-436d-ad4f-7e3174bbf5a1')]",
            "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/c220acf2-b8bb-436d-ad4f-7e3174bbf5a1')]",
            "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
            "kind": "Scheduled",
            "apiVersion": "2022-09-01-preview",
            "properties": {
                "displayName": "CUSTOM: Possible Privilege Escalation (Azure Key Vault Critical Credential Retrieval or Update)",
                "description": "",
                "severity": "High",
                "enabled": true,
                "query": "// Updating a specific existing password Success\nlet CRITICAL_PASSWORD_NAME = \"Tenant-Global-Admin-Password\";\nAzureDiagnostics\n| where ResourceProvider == \"MICROSOFT.KEYVAULT\" \n| where OperationName == \"SecretGet\" or OperationName == \"SecretSet\"\n| where id_s contains CRITICAL_PASSWORD_NAME",
                "queryFrequency": "PT10M",
                "queryPeriod": "PT5H",
                "triggerOperator": "GreaterThan",
                "triggerThreshold": 0,
                "suppressionDuration": "PT5H",
                "suppressionEnabled": false,
                "startTimeUtc": null,
                "tactics": [
                    "PrivilegeEscalation"
                ],
                "techniques": [],
                "alertRuleTemplateName": null,
                "incidentConfiguration": {
                    "createIncident": true,
                    "groupingConfiguration": {
                        "enabled": true,
                        "reopenClosedIncident": false,
                        "lookbackDuration": "PT5H",
                        "matchingMethod": "AllEntities",
                        "groupByEntities": [],
                        "groupByAlertDetails": [],
                        "groupByCustomDetails": []
                    }
                },
                "eventGroupingSettings": {
                    "aggregationKind": "SingleAlert"
                },
                "alertDetailsOverride": null,
                "customDetails": null,
                "entityMappings": [
                    {
                        "entityType": "IP",
                        "fieldMappings": [
                            {
                                "identifier": "Address",
                                "columnName": "CallerIPAddress"
                            }
                        ]
                    },
                    {
                        "entityType": "Account",
                        "fieldMappings": [
                            {
                                "identifier": "AadUserId",
                                "columnName": "identity_claim_oid_g"
                            }
                        ]
                    }
                ],
                "sentinelEntitiesMappings": null,
                "templateVersion": null
            }
        },
        {
            "id": "[concat(resourceId('Microsoft.OperationalInsights/workspaces/providers', parameters('workspace'), 'Microsoft.SecurityInsights'),'/alertRules/cf0df627-c9ba-4fa7-858d-265cd5cd3548')]",
            "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/cf0df627-c9ba-4fa7-858d-265cd5cd3548')]",
            "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
            "kind": "Scheduled",
            "apiVersion": "2022-09-01-preview",
            "properties": {
                "displayName": "CUSTOM: Brute Force ATTEMPT - Linux Syslog",
                "description": "",
                "severity": "Medium",
                "enabled": true,
                "query": "// Brute Force Success Linux\nlet IpAddress_REGEX_PATTERN = @\"\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b\";\nSyslog\n| where Facility == \"auth\" and SyslogMessage startswith \"Failed password for\"\n| where TimeGenerated > ago(1h)\n| project TimeGenerated, AttackerIP = extract(IpAddress_REGEX_PATTERN, 0, SyslogMessage), DestinationHostName = HostName, DestinationIP = HostIP, Facility, SyslogMessage, ProcessName, SeverityLevel, Type\n| summarize FailureCount = count() by AttackerIP, DestinationHostName, DestinationIP\n| where FailureCount >= 10",
                "queryFrequency": "PT10M",
                "queryPeriod": "PT1H",
                "triggerOperator": "GreaterThan",
                "triggerThreshold": 0,
                "suppressionDuration": "PT5H",
                "suppressionEnabled": false,
                "startTimeUtc": null,
                "tactics": [
                    "CredentialAccess"
                ],
                "techniques": [
                    "T1110"
                ],
                "alertRuleTemplateName": null,
                "incidentConfiguration": {
                    "createIncident": true,
                    "groupingConfiguration": {
                        "enabled": true,
                        "reopenClosedIncident": false,
                        "lookbackDuration": "PT5H",
                        "matchingMethod": "AllEntities",
                        "groupByEntities": [],
                        "groupByAlertDetails": [],
                        "groupByCustomDetails": []
                    }
                },
                "eventGroupingSettings": {
                    "aggregationKind": "SingleAlert"
                },
                "alertDetailsOverride": null,
                "customDetails": null,
                "entityMappings": [
                    {
                        "entityType": "Host",
                        "fieldMappings": [
                            {
                                "identifier": "HostName",
                                "columnName": "DestinationHostName"
                            }
                        ]
                    },
                    {
                        "entityType": "IP",
                        "fieldMappings": [
                            {
                                "identifier": "Address",
                                "columnName": "AttackerIP"
                            }
                        ]
                    }
                ],
                "sentinelEntitiesMappings": null,
                "templateVersion": null
            }
        },
        {
            "id": "[concat(resourceId('Microsoft.OperationalInsights/workspaces/providers', parameters('workspace'), 'Microsoft.SecurityInsights'),'/alertRules/e5450d35-8fd2-47a8-b9cf-e8081d798e8b')]",
            "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/e5450d35-8fd2-47a8-b9cf-e8081d798e8b')]",
            "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
            "kind": "Scheduled",
            "apiVersion": "2022-09-01-preview",
            "properties": {
                "displayName": "CUSTOM: Malware Detected",
                "description": "",
                "severity": "High",
                "enabled": true,
                "query": "SecurityAlert\n| where AlertType == \"AntimalwareActionTaken\"",
                "queryFrequency": "PT10M",
                "queryPeriod": "PT1H",
                "triggerOperator": "GreaterThan",
                "triggerThreshold": 0,
                "suppressionDuration": "PT5H",
                "suppressionEnabled": false,
                "startTimeUtc": null,
                "tactics": [
                    "Collection",
                    "CommandAndControl",
                    "Exfiltration",
                    "Impact"
                ],
                "techniques": [],
                "alertRuleTemplateName": null,
                "incidentConfiguration": {
                    "createIncident": true,
                    "groupingConfiguration": {
                        "enabled": true,
                        "reopenClosedIncident": false,
                        "lookbackDuration": "PT5H",
                        "matchingMethod": "AllEntities",
                        "groupByEntities": [],
                        "groupByAlertDetails": [],
                        "groupByCustomDetails": []
                    }
                },
                "eventGroupingSettings": {
                    "aggregationKind": "SingleAlert"
                },
                "alertDetailsOverride": null,
                "customDetails": null,
                "entityMappings": [
                    {
                        "entityType": "Host",
                        "fieldMappings": [
                            {
                                "identifier": "HostName",
                                "columnName": "CompromisedEntity"
                            }
                        ]
                    }
                ],
                "sentinelEntitiesMappings": null,
                "templateVersion": null
            }
        },
        {
            "id": "[concat(resourceId('Microsoft.OperationalInsights/workspaces/providers', parameters('workspace'), 'Microsoft.SecurityInsights'),'/alertRules/c18a784d-5d2e-47bd-8203-bd4cc09b03d2')]",
            "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/c18a784d-5d2e-47bd-8203-bd4cc09b03d2')]",
            "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
            "kind": "Scheduled",
            "apiVersion": "2022-09-01-preview",
            "properties": {
                "displayName": "CUSTOM: Brute Force ATTEMPT - MS SQL Server",
                "description": "",
                "severity": "Medium",
                "enabled": true,
                "query": "// Brute Force Attempt MS SQL Server\nlet IpAddress_REGEX_PATTERN = @\"\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b\";\nEvent\n| where EventLog == \"Application\"\n| where EventID == 18456\n| where TimeGenerated > ago(1hr)\n| project TimeGenerated, AttackerIP = extract(IpAddress_REGEX_PATTERN, 0, RenderedDescription), DestinationHostName = Computer, RenderedDescription\n| summarize FailureCount = count() by AttackerIP, DestinationHostName\n| where FailureCount >= 10",
                "queryFrequency": "PT10M",
                "queryPeriod": "PT1H",
                "triggerOperator": "GreaterThan",
                "triggerThreshold": 0,
                "suppressionDuration": "PT5H",
                "suppressionEnabled": false,
                "startTimeUtc": null,
                "tactics": [
                    "CredentialAccess"
                ],
                "techniques": [
                    "T1110"
                ],
                "alertRuleTemplateName": null,
                "incidentConfiguration": {
                    "createIncident": true,
                    "groupingConfiguration": {
                        "enabled": true,
                        "reopenClosedIncident": false,
                        "lookbackDuration": "PT5H",
                        "matchingMethod": "AllEntities",
                        "groupByEntities": [],
                        "groupByAlertDetails": [],
                        "groupByCustomDetails": []
                    }
                },
                "eventGroupingSettings": {
                    "aggregationKind": "SingleAlert"
                },
                "alertDetailsOverride": null,
                "customDetails": null,
                "entityMappings": [
                    {
                        "entityType": "Host",
                        "fieldMappings": [
                            {
                                "identifier": "HostName",
                                "columnName": "DestinationHostName"
                            }
                        ]
                    },
                    {
                        "entityType": "IP",
                        "fieldMappings": [
                            {
                                "identifier": "Address",
                                "columnName": "AttackerIP"
                            }
                        ]
                    }
                ],
                "sentinelEntitiesMappings": null,
                "templateVersion": null
            }
        },
        {
            "id": "[concat(resourceId('Microsoft.OperationalInsights/workspaces/providers', parameters('workspace'), 'Microsoft.SecurityInsights'),'/alertRules/b1cafe38-aa17-49a4-ac62-99198caeb3fb')]",
            "name": "[concat(parameters('workspace'),'/Microsoft.SecurityInsights/b1cafe38-aa17-49a4-ac62-99198caeb3fb')]",
            "type": "Microsoft.OperationalInsights/workspaces/providers/alertRules",
            "kind": "Scheduled",
            "apiVersion": "2022-09-01-preview",
            "properties": {
                "displayName": "CUSTOM: Possible Lateral Movement (Excessive Password Resets)",
                "description": "",
                "severity": "Medium",
                "enabled": true,
                "query": "AuditLogs\n| where OperationName startswith \"Change\" or OperationName startswith \"Reset\"\n| order by TimeGenerated\n| summarize count() by tostring(InitiatedBy)\n| project Count = count_, InitiatorId = parse_json(InitiatedBy).user.id, InitiatorUpn = parse_json(InitiatedBy).user.userPrincipalName, InitiatorIpAddress = parse_json(InitiatedBy).user.ipAddress \n| where Count >= 10\n",
                "queryFrequency": "PT5M",
                "queryPeriod": "PT5H",
                "triggerOperator": "GreaterThan",
                "triggerThreshold": 0,
                "suppressionDuration": "PT5H",
                "suppressionEnabled": false,
                "startTimeUtc": null,
                "tactics": [
                    "CredentialAccess",
                    "PrivilegeEscalation"
                ],
                "techniques": [
                    "T1555",
                    "T1078"
                ],
                "alertRuleTemplateName": null,
                "incidentConfiguration": {
                    "createIncident": true,
                    "groupingConfiguration": {
                        "enabled": true,
                        "reopenClosedIncident": false,
                        "lookbackDuration": "PT1H",
                        "matchingMethod": "AllEntities",
                        "groupByEntities": [],
                        "groupByAlertDetails": [],
                        "groupByCustomDetails": []
                    }
                },
                "eventGroupingSettings": {
                    "aggregationKind": "SingleAlert"
                },
                "alertDetailsOverride": null,
                "customDetails": null,
                "entityMappings": [
                    {
                        "entityType": "Account",
                        "fieldMappings": [
                            {
                                "identifier": "AadUserId",
                                "columnName": "InitiatorId"
                            }
                        ]
                    },
                    {
                        "entityType": "IP",
                        "fieldMappings": [
                            {
                                "identifier": "Address",
                                "columnName": "InitiatorIpAddress"
                            }
                        ]
                    }
                ],
                "sentinelEntitiesMappings": null,
                "templateVersion": null
            }
        }
    ]
}

```
---

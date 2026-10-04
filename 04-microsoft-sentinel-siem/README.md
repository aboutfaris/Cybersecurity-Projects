# Microsoft Sentinel SIEM

Turn the lab's Log Analytics workspace into a working SOC: build attack maps, write and import detection rules, generate attack traffic, then work four real incidents end to end using the NIST 800-61 lifecycle.

## What you'll use

- Microsoft Azure, Microsoft Sentinel, Microsoft Defender for Cloud
- Log Analytics workspace (KQL)
- Windows 10 Pro VM (`windows-vm`), Ubuntu VM (`linux-vm`), and a separate `attack-vm`
- PowerShell with the Az module, Visual Studio Code
- Files from [Summary of Cloud SOC Project](../01-cloud-soc-project-summary/): workbook JSON, analytics rules JSON, attack scripts, KQL cheat sheet

## Prerequisites

- The earlier Cloud SOC labs are done: VMs, Azure SQL, Key Vault, and NSG flow logs send data to the Log Analytics workspace, and Sentinel is enabled on it.
- The `geo_ipv4` and `geo_ipv4_cities` watchlists exist in Sentinel (the map queries join on them).
- Check your subscription's Cost Analysis before and after. This lab runs several resources for more than 24 hours.

## Steps

### Part 1: Build the attack maps (workbooks)

You will build 4 workbooks, each a world map of one kind of malicious traffic. Prebuilt JSON keeps the typing to a minimum.

1. Go to Microsoft Sentinel > Workbooks and select Add workbook.
2. Select Edit, then remove the pre-included text and query items.
3. Select Add > Add query, open Advanced Editor, and paste the contents of [linux-ssh-auth-fail.json](../01-cloud-soc-project-summary/Sentinel-Maps%28JSON%29/linux-ssh-auth-fail.json).
4. Select Done Editing and run the query.

   Expected result: a world map of Linux SSH authentication failures. Your bubbles will differ from mine because they reflect whoever attacked your VMs.

5. Optional: open Edit > Map Settings to tune the map. The JSON already sets Location info to Latitude/Longitude, Coloring type to Heatmap with a Green to Red palette, and the metric label to `friendly_location`. I kept the defaults.
6. Select Save, title it `Linux SSH Auth Failure`, and save it to your lab resource group and region.
7. Repeat steps 1 to 6 for the other three maps:
   - [MS SQL authentication failures](../01-cloud-soc-project-summary/Sentinel-Maps%28JSON%29/mssql-auth-fail.json)
   - [NSG malicious flows allowed in](../01-cloud-soc-project-summary/Sentinel-Maps%28JSON%29/nsg-malicious-allowed-in.json)
   - [Windows RDP and SMB authentication failures](../01-cloud-soc-project-summary/Sentinel-Maps%28JSON%29/windows-rdp-auth-fail.json)

   Expected result: the SQL map is dominated by sources in Russia and the Netherlands, the NSG map shows dozens of sources on every continent, and the RDP map shows a few large clusters (in my run: Los Angeles, Jakarta, Giza).

8. To look at a narrower window, open a workbook, select Edit, and change Time Range (for example to Last 30 minutes).

   Expected result: the map redraws with only the sources seen in that window.

9. Open Sentinel > Workbooks and confirm your saved list.

   Expected result: 4 custom workbooks: Linux SSH Auth Failure, MySQL Auth Fail, nsg-malicious-allowed-in, and Windows RDP & SMB Authentication Failure.

Troubleshooting, if a map is still empty 24 hours after you created the resources:

- Generate some traffic yourself (failed logins) and check again.
- Make sure both VMs are running.
- Check that Defender for Cloud and the Data Collection Rules collect logs from the VMs (Logging and Monitoring lab).
- Check that MS SQL Server logging is configured (Azure intro lab).
- If NSG flow logs are empty, recheck their configuration (Logging and Monitoring lab).
- You can also skip ahead to Part 3 to generate traffic, but logging must work first.

### Part 2: Analytics, alerting, and incident generation

10. In the Log Analytics workspace, open Logs and run this query to find sources with 10 or more failed Windows logons in the last hour:

    ```kusto
    SecurityEvent
    | where EventID == 4625
    | where TimeGenerated > ago(60m)
    | summarize FailureCount = count() by SourceIP = IpAddress, EventID, Activity
    | where FailureCount >= 10
    ```

    Expected result: a handful of source IPs, each with 10 to a few hundred failures. A user mistyping a password a few times stays under the threshold; 10 or more in an hour is worth an alert.

11. Go to Sentinel > Analytics and select Create > Scheduled query rule.
12. On General, set Tactics and techniques to Credential Access > Brute Force.
13. On Set rule logic, paste the rule query:

    ```kusto
    SecurityEvent
    | where EventID == 4625 and LogonType == 3
    | where TimeGenerated > ago(60m)
    | summarize FailureCount = count() by AttackerIP = IpAddress, EventID, Activity, LogonType, DestinationHostName = Computer
    | where FailureCount >= 10
    ```

    Expected result: View query results lists several attacker IPs against `windows-vm`.

14. Under Alert enrichment > Entity mapping, add an IP entity with Address = `AttackerIP`, then a Host entity with HostName = `DestinationHostName`. Sentinel uses these entities to correlate one attacker IP across alerts.
15. Under Query scheduling, set Run query every 10 minutes and Lookup data from the last 1 day. Set Alert threshold to "is greater than 0", Event grouping to "Group all events into a single alert", and leave Suppression off.
16. On Incident settings, keep Create incidents enabled. Enable Alert grouping, limit it to 5 hours, and group alerts when all entities match. Leave Re-open closed matching incidents disabled.
17. Select Review and create, then Create.

    Expected result: within minutes, Sentinel > Incidents shows a Medium incident such as "Test: Brute Force Windows".

18. Open the incident.

    Expected result: 1 alert, about 11 IP entities, and the tactic Credential Access.

19. Select Investigate.

    Expected result: a graph linking the incident to `windows-vm` and each attacker IP.

20. Delete the test rule and its incident. If no incident appeared, RDP into `windows-vm` and fail the login 10 or more times.
21. Download [Sentinel-Analytics-Rules(KQL Alert Queries).json](../01-cloud-soc-project-summary/Sentinel-Analytics-Rules/Sentinel-Analytics-Rules%28KQL%20Alert%20Queries%29.json) and import it from Sentinel > Analytics > Import.

    Expected result: 13 active rules (7 High, 6 Medium): the built-in Fusion "Advanced Multistage Attack Detection" plus 12 custom rules:
    - CUSTOM: Brute Force ATTEMPT and SUCCESS for Windows, Linux Syslog, and Azure Active Directory
    - CUSTOM: Brute Force ATTEMPT for MS SQL Server and Azure Key Vault
    - CUSTOM: Possible Privilege Escalation (Azure Key Vault Critical Credential Retrieval or Update)
    - CUSTOM: Possible Privilege Escalation (Global Admin Role Assignment)
    - CUSTOM: Possible Lateral Movement (Excessive Password Resets)
    - CUSTOM: Malware Detected

    The Overview page then shows the first few incidents (4 in my run).

22. Open any rule and read its query under Set rule logic. For example, CUSTOM: Possible Privilege Escalation (Global Admin Role Assignment):

    ```kusto
    AuditLogs
    | where OperationName == "Add member to role" and Result == "success"
    | where TargetResources[0].modifiedProperties[1].newValue == '"Company Administrator"' and TargetResources[0].type == "User"
    | project TimeGenerated, OperationName, AssignedRole = TargetResources[0].modifiedProperties[1].newValue, InitiatorId = InitiatedBy.user.id, InitiatorUpn = InitiatedBy.user.userPrincipalName, TargetAccountId = TargetResources[0].id, TargetAccountUpn = TargetResources[0].userPrincipalName, InitiatorIpAddress = InitiatedBy.user.ipAddress, Status = Result
    ```

    - `AuditLogs` is the table of Azure AD directory actions.
    - The first `where` keeps successful "Add member to role" operations.
    - The second `where` keeps only assignments of a user to the Company Administrator (Global Admin) role.
    - `project` keeps and renames the useful columns: time, operation, assigned role, who did it (ID, UPN, IP), the target account (ID, UPN), and the result.

23. Wait a little, then open Sentinel > Incidents and pick a new one, such as "CUSTOM: Brute Force ATTEMPT - MS SQL Server".

    Expected result: several alerts and events, about 8 attacker IPs plus `windows-vm`, and Similar incidents listing related Windows brute force attempts.

24. Select Investigate.

    Expected result: a dense web linking 4 alerts to the same set of attacker IPs.

25. Open the MS SQL workbook and set the time range to match the incident.

    Expected result: the map shows the same sources, mostly Russia and the Netherlands.

### Part 3: Generate attack traffic

Play the attacker. The internet has probably already done a lot of this for you.

Expected result before you start: Sentinel > Incidents already shows dozens of open incidents (73 in my run, 2 High), mostly Windows brute force attempts arriving every 15 minutes.

26. RDP into `attack-vm` and install Visual Studio Code (SSMS is optional).
27. Open PowerShell as Administrator and install the Az module:

    ```powershell
    Install-Module Az
    ```

28. Answer `Y` to install the NuGet provider, then `A` (Yes to All) to trust the PSGallery repository.
29. Download the 4 scripts from the Attack-Scripts folder into one folder on the VM (for example `Downloads\Attack Scripts`):
    - [AAD-Brute-Force-Success-Simulator.ps1](../01-cloud-soc-project-summary/Attack-Scripts/AAD-Brute-Force-Success-Simulator.ps1)
    - [Key-Vault-Secret-Reader.ps1](../01-cloud-soc-project-summary/Attack-Scripts/Key-Vault-Secret-Reader.ps1)
    - [Malware-Generator-EICAR.ps1](../01-cloud-soc-project-summary/Attack-Scripts/Malware-Generator-EICAR.ps1)
    - [SQL-Brute-Force-Simulator.ps1](../01-cloud-soc-project-summary/Attack-Scripts/SQL-Brute-Force-Simulator.ps1)

30. Open the folder in VS Code, choose "Yes, I trust the authors", and install the PowerShell extension if prompted.

You can do what each script does by hand, but scripting it is faster and repeatable. If a line is unclear, ask an AI assistant to explain it line by line. After each script, check both Log Analytics and Sentinel incidents.

**AAD brute force success** (manual alternative: fail and then succeed at the portal sign-in)

31. Edit the variables at the top of `AAD-Brute-Force-Success-Simulator.ps1`:

    ```powershell
    $tenantId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"      # Your tenant ID, from the Azure AD blade
    $username = "attacker@<your-tenant>.onmicrosoft.com"    # A user that exists in your tenant
    $correct_password = "<attacker-user-password>"          # That user's real password
    $wrong_password = "___WRONG PASSWORD___"                # Used to generate failures
    $max_attempts = 11                                      # Failures before the successful login
    ```

    If you forgot the user's password, reset it from a private browser window and sign in to Azure AD once.

32. Run the script. At the security warning, answer `R` (Run once).

    Expected result: 11 failed logins in a loop, then 1 successful login.

33. In Log Analytics, run:

    ```kusto
    SigninLogs
    | order by TimeGenerated desc
    ```

    Expected result: a burst of Sign-in activity rows seconds apart. Expanding a failed row shows ResultType 50126 ("Invalid username or password"), Identity `attacker`, and AppDisplayName Microsoft Azure PowerShell. It can take a few minutes to appear.

**Key Vault secret reader** (manual alternative: view the Key Vault secrets in the portal)

34. In `Key-Vault-Secret-Reader.ps1`, set `$KEY_VAULT_NAME` to your vault and `$SECRET_NAME` to your secret (mine was `Tenant-Global-Admin-Password`). The script reads the secret 20 times.
35. Run it. If every read fails with "Run Connect-AzAccount to login", add these two lines after the variables (lines 6 and 7) and run it again, signing in as the attacker user:

    ```powershell
    Disconnect-AzAccount
    Connect-AzAccount
    ```

    The attacker role from the earlier labs has no read rights on the Key Vault. If you still have trouble, stop the VM from the portal, start it again, and rerun the script.

36. In Log Analytics, run:

    ```kusto
    AzureDiagnostics
    | where ResourceProvider == "MICROSOFT.KEYVAULT"
    | where ResultSignature == "Forbidden"
    ```

    Expected result: about 20 SecretGet AuditEvent rows a second apart. Each one shows ResultSignature Forbidden (HTTP 403), and CallerIPAddress is your attack VM's public IP, which is how you know it was you.

    Expected result in Sentinel: a High incident "CUSTOM: Possible Privilege Escalation (Azure Key Vault Critical Credential Retrieval or Update)" with 2 IP and 2 account entities, plus related Key Vault and Azure AD brute force incidents.

**EICAR malware test** (manual alternative: save the EICAR string in a .txt file)

37. Run `Malware-Generator-EICAR.ps1` from PowerShell ISE as Administrator. It joins the two halves of the EICAR test string and writes them to a file. To do it manually, paste the full EICAR string into Notepad and save it as a .txt file.

    Expected result: Windows Security > Protection history shows "Threat quarantined", Severe, Virus:DOS/EICAR_Test_File, pointing at the file you created.

    Sentinel only raises the Malware Detected incident once Windows Security has acted on the file. If it was only flagged, take the action yourself, then wait. It can take a long time to show up.

**SQL brute force** (manual alternative: try bad credentials in SSMS)

38. Run `SQL-Brute-Force-Simulator.ps1`. Logs take a while to land in Log Analytics.
39. For Linux and RDP brute force, just fail the login 10 or more times. The internet is probably already doing this for you.

### Part 4: Run the insecure environment for 24 hours and capture metrics

40. Leave everything running for 24 hours.
41. Confirm the 24-hour window:

    ```kusto
    range x from 1 to 1 step 1
    | project StartTime = ago(24h), StopTime = now()
    ```

    Expected result: one row with a start and stop time 24 hours apart.

42. Run each count query and record the results:

    ```kusto
    // Security events (Windows VMs)
    SecurityEvent
    | where TimeGenerated >= ago(24h)
    | count
    ```

    ```kusto
    // Syslog (Linux VMs)
    Syslog
    | where TimeGenerated >= ago(24h)
    | count
    ```

    ```kusto
    // SecurityAlert (Microsoft Defender for Cloud)
    SecurityAlert
    | where DisplayName !startswith "CUSTOM" and DisplayName !startswith "TEST"
    | where TimeGenerated >= ago(24h)
    | count
    ```

    ```kusto
    // SecurityIncident (Sentinel incidents)
    SecurityIncident
    | where TimeGenerated >= ago(24h)
    | count
    ```

    ```kusto
    // NSG inbound malicious flows allowed
    AzureNetworkAnalytics_CL
    | where FlowType_s == "MaliciousFlow" and AllowedInFlows_d > 0
    | where TimeGenerated >= ago(24h)
    | count
    ```

    ```kusto
    // NSG inbound malicious flows blocked
    AzureNetworkAnalytics_CL
    | where FlowType_s == "MaliciousFlow" and DeniedInFlows_d > 0
    | where TimeGenerated >= ago(24h)
    | count
    ```

    My results before hardening:

    | Metric                   | Count |
    | ------------------------ | ----- |
    | SecurityEvent            | 39046 |
    | Syslog                   | 782   |
    | SecurityAlert            | 0     |
    | SecurityIncident         | 222   |
    | AzureNetworkAnalytics_CL | 1350  |

43. Open each workbook with Time Range set to Last 24 hours and note the top sources.

    Expected result (before hardening):
    - Windows RDP & SMB: thousands of failures, led by Ukraine (4.5K) and Panama (3K).
    - Linux SSH: spread across the US, Europe, Russia, and Asia, a few dozen per city.
    - MySQL: led by Russia (4.17K) and the Netherlands (about 2K each for country and Meppel).
    - NSG malicious allowed in: dozens of sources on every continent, top ones at 100 to 185 flows each.

### Part 5: Incident response (NIST 800-61)

Take notes as you go. Each incident follows the NIST 800-61 lifecycle: Preparation, then Detection and Analysis, then Containment, Eradication, and Recovery, then Post-Incident Activity, looping back to Preparation.

- Preparation: already done by ingesting the logs and creating the alert rules.
- Detection and Analysis: set severity, status, and owner; view full details; read the activity log; review entities and the timeline; select Investigate to find the scope and related events; decide True Positive or False Positive. Close false positives.
- Containment, Eradication, and Recovery: follow the playbook for the incident type.
- Post-Incident Activity: document findings and close the incident in Sentinel.

**Incident 1: Brute Force SUCCESS (Windows)**

44. Open a "CUSTOM: Brute Force SUCCESS - Windows" incident. Assign yourself as owner, set Status to Active, and keep Severity High.
45. Select View full details.

    Expected result: 4 alerts in the timeline, one attacker IP plus `windows-vm` as entities, tactic Credential Access.

46. Open the Activity log.

    Expected result: entries for "Incident was created by Alert Grouping", the owner change, and the status change to Active.

47. Select the attacker IP entity.

    Expected result: geolocation for the source (in my case a telecom network in China).

48. Select Investigate, select the IP node, and expand Related alerts. Use "See all aggregated nodes" for the full list.

    Expected result: the IP connects to more than 14 Brute Force SUCCESS alerts and about 26 Brute Force ATTEMPT alerts (41 related events in my run).

49. List every alert tied to that IP in KQL:

    ```kusto
    let GetIPRelatedAlerts = (v_IP_Address: string) {
        SecurityAlert
        | summarize arg_max(TimeGenerated, *) by SystemAlertId
        | extend entities = todynamic(Entities)
        | mv-expand entities
        | project-rename entity=entities
        | where entity['Type'] == 'ip' and entity['Address'] =~ v_IP_Address
        | project-away entity
    };
    GetIPRelatedAlerts(@'198.51.100.23')
    ```

    Expected result: a list of High Brute Force SUCCESS and Medium Brute Force ATTEMPT alerts for that IP (37 rows in my run).

50. Check whether the "success" is real. This is the rule's own query, from the [KQL cheat sheet](../01-cloud-soc-project-summary/KQL-Queries):

    ```kusto
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

51. List the account names the attackers tried over the last 24 hours:

    ```kusto
    SecurityEvent
    | where EventID == 4625
    | distinct Account
    ```

    Expected result: a long dictionary of common usernames.

52. Narrow it to the attacker: replace `| distinct Account` with a filter on the IP:

    ```kusto
    SecurityEvent
    | where EventID == 4625
    | where IpAddress == "198.51.100.23"
    ```

    Expected result: only 4625 "An account failed to log on" events against `windows-vm`, about one a minute, and no real successful logon.

53. Decide. I closed this as a False Positive: the IP kept brute forcing after the supposed successes, and no actual successful logon exists. The real problem is the attacker's persistence. Given enough time they could get in, so harden the VM anyway.
54. Follow the brute force playbook for a Windows VM:
    - Verify the alert is genuine.
    - Isolate the machine and change the affected user's password.
    - Find the attack's origin and whether that IP is involved in anything else.
    - Determine how and when it happened. If the NSG is wide open, check the other NSGs too.
    - Assess the impact: what type of account was it, and what permissions does it have?
    - Containment and recovery: lock down the NSG on the VM or subnet to allow only necessary traffic, reset the user's password, and enable MFA.
55. Open `windows-vm` > Networking > `windows-vm-nsg`, edit the DANGERAnyInbound rule, set Source to IP Addresses, and enter `<your-public-ip>/32`. The /32 means only that one address.
56. Delete the old RDP rule (port 3389 from Any) from the earlier labs.

    Expected result: the only broad inbound rule left allows your own /32 address, so nobody else can brute force the VM.

57. Repeat the NSG lockdown for every VM.

**Incident 2: Possible Privilege Escalation (Key Vault)**

58. Open "CUSTOM: Possible Privilege Escalation (Azure Key Vault Critical Credential Retrieval or Update)" and work it the same way.

    Expected result: 525 events and 25 alerts. The IP entity geolocates to Microsoft Corporation (an Azure datacenter), and Investigate shows about 24 aggregated alerts from the same IP and accounts.

59. Compare the IP with your attack VM. It matches, so this was the Key Vault script left running. In a real incident, anything generating this many alerts needs a closer look.
60. Confirm with the user. Here, pretend the user is a pentester who arranged the test with their manager.
61. Close the incident as False Positive (Inaccurate Data).

    Expected result: the Overview shows 3 closed incidents (1 Brute Force, 1 Privilege Escalation, 1 duplicate of the Brute Force).

**Incident 3: Brute Force ATTEMPT (Linux)**

My lab had no successful Linux brute force, only attempts.

62. Open a "CUSTOM: Brute Force ATTEMPT - Linux Syslog" incident and select Investigate.

    Expected result: 1 alert, about 5 events, 5 attacker IPs plus `linux-vm`, and several similar Linux Syslog incidents. The alert's Entities field lists the host and each IP.

63. Check for any real success:

    ```kusto
    // Brute Force Success Linux
    let FailedLogons = Syslog
    | where Facility == "auth" and SyslogMessage startswith "Failed password for"
    | where TimeGenerated > ago(1h)
    | project TimeGenerated, SourceIP = extract(@"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", 0, SyslogMessage), DestinationHostName = HostName, DestinationIP = HostIP, Facility, SyslogMessage, ProcessName, SeverityLevel, Type
    | summarize FailureCount = count() by AttackerIP = SourceIP, DestinationHostName
    | where FailureCount >= 5;
    let SuccessfulLogons = Syslog
    | where Facility == "auth" and SyslogMessage startswith "Accepted password for"
    | where TimeGenerated > ago(1h)
    | project TimeGenerated, SourceIP = extract(@"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", 0, SyslogMessage), DestinationHostName = HostName, DestinationIP = HostIP, Facility, SyslogMessage, ProcessName, SeverityLevel, Type
    | summarize SuccessfulCount = count() by SuccessTime = TimeGenerated, AttackerIP = SourceIP, DestinationHostName
    | where SuccessfulCount >= 1
    | project DestinationHostName, SuccessfulCount, AttackerIP, SuccessTime;
    let BruteForceSuccesses = SuccessfulLogons
    | join kind = leftouter FailedLogons on AttackerIP, DestinationHostName;
    BruteForceSuccesses
    ```

    Expected result: no successful logins. To focus on one attacker out of thousands, add a filter on that IP.

64. Per the playbook, check whether these IPs are tied to other incidents. They were, so reset the VM password (Virtual machines > `linux-vm` > Reset password, mode Reset password, your admin username, a new password) and lock down the Linux NSG the same way as step 55.
65. Record the impact: a non-admin account on a Linux VM, probably low impact, but the attackers appear in many other incidents. NSG hardening covers them.
66. Close the incident as Benign Positive (a real attempt, no success).

**Incident 4: Possible Malware Outbreak**

67. Open "CUSTOM: Malware Detected".

    Expected result: a High incident with `windows-vm` as the only entity, a dozen alerts added by Alert Grouping, and Investigate linking the VM to the malware alerts plus many brute force alerts.

    The extra alerts are not necessarily part of the malware incident, although attackers who get in often drop malware.

68. Look at the alerts behind the incident:

    ```kusto
    SecurityAlert
    | where AlertType == "AntimalwareActionTaken"
    ```

    Expected result: a few Low "Antimalware Action Taken" alerts from Microsoft Antimalware.

69. Filter to the compromised entity:

    ```kusto
    SecurityAlert
    | where AlertType == "AntimalwareActionTaken"
    | where CompromisedEntity == "windows-vm"
    ```

70. Exclude alerts that were already remediated automatically:

    ```kusto
    SecurityAlert
    | where AlertType == "AntimalwareActionTaken"
    | where CompromisedEntity == "windows-vm"
    | where RemediationSteps !has "No user action is necessary"
    ```

    Expected result: the remaining rows say Microsoft Antimalware has taken an action to protect the machine.

71. Exclude the EICAR test file to confirm nothing else is behind it:

    ```kusto
    SecurityAlert
    | where AlertType == "AntimalwareActionTaken"
    | where CompromisedEntity == "windows-vm"
    | where RemediationSteps !has "No user action is necessary"
    | where ExtendedProperties !has "EICAR"
    ```

    Expected result: "No results found". The only malware was your EICAR test file, and it was remediated automatically.

72. Close the incident as Benign Positive - Suspicious but expected, with a comment naming the incident, the host, and that other alerts were raised.

**Wrap up**

73. In Sentinel > Incidents, select all remaining open incidents, then Actions: assign them to yourself, set Status to Closed, set the classification to Benign Positive - Suspicious but expected, and add the comment "Mass Closing".

    Expected result: 0 open incidents, "No incidents were found".

74. Leave the environment running for another 24 hours. The next lab hardens it and compares the before and after metrics.

## What I learned

- How to turn raw logs into map workbooks and scheduled analytics rules, including entity mapping, scheduling, and alert grouping.
- How to generate controlled attack traffic (Azure AD brute force, Key Vault reads, EICAR, SQL brute force) and trace each one through Log Analytics and Sentinel.
- How to work incidents with NIST 800-61: scope with entities and the investigation graph, confirm with KQL, then decide True Positive, False Positive, or Benign Positive.
- That an open NSG invites constant brute force. Restricting inbound access to a single /32 is the most effective fix.

## Next steps / cleanup

- Continue to the hardening lab and compare the 24-hour metrics before and after.
- When you're done with the series, delete the lab resource groups to stop charges, and check Cost Analysis.

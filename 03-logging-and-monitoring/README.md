# Logging and Monitoring

Build the logging layer of an Azure cloud SOC. You load GeoIP data into Microsoft Sentinel, then send logs from Azure AD (tenant), the Activity Log (subscription), and VMs, NSGs, Blob Storage, and Key Vault (resources) into one Log Analytics workspace, and query them with KQL.

The finished design has Azure AD, a SQL database, two VMs behind NSGs, Blob Storage, Key Vault, and the Activity Log all feeding a single Log Analytics workspace that Sentinel reads from.

## What you'll use

- Microsoft Azure: Storage account, Log Analytics workspace, Microsoft Sentinel, Microsoft Defender for Cloud, Azure Monitor, Key Vault, Azure AD (Entra ID) with Premium P2
- VMs: `windows-vm` (Windows 10 Pro 21H2 with SQL Server), `linux-vm` (Ubuntu Server 20.04 LTS), and `attack-vm` for generating test traffic
- SQL Server Management Studio (SSMS), Remote Desktop, SSH, Visual Studio Code with the PowerShell extension
- KQL (Kusto Query Language)

## Prerequisites

- The resource group `RG-Cyber-Lab` with `windows-vm` and its virtual network (`Lab-VNet`), plus `attack-vm` in `RG-Cyber-Lab-Attacker`, from the [Cloud SOC prerequisites lab](../02-cloud-soc-prerequisites/).
- The two GeoIP2 city CSV files from the course materials: `GeoIP2-City-Blocks-IPv4.csv` (about 496 MB) and `GeoIP2-City-Locations-en.csv` (about 12 MB).

## Steps

### Part 1: Ingest GeoIP data into Sentinel

Event logs only show IP addresses. The GeoIP watchlists let you map each IP to a city and country.

1. Download both GeoIP2 CSV files.
   Expected result: `GeoIP2-City-Blocks-IPv4.csv` and `GeoIP2-City-Locations-en.csv` are in your Downloads folder. The Blocks file is about 496 MB, so it takes a minute.
2. In the Azure portal, go to Storage accounts > Create storage account.
3. On the Basics tab, set Resource group `RG-Cyber-Lab`, a storage account name (for example `<your-storage-account>`), Region (US) East US 2, Performance Standard, and Redundancy Locally-redundant storage (LRS). Create it.
4. Open the storage account > Data storage > Containers > + Container. Name it `ipgeodata`, keep Public access level Private (no anonymous access), and click Create.
5. Open `ipgeodata` > Upload, select both CSV files, and click Upload. The large file takes a while.
   Expected result: the container lists `GeoIP2-City-Blocks-IPv4.csv` and `GeoIP2-City-Locations-en.csv`.
6. Right-click `GeoIP2-City-Blocks-IPv4.csv` (or use its ... menu) and choose Generate SAS. A SAS grants access to one file instead of the whole container.
7. Set Permissions Read, push the Expiry date out past the end of the lab, keep Allowed protocols HTTPS only, and click Generate SAS token and URL. Copy the Blob SAS URL into a notepad.
8. Repeat steps 6 and 7 for `GeoIP2-City-Locations-en.csv`.
   Expected result: your notepad holds two labelled Blob SAS URLs shaped like this:

   ```text
   https://<your-storage-account>.blob.core.windows.net/ipgeodata/GeoIP2-City-Blocks-IPv4.csv?sp=r&st=<start-time>&se=<expiry-time>&spr=https&sv=<api-version>&sr=b&sig=<signature>
   https://<your-storage-account>.blob.core.windows.net/ipgeodata/GeoIP2-City-Locations-en.csv?sp=r&st=<start-time>&se=<expiry-time>&spr=https&sv=<api-version>&sr=b&sig=<signature>
   ```

9. Go to Log Analytics workspaces > Create. Set Resource group `RG-Cyber-Lab`, Name `LAW-Cyber-Lab-05`, Region East US 2, and create it. This is where every log in the lab lands.
10. Go to Microsoft Sentinel > Create, select `LAW-Cyber-Lab-05`, and click Add. Sentinel offers a 31-day free trial.
11. In Sentinel, go to Configuration > Watchlist > + Add new.
12. On the General tab, set Name and Alias to `geo_ipv4`.
13. On the Source tab, set Source type Azure Storage, File type CSV file with a header, Number of lines before row with headings `0`, paste the Blob SAS URL for `GeoIP2-City-Blocks-IPv4.csv`, and set SearchKey `network`. Review and create.
    Expected result: the file preview shows columns `network`, `geoname_id`, and `registered_country_geoname_id`.
14. Create a second watchlist with Name and Alias `geo_ipv4_cities`, Source type Azure Storage, Number of lines `0`, the Blob SAS URL for `GeoIP2-City-Locations-en.csv`, and SearchKey `geoname_id`.
15. Wait for both watchlists to load. The large one can take more than 24 hours.
16. In `LAW-Cyber-Lab-05` > Logs, join the two watchlists to confirm the data is there:

    ```kusto
    let GeoIPDB = _GetWatchlist("geo_ipv4");
    let GeoIPDB_cities = _GetWatchlist("geo_ipv4_cities");
    let GeoIPDB_FULL = GeoIPDB | join kind = leftouter GeoIPDB_cities on geoname_id;
    GeoIPDB_FULL | limit 10
    ```

    Expected result: 10 rows with `SearchKey` (a network range), `accuracy_radius`, `geoname_id`, and `latitude` filled in.

### Part 2: Create the Linux VM and turn on Defender for Cloud

17. Create a VM in `RG-Cyber-Lab` named `linux-vm`, in the same region and VNet as `windows-vm`. Use Image Ubuntu Server 20.04 LTS x64 Gen2 and Security type Standard.
18. Pick a size larger than B1s (for example Standard_D2s_v3, 2 vCPUs, 8 GiB) so the VM keeps logging under attack traffic. Choose Authentication type Password with a username and password, and allow inbound SSH (22). Open the VM's NSG to all inbound traffic, as you did for `windows-vm`, so it attracts attempts.
19. Go to Microsoft Defender for Cloud > Management > Environment settings. On the `Azure subscription 1` row, open the ... menu and choose Edit settings.
20. Under Defender plans, click Enable all plans and save.
21. Under Continuous export, open the Log Analytics workspace tab and set Export enabled On. Select Security recommendations (all, severity Low, Medium, High, include security findings), Secure score (overall and control score), Security alerts (Low, Medium, High, Informational), and Regulatory compliance (all standards). Send it to `LAW-Cyber-Lab-05` and save.
22. Under Security policy > Industry & regulatory standards, click Add more standards. Add NIST SP 800-53 and CIS Microsoft Azure Foundations Benchmark 1.4.0.
23. Back in Environment settings, open the ... menu on the `LAW-Cyber-Lab-05` row and choose Edit settings.
    Expected result: the subscription row now shows 12/12 plans.
24. Under Defender plans for the workspace, click Enable all plans. Servers and SQL servers on machines switch to On. Save.
25. Under Data collection, choose All Events (all Windows security and AppLocker events) and save. This sends Windows security events to the workspace.

### Part 3: Send NSG flow logs and NSG diagnostics to the workspace

26. Open `windows-vm` > Networking and click the network security group `windows-vm-nsg`.
27. Create an NSG flow log for `windows-vm-nsg`: storage account `<your-storage-account>`, Retention 30 days, Flow Logs Version 2, Traffic Analytics enabled every 10 minutes, workspace `LAW-Cyber-Lab-05`.
    Expected result: Review + create shows Validation passed with flow log name `windows-vm-nsg-rg-cyber-lab-flowlog`.
28. Repeat for `linux-vm` > Networking > `linux-vm-nsg`.
29. Open `windows-vm-nsg` > Diagnostic settings > Add diagnostic setting. Name it `DS-vNIC-logs`, check allLogs (Network Security Group Event and Rule Counter), check Send to Log Analytics workspace, pick `LAW-Cyber-Lab-05`, and save.
30. Repeat the diagnostic setting for `linux-vm-nsg`.

### Part 4: Collect VM logs with data collection rules

31. In Sentinel, go to Configuration > Data connectors, search `windows`, select Windows Security Events via AMA, and click Open connector page. This connector streams security events from connected Windows machines into the workspace.
32. Click Create data collection rule. On Basics, set Rule Name `windows-vm-logs`, Subscription `Azure subscription 1`, and Resource Group `RG-Cyber-Lab`.
33. On Resources, click Add resources and check `windows-vm` under `RG-Cyber-Lab`.
34. On Collect, choose All Security Events and create the rule.
    Expected result: Review + create lists `windows-vm` (microsoft.compute/virtualmachines) and Selected events AllEvents.
35. Go to `LAW-Cyber-Lab-05` > Agents > Linux servers and click Data Collection Rules, then Create.
36. On Basics, set Rule Name `Linux-vm-logs`, Resource Group `RG-Cyber-Lab`, Platform Type Linux, and Data Collection Endpoint none.
37. On Resources, click Add resources and check `linux-vm`.
38. On Collect and deliver, click Add data source. Choose Linux Syslog, set `LOG_AUTH` to `LOG_DEBUG`, and leave every other facility at `none`. Keep the destination Azure Monitor Logs (`LAW-Cyber-Lab-05`).
    Expected result: Review + create shows Validation passed, resource `linux-vm`, data source Linux Syslog to Azure Monitor Logs, platform Linux.
39. Create one more rule for application logs on Windows: Rule Name `windows-vm-logs-2`, Platform Type Windows, resource `windows-vm`, data source Windows Event Logs (Application) to Azure Monitor Logs.
    Expected result: Review + create shows Validation passed, resource `windows-vm`, data source Windows Event Logs, platform Windows.
40. Go to `LAW-Cyber-Lab-05` > Agents and refresh until both VMs report in.
    Expected result: Windows servers shows 1 Windows computer connected via Azure Monitor Windows agent, and Linux servers shows 1 Linux computer connected via Azure Monitor Linux agent.
41. In Logs, run `Syslog`.
    Expected result: auth facility rows from `linux-vm` with messages such as `Invalid user ... from <ip>` and `Failed password for invalid user`. The internet is already probing the VM.
42. Count failed Windows logons:

    ```kusto
    SecurityEvent
    | where EventID == 4625
    | count
    ```

    Expected result: a single Count row (over a thousand failed logons within the first 24 hours in this lab).

### Part 5: Generate failed logins and find them with KQL

43. From `attack-vm`, open SSMS and try to connect to `<windows-vm-public-ip>` as `sa` with a wrong password three times.
    Expected result: Cannot connect to `<windows-vm-public-ip>`. Login failed for user 'sa'. (Microsoft SQL Server, Error: 18456)
44. From `attack-vm`, open Remote Desktop Connection to `<windows-vm-public-ip>` as `labuser` and enter a wrong password.
    Expected result: The logon attempt failed.
45. From `attack-vm`, fail SSH logins to `linux-vm` three times with a made-up username, then sign in once with the real account:

    ```powershell
    ssh <made-up-user>@<linux-vm-public-ip>
    ssh labuser@<linux-vm-public-ip>
    ```

    Expected result: the made-up user gets Permission denied (publickey,password) after three tries, and the real login ends with Welcome to Ubuntu 20.04.6 LTS.
46. Find the failed SQL logins in the Windows application log:

    ```kusto
    Event
    | where EventLog == "Application"
    | where Source == "MSSQLSERVER"
    | where RenderedDescription startswith "Login failed"
    | order by TimeGenerated desc
    ```

    Expected result: entries from Computer `windows-vm`, Source MSSQLSERVER, user `sa`, Reason Password did not match that for the login provided, and `[CLIENT: <attack-vm-public-ip>]`.
47. Find the failed SSH logins on Linux:

    ```kusto
    Syslog
    | where SyslogMessage contains "<made-up-user>"
    | order by TimeGenerated desc
    ```

    Expected result: sshd entries from `linux-vm` such as Invalid user `<made-up-user>` from `<attack-vm-public-ip>`, Failed password for invalid user, and Connection reset by invalid user [preauth].
48. Find the failed RDP logins from the attack VM:

    ```kusto
    SecurityEvent
    | where EventID == 4625
    | where IpAddress == "<attack-vm-public-ip>"
    | order by TimeGenerated desc
    ```

    Expected result: rows with Account `attack-vm\labuser`, Computer `windows-vm`, Channel Security.

### Part 6: Tenant-level logging (Azure AD)

49. In Azure AD, go to Licenses > All products, click Add, and start the Azure AD Premium P2 free trial. Identity Protection needs it.
50. Go to Azure AD > Security > Identity Protection > User risk policy. Set Users All users, User risk Low and above, Access Block access, Policy enforcement Enabled, and save.
51. Turn on the Sign-in risk policy the same way.
52. Go to Azure AD > Monitoring > Diagnostic settings > Add diagnostic setting. Name it `AAD Logs`, select the log categories (AuditLogs, SignInLogs, NonInteractiveUserSignInLogs, and the rest you want), and send them to `LAW-Cyber-Lab-05`.
    Expected result: the Diagnostic settings list shows `AAD Logs` with Log Analytics workspace `LAW-Cyber-Lab-05`.
53. Go to Users > New user > Create new user. Set User principal name and Display name `dummy_user`, keep Auto-generate password and Account enabled, and create it.
54. Open `dummy_user` > Assigned roles > Add assignments, search `global`, and assign Global Administrator.
55. Open `dummy_user` > Overview > Delete, and confirm Delete. Creating, elevating, and deleting the user generates audit logs.
56. On `attack-vm`, install Visual Studio Code (`VSCodeUserSetup....exe`) and the PowerShell extension.
57. Open `AAD-Brute-Force-Success-Simulator.ps1` in VS Code as Administrator. Set `$tenantId`, `$username` (a user in your tenant, for example `attacker@<your-tenant>.onmicrosoft.com`), `$correct_password`, and `$max_attempts`. The script installs the Az module if needed, fails the login `$max_attempts` times with a wrong password, then signs in successfully once. Run it.
58. In `LAW-Cyber-Lab-05` > Logs, review the sign-ins:

    ```kusto
    SigninLogs
    | order by TimeGenerated desc
    ```

    To see only the failures with location details:

    ```kusto
    SigninLogs
    | where ResultDescription == "Invalid username or password or Invalid on-premise username or password."
    | extend location = parse_json(LocationDetails)
    | extend City = location.city, State = location.state, Country = location.countryOrRegion, Latitude = location.geoCoordinates.latitude, Longitude = location.geoCoordinates.longitude
    | project TimeGenerated, ResultDescription, UserPrincipalName, AppDisplayName, IPAddress, IPAddressFromResourceProvider, City, State, Country, Latitude, Longitude
    | order by TimeGenerated desc
    ```

    Expected result: a burst of Sign-in activity rows in the SignInLogs category, one per attempt the script made.

### Part 7: Subscription-level logging (Activity Log)

59. Go to Azure Monitor > Activity log > Export Activity Logs > Add diagnostic setting. Name it `DS-Monitor`, check Administrative, Security, ServiceHealth, Alert, and Recommendation, send to `LAW-Cyber-Lab-05`, and save.
60. Create two resource groups, `scratch-resource-group` and `Critical-Infrastructure-Wastewater`.
    Expected result: both appear in the Resource groups list next to `RG-Cyber-Lab` and `RG-Cyber-Lab-Attacker`.
61. Delete both resource groups to generate activity.
62. Query the Activity Log:

    ```kusto
    // Changes to network security groups
    AzureActivity
    | where OperationNameValue == "MICROSOFT.NETWORK/NETWORKSECURITYGROUPS/SECURITYRULES/WRITE"
    | order by TimeGenerated
    ```

    ```kusto
    // Deletions within the last 30 minutes
    AzureActivity
    | where OperationNameValue endswith "DELETE"
    | where ActivityStatusValue == "Success"
    | where TimeGenerated > ago(30m)
    | order by TimeGenerated
    ```

    Expected result: the deletion query returns two Success rows, one for SCRATCH-RESOURCE-GROUP and one for CRITICAL-INFRASTRUCTURE-WASTEWATER.

### Part 8: Resource-level logging (Blob Storage and Key Vault)

63. Open your storage account > Monitoring > Diagnostic settings, select blob, and add a diagnostic setting named `DS Storage`. Check StorageRead, StorageWrite, StorageDelete, and the Transaction metric, send to `LAW-Cyber-Lab-05`, and save.
64. Generate storage logs: open `ipgeodata`, select `GeoIP2-City-Locations-en.csv`, and choose ... > Download.
65. Go to Key vaults > Create. Set Resource group `RG-Cyber-Lab`, Key vault name (for example `akv-cyber-lab5`), Region East US 2, Pricing tier Standard. Keep soft-delete at 90 days and purge protection disabled, then create it.
66. Open the key vault > Diagnostic settings > Add diagnostic setting. Name it `akv-logs`, check audit and allLogs plus AllMetrics, send to `LAW-Cyber-Lab-05`, and save.
67. Open the key vault > Secrets > Generate/Import. Set Upload options Manual, Name `Tenant-Global-Admin-Password`, a made-up secret value, Enabled Yes, and create it.
68. Read the secret in the portal a few times to generate Key Vault logs.
69. Wait a few minutes, then query the storage and Key Vault logs in `LAW-Cyber-Lab-05` > Logs. The [KQL queries file](../01-cloud-soc-project-summary/KQL-Queries) has ready-made queries.

## What I learned

- Azure logs live at three layers: tenant (Azure AD), subscription (Activity Log), and resource (VMs, NSGs, storage, Key Vault). Each one needs its own diagnostic setting or data collection rule to reach the workspace.
- Watchlists turn raw IPs into locations, which makes later attack maps possible.
- A VM open to the internet collects failed SSH and RDP attempts within hours.
- A few KQL patterns (`where`, `count`, `order by`, `join`, `extend`, `project`) cover most first-pass investigations.

## Next steps / cleanup

- Continue with [Microsoft Sentinel SIEM](../04-microsoft-sentinel-siem/) to build workbooks and analytics rules on top of these logs.
- If you stop here, delete the lab resource groups to avoid charges. Defender plans and Sentinel bill per resource after their trials end.

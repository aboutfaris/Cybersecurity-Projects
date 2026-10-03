# Cloud SOC Projects

Build a small cloud SOC in Azure: deliberately exposed VMs, Azure AD, SQL, and Key Vault send their logs to a Log Analytics workspace, and Microsoft Sentinel turns those logs into attack maps, alerts, and incidents. This repo is the series index and holds the shared files the labs use.

## What you'll use

- An Azure subscription (watch Cost Analysis; several labs run resources for 24 hours or more)
- Microsoft Sentinel, Log Analytics, Microsoft Defender for Cloud
- Windows and Linux VMs, Azure SQL, Azure Key Vault, Network Security Groups
- The workbook, analytics rule, KQL, and PowerShell files in this repo

## Steps

Do the labs in order. Each one builds on the previous one.

1. Set up the prerequisites: VMs, SQL, failed authentication, and Active Directory. Follow [Cloud-SOC-PreReq](https://github.com/aboutfaris/Cloud-SOC-PreReq).
2. Turn on logging and monitoring so every resource sends logs to the workspace. Follow [Logging-and-Monitoring](https://github.com/aboutfaris/Logging-and-Monitoring).
3. Build the Sentinel maps and rules, generate attack traffic, and work the incidents. Follow [Microsoft-Sentinel-SIEM](https://github.com/aboutfaris/Microsoft-Sentinel-SIEM).
4. Harden the environment and measure the same 24-hour window again. Follow [Secure-Cloud-Configuration](https://github.com/aboutfaris/Secure-Cloud-Configuration).
5. Compare the before and after metrics. Read [Cloud-SOC-Final](https://github.com/aboutfaris/Cloud-SOC-Final).

## Results: before and after hardening

Each stage shows the same 4 workbooks with Time Range set to Last 24 hours.

### Before securing

- Expected result (Linux SSH auth failures): sources across the US, Europe, Russia, and East and Southeast Asia, about 20 to 34 failures per top city (North Bergen 34, Moscow 32, Singapore 31).
- Expected result (MySQL auth failures): heavy brute force from Russia (4.17K) and the Netherlands (2.12K, plus 2.11K from Meppel), with only a few from the US.
- Expected result (Windows RDP and SMB auth failures): thousands of failures, led by Ukraine (4.5K), Panama (3K), and Toronto (989).
- Expected result (NSG malicious flows allowed in): dozens of sources on every continent, led by Ukraine (185), Moscow (164), and Panama (148).

### After locking down the NSGs

- Expected result (Linux SSH auth failures): the query returns no results.
- Expected result (MySQL auth failures): the query returns no results.
- Expected result (Windows RDP and SMB auth failures): the query returns no results.
- Expected result (NSG malicious flows allowed in): still populated worldwide in this 24-hour window, led by London (125), China (98), and the United States (94).

### After hardening the systems

- Expected result (Linux SSH auth failures): the query returns no results.
- Expected result (MySQL auth failures): the query returns no results.
- Expected result (Windows RDP and SMB auth failures): the query returns no results.
- Expected result (NSG malicious flows allowed in): the legend lists a single source (Tromso, Norway: 1 flow), although the map still draws older bubbles.

## Repository contents

- `Attack-Scripts/`: PowerShell scripts that simulate brute force and malware activity against the lab (Azure AD, SQL, Key Vault, EICAR test file).
- `Sentinel-Maps(JSON)/` and `Sentinel-Analytics-Rules/`: Sentinel workbook map definitions and the analytics rule export used in the labs.
- `KQL-Queries`: saved Kusto queries used during investigation.
- `Top 300 Azure Sentinel Used Cases KQL (Kusto Query Language).pdf`: reference sheet of Sentinel KQL use cases.
- The before and after workbook screenshots are described in the Results section above. The original image files remain in the git history.

## What I learned

- How the pieces of a cloud SOC connect: resources send logs to Log Analytics, and Sentinel turns them into maps, alerts, and incidents.
- That internet-exposed VMs and databases draw thousands of brute force attempts within a day.
- That restricting NSGs is the change that clears the authentication-failure maps. The NSG flow map shows how much traffic still reaches the network edge.

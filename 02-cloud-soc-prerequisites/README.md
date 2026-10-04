# Cloud SOC Pre-requisites

Set up the Azure lab that the rest of the Cloud SOC series builds on. You deploy a deliberately exposed Windows VM running SQL Server, generate failed RDP and SQL logins from a second "attacker" VM, read those events in Event Viewer, and then test Azure AD roles at the tenant, subscription, and resource group levels.

Azure organizes everything as a hierarchy: an Azure AD tenant contains management groups, which contain subscriptions, which contain resource groups, which hold the actual resources (VMs, firewalls, SQL databases). Part 4 assigns roles at three of those levels.

## What you'll use

- Microsoft Azure: Virtual Machines, Network Security Groups (NSGs), Azure Active Directory (Entra ID), Access control (IAM)
- Windows 10 Pro (21H2) VMs: `windows-vm` (target) and `attack-vm` (attacker)
- SQL Server 2022 Evaluation and SQL Server Management Studio (SSMS)
- Remote Desktop Connection, Command Prompt, Registry Editor, Event Viewer

## Prerequisites

- An Azure subscription (the free trial works).

## Steps

### Part 1: Build the target VM and SQL Server

1. In the Azure portal, go to Virtual machines > Create. On the Basics tab set:
   - Resource group: create `RG-Cyber-Lab`
   - Virtual machine name: `windows-vm`
   - Region: (US) East US 2
   - Image: Windows 10 Pro, version 21H2 - x64 Gen2
   - A local administrator username and password (for example `<your-username>` and `<your-lab-password>`; document both)
2. On the Networking tab, create a new virtual network named `Lab-VNet` (default subnet `10.0.0.0/24`), keep the new public IP `windows-vm-ip`, NIC network security group Basic, and allow inbound RDP (3389).
3. Click Review + create, then Create.
   Expected result: validation passes and the summary shows `windows-vm` in `RG-Cyber-Lab`, East US 2, size Standard D2s v3 (2 vCPUs, 8 GiB), on `Lab-VNet`.
4. Open Resource groups > `RG-Cyber-Lab` > `windows-vm-nsg` > Inbound security rules > Add. The goal is to make the VM look enticing to attackers, so this rule allows everything:
   - Source: Any, Source port ranges: `*`
   - Destination: Any, Service: Custom, Destination port ranges: `*`
   - Protocol: Any, Action: Allow
   - Priority: `290` (lower than the RDP rule at 300, so it is evaluated first)
   - Name: `DANGERAnyInbound`
5. From your own computer, ping the VM's public IP:

   ```cmd
   ping <windows-vm-public-ip>
   ```

   Expected result: four "Request timed out" lines and 100% loss. The NSG now allows the traffic, but the Windows firewall inside the VM still blocks ICMP.
6. Open Remote Desktop Connection, enter `<windows-vm-public-ip>`, click Connect, and sign in with the VM credentials.
7. Inside the VM, run `wf.msc` from the Start menu to open Windows Defender Firewall with Advanced Security.
8. Click Windows Defender Firewall Properties. On the Domain Profile, Private Profile, and Public Profile tabs, set Firewall state to Off. Ignore IPsec Settings. Click OK.
9. Ping the VM again from your computer. Use `-t` to keep pinging:

   ```cmd
   ping -t <windows-vm-public-ip>
   ```

   Expected result: replies come back with 0% loss.
10. In the VM, download the [SQL Server 2022 evaluation](https://www.microsoft.com/en-us/evalcenter/download-sql-server-2022). Run the installer, choose Download Media, pick the ISO option, open the download folder, and mount the ISO.
    Expected result: File Explorer shows a DVD drive named `SQLServer2022` containing `setup.exe`.
11. Run `setup.exe`. In SQL Server Installation Center, choose Installation > New SQL Server standalone installation. On the Edition page, select Specify a free edition: Evaluation, then Next.
12. On Feature Selection, check only Database Engine Services and keep the default directories.
13. On Database Engine Configuration > Server Configuration, select Mixed Mode (SQL Server authentication and Windows authentication). Windows authentication mode only allows Windows accounts; Mixed Mode also allows SQL logins, which the attack VM will target.
    - Default username: `sa`
    - Password: `<your-lab-password>` (set any password you like, just document it)
14. Click Add Current User, then finish the install.
15. Back in Installation Center, choose Install SQL Server Management Tools and download [SQL Server Management Studio](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms). Run the SSMS installer and click Install.
    Expected result: SSMS installs and you can connect to `windows-vm` with Windows authentication.

### Part 2: Send SQL Server logins to the Windows event log

Follow Microsoft's guide to [write SQL Server audit events to the Security log](https://learn.microsoft.com/en-us/sql/relational-databases/security/auditing/write-sql-server-audit-events-to-the-security-log).

16. In SSMS Object Explorer, right-click `windows-vm` > Properties > Security. Confirm SQL Server and Windows Authentication mode is selected, set Login auditing to Both failed and successful logins, and click OK.
17. From the Start menu, right-click Command Prompt > Run as administrator (accept the User Account Control prompt), then run:

    ```cmd
    auditpol /set /subcategory:"application generated" /success:enable /failure:enable
    ```

    Expected result: "The command was successfully executed."
18. Open Registry Editor (`regedit`) and go to:

    ```text
    HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EventLog\Security
    ```

19. Right-click the `Security` key > Permissions, select NETWORK SERVICE, allow Full Control, and click OK. This lets the SQL Server service write to the Security log.
20. Restart SSMS (or disconnect and reconnect). In Connect to Server, choose SQL Server Authentication and enter a username and password that do not exist.
    Expected result: "Login failed for user ... (Microsoft SQL Server, Error: 18456)".
21. Open Event Viewer > Windows Logs > Application and find the newest MSSQLSERVER entry.
    Expected result: Event ID 18456, Task Category Logon, Keywords Classic, Audit Failure, with the message "Login failed for user ... Reason: Could not find a login matching the name provided. [CLIENT: <local machine>]".

### Part 3: Generate attacks from a second VM

The aim is to see what real failed logins look like, so you can later tell true positives, false positives, true negatives, and false negatives apart.

22. Create a second VM with Virtual machines > Create:
    - Resource group: create `RG-Cyber-Lab-Attacker`
    - Virtual machine name: `attack-vm`
    - Region: a different region from `windows-vm` (for example (Africa) South Africa North), so the attacks come from far away
    - Image: Windows 10 Pro, version 21H2 - x64 Gen2
23. On the Networking tab, create a new virtual network named `Lab-VNet-Attacker` (default subnet `10.1.0.0/24`), keep the new public IP `attack-vm-ip`, and allow inbound RDP (3389). Review + create, then Create.
24. Open `attack-vm` > Overview, copy its Public IP address (`<attack-vm-public-ip>`), and RDP into it from your computer.
25. Inside `attack-vm`, open Remote Desktop Connection, enter `<windows-vm-public-ip>`, and try to sign in 5 times with a wrong username and password.
26. Install SSMS on `attack-vm`. Connect to `<windows-vm-public-ip>` with SQL Server Authentication, user `sa`, and a wrong password, 5 times.
    Expected result: each attempt fails with "Cannot connect to <windows-vm-public-ip>. Login failed for user ... Error: 18456".
27. Sign out of `attack-vm`. From your own computer, RDP into `windows-vm` and open Event Viewer.
28. In Windows Logs > Security, open the newest Audit Failure entries (RDP).
    Expected result: Event ID 4625 (Logon) with Workstation Name `attack-vm`, Source Network Address `<attack-vm-public-ip>`, and authentication package NTLM.
29. In Windows Logs > Application, open the newest MSSQLSERVER entries (SQL).
    Expected result: Event ID 18456 with "Login failed for user 'sa'. Reason: Password did not match that for the login provided. [CLIENT: <attack-vm-public-ip>]". Note the Event IDs, messages, and source IPs; later labs alert on them.

### Part 4: Azure AD users and role-based access control

Use a new private (incognito) browser window for each test user so you stay signed in as the admin in your main window.

Tenant-level Global Reader:

30. In the main browser, go to Azure Active Directory > Users > New user > Create user. Set User name `globalreaderjohn`, Name `globalreaderjohn`, select Auto-generate password, and copy the initial password (`<auto-generated-password>`; yours will be different). Click Create.
31. Open `globalreaderjohn` > Assigned roles > Add assignments. Search `reader`, check Global Reader, and click Add.
    Expected result: the user's Overview shows Assigned roles: 1. Copy the User principal name, for example `globalreaderjohn@<your-tenant>.onmicrosoft.com`.
32. In a private window, sign in to the [Azure portal](https://portal.azure.com/) as `globalreaderjohn`. Change the auto-generated password when prompted and remember the new one.
33. Open Subscriptions, then Azure Active Directory > Users, and open another user.
    Expected result: the subscription page is empty, but you can see every user. On a user's page, Edit properties and Delete are greyed out, and Reset password is not allowed. Global Reader reads tenant settings and nothing more, which is least privilege in practice.
34. Close the private window.

Subscription-level Reader:

35. In the main browser, create another user: User name `subreaderjane`, Auto-generate password (`<auto-generated-password>`).
36. Open Subscriptions > your subscription (for example `Azure subscription 1`) > Access control (IAM) > Add role assignment.
37. Select the Reader role, then Members > Select members, pick `subreaderjane`, and click Review + assign.
38. In a private window, sign in as `subreaderjane` and change the password when prompted.
39. Go to Resource groups. You can see every resource group and the resources inside them. Open `RG-Cyber-Lab-Attacker` > Delete resource group, type the name to confirm, and click Delete.
    Expected result: a "Delete resource group RG-Cyber-Lab-Attacker failed" notification with code AuthorizationFailed. Reader can view everything in the subscription but cannot create or delete anything.
40. Close the private window.

Resource group-level Contributor:

41. In the main browser, create a third user: User name `rgcontributordave`, Auto-generate password (`<auto-generated-password>`).
42. Create a new resource group named `PermissionsTester`.
43. Open `PermissionsTester` > Access control (IAM) > Add role assignment. Select the Contributor role, then Members > Select members, pick `rgcontributordave`, and click Review + assign.
44. In a private window, sign in as `rgcontributordave` and change the password when prompted. Open Resource groups.
    Expected result: only `PermissionsTester` is listed.
45. From the portal home, go to Azure services > Storage accounts > Create, and create a storage account in `PermissionsTester`.
    Expected result: the deployment succeeds and the storage account Overview shows resource group `PermissionsTester`. Contributor can build inside its one resource group but cannot see the rest of the subscription.
46. Close the private window.

## What I learned

- An NSG and the guest OS firewall are separate layers. Opening the NSG was not enough; ping only worked after the Windows firewall was turned off.
- Failed RDP logins land in the Security log as Event ID 4625, and failed SQL logins land in the Application log as Event ID 18456, both with the attacker's source IP.
- SQL Server only writes login failures to the Windows logs after login auditing, `auditpol`, and the EventLog registry permission are all configured.
- Azure RBAC scope matters: Global Reader sees the whole tenant, a subscription Reader sees but cannot change resources, and a resource group Contributor can only work inside its own group.

## Next steps / cleanup

Do not delete `RG-Cyber-Lab`, `windows-vm`, or `attack-vm`. The next lab, [Logging and Monitoring](../03-logging-and-monitoring/), uses the same resource groups and VMs.

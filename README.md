![image](https://user-images.githubusercontent.com/109401839/230745596-57cee9bd-687c-427d-b0db-d1080df77f7e.png)

# Azure Preparation

### We will create our Subscription and Resources, then go over Failed Authentication and Log Observation, and finally
Azure Active Directory Overview (Users, Groups, and Access Management)

#### Environments and Technologies Used 

- Microsoft Azure
- SQL Server
- Event Viewer

### Operating Systems Used

- VM Windows 10 PRO (21H2)

## Resources & SQL Server Vulnerabilties

Faris

<details close>

<div>

</summary>

#### Actions and Observations<b>

- Create Windows 10 Pro Virtual Machine
- Name the Resource Group: RG-Cyber-Lab

![gtxtw3z5](https://user-images.githubusercontent.com/109401839/230747447-40c9b360-38e2-4d8d-b4b2-7ea0bb12ae0f.png)

- Name the Virtual Network. NAME IT “Lab-VNet”

![hjl0rzkf](https://user-images.githubusercontent.com/109401839/230747449-be2118b3-a451-4d32-a756-d4082055ae31.png)

- Now, double-check the VM settings and create! 

![image](https://user-images.githubusercontent.com/109401839/230747537-211a32a7-9525-4572-a455-0a250278c604.png)

- Configure Network Security Group (Layer 4 Firewall) to allow all traffic inbound

- A mini firewall that will be configured for our virtual machine to allow all traffic in. We want to make this firewall look enticing to allow threat actors such as hackers, bots, and attackers to try to get into our virtual machine. 

- In resource groups, we will go inside it, and we can see all the things associated with the VM being created. 
- We will edit, the network security group, either by search or in the resource groups. 
- Based on the traffic coming into the network we can see the priority categorised in Azzure based on the set rules/protocols. 
- Create Inbound Security Rule, Any, Name it "DangerAllInBound" 

![nsg danger inbound](https://user-images.githubusercontent.com/109401839/230748062-20cb8a7d-768c-4d8b-b548-dad98fdef095.png)

- Now try to ping the IP Address of the VM in CMD...
- Did it work? 

![ping](https://i.imgur.com/ZnVQuDB.png)

- No it didn't because we need to remote in and change the firewall setting within the VM as well. 

- Remote Into the VM

- Now remote in, on Windows 10 we will use  "Remote Desktop Connection" 

![e](https://i.imgur.com/8RQ9xpu.png)

- Turn off Windows Firewall
 
- Once you are logged in, search "wf.msc" in the start menu to execute the program "Windows Defender Firewall Advanced Security.
- Click on "Windows Defender Firewall Properties" 
- On each tab, turn off the "Firewall State" 
- Ignore IPSEC Settings for now.

![3](https://i.imgur.com/pBzKoId.png)

- Now observe the changes in CMD: 

![image](https://user-images.githubusercontent.com/109401839/230748490-8588cf7e-e3b4-4739-befd-f4695ba665ce.png)

- Install SQL Server Evaluation

- [Download here](https://www.microsoft.com/en-us/evalcenter/download-sql-server-2022)

- Install .exe file, Download Media, ISO option, Open Folder, and Mount Media

- It will show as a disk file under the "This PC" side panel: 

![image](https://user-images.githubusercontent.com/109401839/230748771-4fd4e778-626d-4baa-8403-b1acf1389bdb.png)

![image](https://user-images.githubusercontent.com/109401839/230748852-edba2194-ebb1-4e15-932f-243d6cce6fac.png)

- Install SSMS (SQL Server Management Studio)

![sql install](https://user-images.githubusercontent.com/109401839/230748997-ad8f84d1-9bf7-4125-b7e5-0cd2f490b62b.png)

![mstsc_Kc9i9HCW3n](https://user-images.githubusercontent.com/109401839/230749050-cdeedde3-6773-48a1-852b-415ea114cfc6.png)

![mstsc_sGtz3qU3M2](https://user-images.githubusercontent.com/109401839/230749062-0bd9eaeb-9c0d-43c2-93a5-c9641bf2285e.png)

- Select "Mixed Mode", this is important because, with Windows Authentication Mode, we will only be able to log in with an online account, whereas, with a mixed mode, we can log in online and locally into the SQL Server.

Default Username: ```sa```
Password: ```LabTest12345```` (This is what we used, you can set any password but document it.) 

- Add your current user, and enter your password. 

- Now Finish Install! Now we can connect to our SQL Database.  

- Next, we will download [Server Management Studio](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16)

![image](https://user-images.githubusercontent.com/109401839/230749437-dfc8f934-0360-4bc8-949f-a99371c0ba40.png)

![image](https://user-images.githubusercontent.com/109401839/230749591-15fffab9-3651-418b-8694-bd763492a9fb.png)

[Configure](https://learn.microsoft.com/en-us/sql/relational-databases/security/auditing/write-sql-server-audit-events-to-the-security-log?view=sql-server-ver16) the audit object access setting in Windows using audit-pol

- Enable logging for SQL Server to be ported into Windows Event Viewer 

- Open a command prompt with administrative permissions.

- From the Start menu, navigate to Command Prompt, and then select Run as administrator.

- If the User Account Control dialogue box opens, select Continue.

- Execute the following statement to enable auditing from SQL Server.

- Windows Command Prompt

- Copy

```audit-pol /set /subcategory: "application generated" /success:enable /failure:enable```

- Close the command prompt window.

![2](https://i.imgur.com/LCjKjIg.png)

- Now RegEdit and explore:

 ```HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EventLog\Security```

![image](https://user-images.githubusercontent.com/109401839/230749756-e9139c85-9cd7-4756-a400-307b02a4c81a.png)

- Restart SQL Management, Disconnect Connection, Reconnect, and Choose SQL Managements Authentication Method. 

- Now, Intentionally enter the wrong username and password to do a failed login attempt. 

![image](https://user-images.githubusercontent.com/109401839/230749821-c108d8bb-e77e-4826-9b93-0a6f2afde4f4.png)

- Test SQL logging to make sure it’s working properly

- Enter Event Viewer, Select Application, and View SQL Management Logs Entries: 

![image](https://user-images.githubusercontent.com/109401839/230749908-b20fe934-00b7-498a-a8f6-1f9554e38aed.png)

- Here we can see the failed login attempt and the reason. That concludes the first lab. 

## Precursor to Security Operations (Failed Authentication and Log Observation)

Vanessa

<details close>

---

</summary>

We will create a VM in the cloud that will be our target of the attack, and we will observe logs and see what they look like. 
The ultimate goal of this lab is to differentiate between false negatives, false positives, true positives, and true negatives. 
  
<b>Actions and Observations<b>

- We are creating an attack vm the goal is to have a different region so it looks like a threat is attacking our windows-VM. 

![OUTSIDE](https://user-images.githubusercontent.com/112146207/230785143-b12ea9d9-8f3d-4fca-a73b-3d54374c3611.png)

``` Now we have to name the VNet Lab-VNet-Attacker```

![image](https://user-images.githubusercontent.com/112146207/230785775-a4c5d027-71cd-4341-8927-faa552ff0cd4.png)

- First thing we will do is get the attack-VM public IP address. Then go to the remote desktop connection and enter your attack VM information. 

![image](https://user-images.githubusercontent.com/112146207/230786468-787b9479-4b0b-42b4-beb0-f627f6c02125.png)

- Get the windows-vm ```public IP address```` and go to RDP and from there go to the start menu and search remote desktop and enter the ``` IP address ```. 
- We will now generate some failed RDP (remote desktop protocol) logs against the windows-vm from the attacker vm. 
- We will attempt this 5 times with the wrong username and password.

![image](https://user-images.githubusercontent.com/112146207/230787466-11cc67e0-4833-4a61-a7b3-f6d250abf75e.png)

- We then go to event viewer and see all the failed login attempts

![image](https://user-images.githubusercontent.com/112146207/230790854-d6bd81a6-4629-4a4d-ab39-681c7b013451.png)

- After this, we will install SSMS within attack-VM and generate some failed MS SQL Auth logs against windows-VM.
- Enter the wrong password 5 times

![image](https://user-images.githubusercontent.com/112146207/230792205-ad1cf545-267b-43ea-9bf0-8ecb72dde3ef.png)

- Log out of the attack VM, and now we are back into our computer. 
- From our computer, we will RDP back into our windows-vm. 
- We will inspect the failures and successes (Security log for RDP, Application log for SQL).
- It's important to also take note of EventIDs, messaging, source IP Addresses etc...

![uuu](https://user-images.githubusercontent.com/112146207/230796726-abf6a180-56d0-4428-9952-8eee097c8147.png)

<div>

<h3>Azure Active Directory Overview (Users, Groups, and Access Management)<h3>
Faris

<details close>

---

</summary>

![Untitled](https://user-images.githubusercontent.com/109401839/230747442-f0a1831d-1cf0-4895-b335-372314cd5d51.png)

<b>Actions and Observations<b>

- Configure and Observe Tenant-Level Global Reader
1. Create a user in Active Directory, we will name the user "globalreaderjohn"
Then we will select the auto password to generate the option, Maxo1396" 
```It will be different for you``

![image](https://user-images.githubusercontent.com/109401839/230799438-00d3e9fe-4348-4052-9995-6d6895f6f283.png)

![image](https://user-images.githubusercontent.com/109401839/230799569-fca3562d-15c4-4332-9e30-0e75432e7e96.png)

- Assign Tenant-Level Global Reader

![image](https://user-images.githubusercontent.com/109401839/230799619-da680846-c56a-479a-b215-ab5758f49b50.png)

![msedge_Y3BrhP8v9T](https://user-images.githubusercontent.com/109401839/230799861-29ebd5fd-4b1d-445f-a9da-abfd1056a726.png)

Be sure to copy your user's "User Principal Name",  for us that is ```globalreaderjohn@fnabeelpm.onmicrosoft.com```

- In a new browser/incognito, log in as globalreaderjohn and observe the result of being a Tenant Level “Global Reader”

 [Login to Azure](http://portal.azure.com/) 

![msedge_HqzxFbf0iN](https://user-images.githubusercontent.com/109401839/230799958-e166ab3b-f43a-4ffc-9042-c836cf5c3ec2.png)

 Azure will prompt you to change your auto-generated password, for us we changed it to ```LabTest123456```, feel free to use anything but be sure to remember it. 

Once you are logged into Azure, notice you can not see anything on your subscription page, however, you can view all available users. 

Due to your role, as Global Reader. I can view users' overviews, however, I am not able to make changes or reset passwords. 

![image](https://user-images.githubusercontent.com/109401839/230800090-ab7e025f-079f-41f5-a8f4-10cf7dbd5676.png)

This is because we have given RBAC (Role-Based Access Control) and enforced the Least Privileges so John can only do his job, Read. 

- Close browser/incognito when satisfied

- Back in the main browser, create another user within AAD  (username: subreaderjane)

- Configure and Observer Subscription Reader

- Auto-generated password, ```Qudo6437```  

![msedge_JftbufmM3X](https://user-images.githubusercontent.com/109401839/230800294-58e9a6f0-984e-435a-8db1-41a5cbbd8523.png)

- Assign Subscription-Level Reader 

This may be called something different for you, for me ``` Azure subscription 1``` and you can find this under ```Subscriptions```. 

Now, Enter the Access Control (IAM) and give Jane the deserved role. 

![image](https://user-images.githubusercontent.com/109401839/230800962-a70cbdaf-c686-41ec-9313-f8dc9cb0fd9e.png)

![msedge_UUzHPizmTA](https://user-images.githubusercontent.com/109401839/230800551-c809f8b7-975f-4a3b-8761-ef7e7c6fe5fb.png)

- In a new browser/incognito, log in as subreaderjane and observe the result of being a Subscription Level “Global Reader”

Again, you will be prompted to change your password and document it. 

Go to resource groups and notice you can see the resources in there and even under subscriptions. 

Let us try to delete a resource group now, we should not be able to do so... 

![image](https://user-images.githubusercontent.com/109401839/230801715-c9537447-9f66-4f22-8d33-19eab3074bd2.png)

Did it delete? YIKES.

![image](https://user-images.githubusercontent.com/109401839/230801752-80f0c485-cf6b-40d5-ac6d-de5b9cedf301.png)

It did not delete! Jane does not have the privileges to create or delete. Only a subscription-level reader. We can not change anything. 

- Close browser/incognito when satisfied

- Configure and Observe Resource Group Contributor (like an admin)

- Back in the main browser, create another user within AAD  (username: rgcontributordave)

Auto-generated password ```Fayo1701```

- Create a new resource group called “Permissions-Tester”

- Assign Resource Group-level Contributor

- For our resource group (RG-Cyber-Lab), assign Contributor Permissions

![image](https://user-images.githubusercontent.com/109401839/230802793-5cd508ee-80f4-4ec5-a550-a9bcfee016b6.png)

- In a new browser/incognito, log in as rgcontributordave and observe the result of being a Subscription Level Reader
 
![msedge_0h9H4b5cvQ](https://user-images.githubusercontent.com/109401839/230802957-c2564141-5e21-4f06-8566-70b1464c40ce.png)

- Observe the result of being a Resource Group Level Contributor

![image](https://user-images.githubusercontent.com/109401839/230803072-730eeeb8-3051-4173-9a19-44d513cddb56.png)

Dave is now able to view the resource group and create further resources in the group such as Storage. 
 
 ![image](https://user-images.githubusercontent.com/109401839/230803808-2d32b1ba-4312-4cc9-99a3-26d158587e0f.png)

```Be sure  NOT to delete your resources``` we will continue with the same RG & VM. 

That concludes the three-part labs series, *Welcome to Cybersecurity*, your journey starts here! 

On our next set of [labs](https://github.com/fnabeel/Logging-and-Monitoring), we will go over Logging and Monitoring. 


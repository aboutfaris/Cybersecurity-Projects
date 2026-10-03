![68747470733a2f2f692e696d6775722e636f6d2f5a5778653033652e6a7067](https://user-images.githubusercontent.com/109401839/236074279-96ae8c16-e42d-43bf-9e33-2b2b3d4b5cde.jpg)

# Cloud SOC Projects

Configuring my own cloud-based SOC environment within Azure. This series demonstrates Azure prerequisite installation, SQL, failed authentication, Active Directory, logging and monitoring, Microsoft Sentinel SIEM, and secure cloud configuration.

---

- [Azure Prerequisite Installation, SQL, Failed Authentication, Active Directory](https://github.com/aboutfaris/Cloud-SOC-PreReq)
- [Logging and Monitoring](https://github.com/aboutfaris/Logging-and-Monitoring)
- [Microsoft Sentinel SIEM](https://github.com/aboutfaris/Microsoft-Sentinel-SIEM)
- [Secure Cloud Configuration](https://github.com/aboutfaris/Secure-Cloud-Configuration)
- [Comprehensive Summary](https://github.com/aboutfaris/Cloud-SOC-Final)

## Repository Contents

- `Attack-Scripts/` — PowerShell scripts that simulate brute-force and malware activity against the lab environment (AAD, SQL, Key Vault, EICAR test file).
- `Sentinel-Maps(JSON)/` and `Sentinel-Analytics-Rules/` — Microsoft Sentinel workbook map definitions and analytics rule exports used in the lab.
- `KQL-Queries/` — saved Kusto queries used during investigation.
- `Cybersecurity Before Securing/`, `Cybersecurity After NSG/`, `CS After Hardening Systems/` — dashboard screenshots showing the before/after effect of hardening the environment. Before hardening, the workbooks showed tens of thousands of failed authentication attempts and malicious inbound flows across Linux SSH, Windows RDP/SMB, and MySQL; after locking down the NSGs to allow only the admin workstation's IP, those same workbooks showed zero events across all four categories. The screenshots are kept as evidentiary results rather than converted to text, since they are workbook output rather than step-by-step instructions.

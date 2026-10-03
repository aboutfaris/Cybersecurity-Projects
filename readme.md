# Vulnerability Management for a Personal Desktop

Harden a Windows 11 desktop, scan it with Nessus, and fix the two medium findings: SMB signing not required and an untrusted SSL certificate.

## What you'll use

- Windows 11
- Nessus (Tenable) Professional
- [HardenTools](https://github.com/hardentools/hardentools)
- Local Group Policy Editor, Internet Options, PowerShell, and Windows Defender Firewall

## Steps

### Part 1: Harden before you scan

1. Download and run HardenTools, then select Show Expert Settings.
2. Leave the default hardening options checked: Windows Script Host, Office Packager Objects (OLE), Office Macros, Office ActiveX, Office DDE Mitigations, the Acrobat Reader options (JavaScript, Embedded Objects, Protected Mode, Protected View, Enhanced Security), Show File Extensions, AutoRun and AutoPlay, Disable PowerShell, User Account Control, File associations, Windows ASR rules, and Defender PUA Protection.
3. Leave Disable cmd.exe and LSA Protection unchecked, then select Harden.
4. Debloat Windows 11 by removing the preinstalled apps, background processes, and telemetry you do not need.

### Part 2: Scan with Nessus

5. In Nessus, run a Basic Network Scan against the desktop.

   Expected result: the scan completes in about 7 minutes. The Vulnerabilities tab lists 23 entries: one MEDIUM finding (CVSS 5.3, family Misc.), a MIXED group in General, and the rest INFO (Windows, Web Servers, Service detection, Port scanners). Most findings are informational fingerprinting.

### Part 3: Fix "SMB Signing not required"

Nessus plugin 57608 (Medium). Signing is not required on the SMB server, so an unauthenticated remote attacker could run a man-in-the-middle attack against it. The Nessus solution is to enforce message signing with the policy "Microsoft network server: Digitally sign communications (always)".

Risk information:

- Risk Factor: Medium
- CVSS v3.0 Base Score: 5.3
- CVSS v3.0 Vector: `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`
- CVSS v3.0 Temporal Vector: `CVSS:3.0/E:U/RL:O/RC:C`
- CVSS v3.0 Temporal Score: 4.6
- CVSS v2.0 Base Score: 5.0
- CVSS v2.0 Temporal Score: 3.7
- CVSS v2.0 Vector: `CVSS2#AV:N/AC:L/Au:N/C:N/I:P/A:N`
- CVSS v2.0 Temporal Vector: `CVSS2#E:U/RL:OF/RC:C`
- Exploit Available: true
- Exploit Ease: Exploits are available
- Vulnerability Publication Date: January 17, 2012

6. Press Win + R, type `gpedit.msc`, and press Enter to open the Local Group Policy Editor.
7. Go to Computer Configuration > Windows Settings > Security Settings > Local Policies > Security Options.
8. Double-click Microsoft network server: Digitally sign communications (always).
9. On the Local Security Setting tab, select Enabled.
10. When the Confirm Setting Change warning about compatibility appears, select Yes, then select Apply and OK.

    Expected result: the policy shows Enabled. The Explain tab notes that with this setting enabled, the server will not talk to an SMB client unless the client agrees to packet signing (the default is disabled for member servers and enabled for domain controllers).

### Part 4: Fix "SSL Certificate Cannot Be Trusted"

Nessus plugin 51192 (Medium). The server's X.509 certificate chain is broken: the top of the chain is not a known public CA (for example, a self-signed certificate), a certificate is outside its valid dates, or a signature does not verify. The Nessus solution is to purchase or generate a proper SSL certificate for the service.

Risk information:

- Risk Factor: Medium
- CVSS v3.0 Base Score: 6.5
- CVSS v3.0 Vector: `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N`
- CVSS v2.0 Base Score: 6.4
- CVSS v2.0 Vector: `CVSS2#AV:N/AC:L/Au:N/C:P/I:P/A:N`

11. Open Internet Options and go to the Advanced tab. Under Settings, confirm Check for server certificate revocation, Check for signatures on downloaded programs, Use TLS 1.2, Use TLS 1.3, and Warn about certificate address mismatch are checked, and Use SSL 3.0, Use TLS 1.0, and Use TLS 1.1 are unchecked. Select Apply.
12. Because one cause is a certificate outside its valid dates, check the system clock in Settings > Time & language > Date & time and select Sync now.
13. To resolve the untrusted chain, create a self-signed certificate for development and add it to the Nessus trusted CAs. Open PowerShell as administrator. If PowerShell is not installed, follow [Microsoft's install guide](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell?view=powershell-7.3).
14. Create the certificate:

    ```powershell
    $cert = New-SelfSignedCertificate -CertStoreLocation "cert:\LocalMachine\My"
    ```

15. Create a secure password for exporting it:

    ```powershell
    $pwd = ConvertTo-SecureString -String '<your-password>' -Force -AsPlainText
    ```

16. Show the certificate and its thumbprint:

    ```powershell
    $cert
    ```

### Part 5: Close commonly targeted ports

These ports are targeted often because they tend to have weak credentials and defenses:

```
FTP (20, 21)
SSH (22)
Telnet (23)
SMTP (25)
NetBIOS over TCP (137, 139)
SMB (445)
SQL Server and MySQL (1433, 1434, 3306)
Remote Desktop (3389)
```

17. In CMD, list listening and established connections and the processes that own them:

    ```cmd
    netstat -aonb
    ```

18. Open Windows Defender Firewall with Advanced Security, select Inbound Rules > New Rule, and choose Port.
19. On Protocol and Ports, select TCP and Specific local ports, and enter the unused ports, for example `445, 20, 21, 23, 25, 137, 139, 1433, 1434, 3306, 3389`. Select Next.
20. Finish the wizard (Action, Profile, Name) so the rule blocks the connections.

## Results

- After the fixes, the scan found no risk factors beyond informational alerts.
- No indicators of compromise were found for: WannaCry Ransomware, Ripple20 Remote Scan, Spectre and Meltdown, CISA Top Vulnerabilities Scan, Microsoft Proxy C2C Scan, Solorigate, ContiLeaks, and the 2022 Threat Landscape Report (TLR).

## What I learned

- Hardening first (HardenTools plus debloating) leaves far fewer findings to triage.
- Most Nessus results on a desktop are informational fingerprinting; the medium findings are where the work is.
- SMB signing is a single Group Policy setting, and closing unused ports with a firewall rule removes common attack paths.

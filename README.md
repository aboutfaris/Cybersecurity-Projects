# Table of Content
[[_TOC_]]

# IR Playbooks

This repository contains Incident Response playbook and workflow templates for an example company's SOC, adapted from a published IR playbook template structure.

Each folder contains a playbook broken down into 6 sections, per [NIST SP 800-61 r2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf).

## 1. Preparation

This section should include the following information:
- List of _ALL_ Assets
  - Servers
  - Endpoints (+critical ones)
  - Networks
  - Applications
  - Employees
  - Security Products
- Baselines
- Communication Plan
- Which Security Events
- Thresholds
- How to access Security Tools
  - How to provision access
- Create Playbooks
- Plan Exercises
  - Table Top
  - Hands On

## 2. Detection and Analysis

This section should include the following information:
- Gathering of Information
- Analyzing the Data
- Building Detections
- Root Cause Analysis
- Depth and Breath of the Attack
  - Admin Rights
  - Affected Systems
- Techniques Used
- Indicators of Compromise / Indicators of Attack
  - Tactics Techniques and Procdures (TTP)
  - IP Address
  - Email Address
  - File Hash
  - Command Line
  - etc.
  
## 3. Containment, Eradication, and Recovery

This section should include the following information:
- Isolate Affected Systems
- Patch Threat Entry Point
- Predefine threshold
  - For Customers
  - For internal systems
  - For escalations
- Preauthorized actions
  - Per customers
  - Per environment
    - Prod
    - QA
    - Internet Facing
- How to Remove the Threat on All Affected Systems
- Get Systems Operational
- Rebuilt and Resume Service

## 4. Post-Incident Activity

- Lessons learned
- New detections
- New hardening
- New patch management
- etc.

# Directory Structure

## Customers

This folder includes all information related to our customers, such as:

- Contacts
  - Names
  - Phone Number
  - Email
- Escalation point
  - Business hours
  - Off Hours
- Account Manager
- Pre-approved Actions and Threshold
- Blackout / Brownout schedule

## Products

This folder contains information about the various commercial products we use during an incident, for example:
- JIRA
- Remedy 
- Service-Now
- ArcSight
- Elastic Stack
- RSA NetWitness
- Splunk
- AMP
- CrowdStrike
- McAfee
- Microsoft ATP
- Symantec
- Firepower
- Fortigate
- Etc.

## IRP-*

These are the individual folders containing the playbooks themselves. Within each directory there should be a PDF folder where an auto-generated PDF version is available for auditors and customers who need to see it.

# Create a New Playbook

## Folder & Files
To create a new Playbook:  
- Create a new folder ex: `IRP-DDoS`
- Create a file called `README.md` inside your new folder
- Paste the content of `IRP-TEMPLATE.md`
- Replace the string `-NAME-` for your playbook name ex: `DDoS` in all the document
- Edit the sections.

## Workflows
To create the Workflows
- Inside your new folder create a folder called `Workflows`
- Open the file `WORKFLOW-TEMPLATE.drawio` in [Draw.io](https://app.diagrams.net)
- Save locally until you have completed all the tabs
- Once all the tabs/phases are completed, upload a copy to your new `Workflows` folder
- Use the `File -> Export as -> PNG` function of Draw.io to save each diagram phase separatly 
    - Make sure you uncheck `Include a copy of the diagram`
    - Click `Export`
    - Save locally
- Upload each .PNG file to your new `Workflows` folder

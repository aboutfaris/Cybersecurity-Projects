# IR-Playbooks

This repository contains Incident Response playbook and workflow templates for an example company's SOC, adapted from a published IR playbook template structure.

Each playbook follows the incident response life cycle in [NIST SP 800-61 r2](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf), and each phase has a written workflow you can follow step by step.

## Contents

- [Playbooks](#playbooks)
- [What you'll use](#what-youll-use)
- [How the playbooks are organized](#how-the-playbooks-are-organized)
- [Directory structure](#directory-structure)
- [Steps: create a new playbook](#steps-create-a-new-playbook)
- [Outcome](#outcome)

## Playbooks

| Playbook | Covers |
| --- | --- |
| [IRP-AccountCompromised](IRP-AccountCompromised/README.md) | Compromised user or service accounts |
| [IRP-Critical](IRP-Critical/README.md) | Escalation path for critical incidents |
| [IRP-DataLoss](IRP-DataLoss/README.md) | Data loss and data leakage |
| [IRP-Malware](IRP-Malware/README.md) | Malware infections |
| [IRP-Phishing](IRP-Phishing/README.md) | Phishing emails |
| [IRP-Ransom](IRP-Ransom/README.md) | Ransomware |
| [IRP-TEMPLATE.md](IRP-TEMPLATE.md) | Starting point for a new playbook |

## What you'll use

- A Markdown editor (any editor, or GitHub's web editor)
- [Draw.io](https://app.diagrams.net) if you want to edit the source diagrams (the `.drawio` file in each playbook's `Workflows` folder)
- `TEMPLATE-Incident_EventLog.xlsx` to record incident events and timestamps

## How the playbooks are organized

### 1. Preparation

- An inventory of all assets:
  - Servers
  - Endpoints (flag the critical ones)
  - Networks
  - Applications
  - Employees
  - Security products
- Baselines
- Communication plan
- Which security events to watch
- Thresholds
- How to access the security tools, and how to provision that access
- Playbooks
- Planned exercises: tabletop and hands-on

### 2. Detection and analysis

- Gather information
- Analyze the data
- Build detections
- Root cause analysis
- Depth and breadth of the attack:
  - Admin rights
  - Affected systems
- Techniques used
- Indicators of compromise and indicators of attack:
  - Tactics, techniques and procedures (TTPs)
  - IP addresses
  - Email addresses
  - File hashes
  - Command lines

### 3. Containment, eradication and recovery

- Isolate the affected systems
- Patch the threat's entry point
- Predefined thresholds for customers, internal systems and escalations
- Preauthorized actions, per customer and per environment (production, QA, internet facing)
- How to remove the threat from all affected systems
- Get systems operational again
- Rebuild and resume service

### 4. Post-incident activity

- Lessons learned
- New detections
- New hardening
- Patch management changes

## Directory structure

### Customers

Information about each customer:

- Contacts (names, phone numbers, email addresses)
- Escalation points for business hours and off hours
- Account manager
- Pre-approved actions and thresholds
- Blackout and brownout schedules

### Products

Notes on the commercial products used during an incident, for example JIRA, Remedy, ServiceNow, ArcSight, Elastic Stack, RSA NetWitness, Splunk, AMP, CrowdStrike, McAfee, Microsoft Defender ATP, Symantec, Firepower and Fortigate.

### Tools

Free and open-source tools for analysis and response. See [Tools](Tools/README.md).

### IRP-*

One folder per playbook. Each holds a `README.md` with the playbook and its written workflows, and a `Workflows` folder with the editable `.drawio` source. A folder can also hold an exported PDF for auditors and customers who need one.

## Steps: create a new playbook

### Folder and files

1. Create a new folder, for example `IRP-DDoS`.
2. Create a `README.md` file inside it.
3. Paste in the content of `IRP-TEMPLATE.md`.
4. Replace every `-NAME-` with your playbook name, for example `DDoS`.
5. Edit each section.

Expected result: `IRP-DDoS/README.md` has every template section with your playbook name filled in.

### Workflows

1. Inside your new folder, create a folder called `Workflows`.
2. There is no blank workflow template, so copy an existing diagram as a starting point, for example `IRP-Phishing/Workflows/Phishing-Workflow.drawio`. Rename it, for example `DDoS-Workflow.drawio`.
3. Open it in [Draw.io](https://app.diagrams.net) and edit one tab per phase: Detect, Analyze, Contain/Eradicate, Recover and Post Incident.
4. Save the finished `.drawio` file to your `Workflows` folder.
5. In your `README.md`, write each phase as a `### Workflow: <phase>` section with numbered steps. Write decision points as "If ... Otherwise ..." so the workflow can be followed without the diagram.

Expected result: your playbook's README has a written workflow for all 5 phases, and the `.drawio` source is in `Workflows`.

## Outcome

A consistent set of playbooks that any analyst can follow step by step, with one shared structure based on NIST SP 800-61 r2 and a template for adding new incident types.

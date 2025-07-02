# 🔧 Automated Incident Remediation with Ansible & ServiceNow

This project demonstrates a real-world use case of integrating **Ansible** with **ServiceNow** to perform **automated incident remediation**. It uses Ansible Playbooks and custom Python scripts to fetch incident data from ServiceNow, parse it, and execute remedial actions automatically.

---

## 📌 Project Goals

- Automatically fetch incidents from ServiceNow using REST API
- Identify incident patterns (e.g., disk full, service down)
- Remediate them using Ansible tasks
- Close or update incidents automatically

---

## 📁 Project Structure

Observe/
├── ansible/
│ ├── inventory/
│ │ └── dev
│ ├── playbooks/
│ │ └── incident_remediation.yml
│ ├── roles/
│ │ └── servicenow/
│ │ ├── defaults/
│ │ │ └── main.yml
│ │ ├── tasks/
│ │ │ └── main.yml
│ │ ├── vars/
│ │ │ └── servicenow.yml
│ │ └── files/
├── scripts/
│ ├── servicenow_incident_fetcher.py
│ ├── incident_parser.py
│ └── test_servicenow_api.py
├── .env
├── ansible.cfg
├── requirements.txt
└── README.md



---

## ⚙️ How It Works

1. **Fetch Incidents:**  
   Python script (`servicenow_incident_fetcher.py`) authenticates with ServiceNow REST API and retrieves active incidents.

2. **Parse Incident:**  
   `incident_parser.py` analyzes incident descriptions and types (e.g., "Disk Full", "Service Unavailable").

3. **Ansible Remediation:**  
   Based on parsing logic, `incident_remediation.yml` triggers Ansible roles to fix issues (e.g., clear temp files, restart services).

4. **Update ServiceNow:**  
   Once remediated, incidents are updated or closed via API call.

---

## ✅ Prerequisites

- ServiceNow Developer Instance ([signup here](https://developer.servicenow.com/))
- Enable API access and get:
  - Instance URL
  - Username
  - Password/API token
- Python 3.8+
- Ansible 2.10+
- Store credentials in a `.env` file.

---

## 🔐 Environment File (`.env`)

```ini
SERVICENOW_INSTANCE=https://devXXXXX.service-now.com
SERVICENOW_USERNAME=admin
SERVICENOW_PASSWORD=your_password

# 🚀 Meraki Network Monitoring & Automation Framework

This project simulates a real-world network automation use case using the **Cisco Meraki Dashboard API**, Python scripting, and CI/CD practices. It is designed for hands-on learning, automation portfolio building, and can be extended for enterprise integration.

---

## 📌 Features

- ✅ Fetch real-time device health data (latency, packet loss, status)
- ✅ Pull client bandwidth usage (MAC, IP, application)
- ✅ Analyze metrics against custom thresholds
- ✅ Generate and store alert reports in CSV format
- ✅ Simulate alerting via console (email/ITSM can be added)
- ✅ Modular design with centralized configuration
- ✅ Ready for CI/CD integration (Jenkins, Ansible, ServiceNow)

---

## 📂 Project Structure

meraki_automation/
├── config/
│ └── config.json # API keys, org ID, thresholds
├── reports/
│ ├── sample_health_report.csv # Sample data (for testing)
│ └── (Generated alert CSVs)
├── scripts/
│ ├── fetch_device_health.py # Pulls device metrics
│ ├── fetch_client_usage.py # Pulls client usage data
│ ├── analyze_metrics.py # Detects threshold breaches
│ └── send_alert.py # Simulated alert notification
├── requirements.txt # Python dependencies
└── README.md

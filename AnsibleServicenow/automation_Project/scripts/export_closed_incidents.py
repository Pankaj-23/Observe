import os
import requests
import json
import csv
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SN_INSTANCE = os.getenv("SN_INSTANCE")
SN_USERNAME = os.getenv("SN_USERNAME")
SN_PASSWORD = os.getenv("SN_PASSWORD")

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

url = f"{SN_INSTANCE}/api/now/table/incident"
params = {
    "sysparm_query": "state=7",  # Closed state
    "sysparm_limit": "100"
}

response = requests.get(url, auth=(SN_USERNAME, SN_PASSWORD), headers=headers, params=params)

if response.status_code != 200:
    print(f"[ERROR] Failed to fetch incidents: {response.status_code}")
    exit(1)

data = response.json()
incidents = data.get("result", [])

# 🧪 Debug: Show what we received
print(f"[INFO] Found {len(incidents)} closed incident(s).")

if not incidents:
    print("No closed incidents to export.")
    exit(0)

# 📦 Save to CSV
filename = f"logs/closed_incidents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
os.makedirs("logs", exist_ok=True)

with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Number", "Short Description", "State", "Closed At", "Priority", "Category"])

    for inc in incidents:
        writer.writerow([
            inc.get("number"),
            inc.get("short_description"),
            inc.get("state"),
            inc.get("closed_at"),
            inc.get("priority"),
            inc.get("category")
        ])

print(f"[SUCCESS] Exported {len(incidents)} closed incidents to {filename}")

import requests
import json
from datetime import datetime

# ✅ Replace with your actual ServiceNow instance details
SNOW_INSTANCE = "https://dev292120.service-now.com"
USER = "Admin"
PASSWORD = "5D5BpvLRx$a*"
TABLE_API = "/api/now/table/incident"

# Sample payload data — customize as needed
def build_payload(short_desc, description, urgency="2", impact="2"):
    return {
        "short_description": short_desc,
        "description": description,
        "urgency": urgency,
        "impact": impact,
        "category": "network"
    }

def create_incident(short_desc, full_description):
    url = f"{SNOW_INSTANCE}{TABLE_API}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = build_payload(short_desc, full_description)

    try:
        response = requests.post(url, auth=(USER, PASSWORD),
                                 headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        result = response.json().get("result", {})
        print(f"✅ Incident created: {result.get('number')} (Sys ID: {result.get('sys_id')})")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to create incident: {e}")

if __name__ == "__main__":
    # Example simulated call
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    short_desc = f"Meraki Device Alert - High Latency at {time_str}"
    description = """
    A Meraki device has exceeded latency threshold.
    Device: Core Switch
    Location: Main Office
    Latency: 178ms
    Packet Loss: 3.1%
    Recommended Action: Investigate uplink health and WAN route.
    """

    create_incident(short_desc, description)

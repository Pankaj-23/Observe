import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load credentials from environment
SN_INSTANCE = os.getenv("SN_INSTANCE", "https://dev12345.service-now.com")
SN_USERNAME = os.getenv("SN_USERNAME", "admin")
SN_PASSWORD = os.getenv("SN_PASSWORD", "your_password")

# Define the API endpoint for fetching and updating incidents
INCIDENT_API_URL = f"{SN_INSTANCE}/api/now/table/incident"

# Define filters: Fetch incidents with 'Resolved' state (state=6)
FILTER_QUERY = "state=6"
LIMIT = 10

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def fetch_resolved_incidents():
    params = {
        "sysparm_query": FILTER_QUERY,
        "sysparm_limit": LIMIT
    }

    response = requests.get(
        INCIDENT_API_URL,
        auth=HTTPBasicAuth(SN_USERNAME, SN_PASSWORD),
        headers=HEADERS,
        params=params
    )

    if response.status_code == 200:
        return response.json().get("result", [])
    else:
        print(f"[ERROR] Failed to fetch incidents. Status Code: {response.status_code}")
        print(response.text)
        return []

def close_incident(incident):
    sys_id = incident["sys_id"]
    update_url = f"{INCIDENT_API_URL}/{sys_id}"
    body = {
        "state": "7",  # Closed
        "close_notes": "Automatically closed by Ansible/Python remediation script."
    }

    response = requests.patch(
        update_url,
        auth=HTTPBasicAuth(SN_USERNAME, SN_PASSWORD),
        headers=HEADERS,
        json=body
    )

    if response.status_code == 200:
        print(f"[CLOSED] Incident {incident['number']} closed successfully.")
    else:
        print(f"[ERROR] Failed to close incident {incident['number']}.")
        print(response.text)

def main():
    incidents = fetch_resolved_incidents()
    if not incidents:
        print("[INFO] No resolved incidents found to close.")
        return

    print(f"[INFO] Found {len(incidents)} resolved incident(s). Closing them...\n")
    for incident in incidents:
        close_incident(incident)

if __name__ == "__main__":
    main()

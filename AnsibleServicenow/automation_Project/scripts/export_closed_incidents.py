import os
import csv
import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Load credentials from environment variables
SN_INSTANCE = os.getenv("SN_INSTANCE")
SN_USERNAME = os.getenv("SN_USERNAME")
SN_PASSWORD = os.getenv("SN_PASSWORD")

# Define the endpoint
INCIDENT_API_URL = f"{SN_INSTANCE}/api/now/table/incident"

# Filter for closed incidents (state=6 or 7 depending on your ServiceNow config)
CLOSED_FILTER = "state=6^ORDERBYDESCclosed_at"

# Headers
HEADERS = {"Accept": "application/json"}


def fetch_closed_incidents():
    params = {"sysparm_query": CLOSED_FILTER, "sysparm_limit": 20}

    try:
        response = requests.get(
            INCIDENT_API_URL,
            auth=HTTPBasicAuth(SN_USERNAME, SN_PASSWORD),
            headers=HEADERS,
            params=params,
        )

        if response.status_code == 200:
            return response.json().get("result", [])
        else:
            print(
                f"Failed to fetch closed incidents. Status Code: {response.status_code}"
            )
            return []

    except Exception as e:
        print(f"Error fetching closed incidents: {e}")
        return []


def export_to_csv(incidents, csv_path):
    with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Number", "Short Description", "State", "Priority", "Closed At"]
        )
        for incident in incidents:
            writer.writerow(
                [
                    incident.get("number", ""),
                    incident.get("short_description", ""),
                    incident.get("state", ""),
                    incident.get("priority", ""),
                    incident.get("closed_at", ""),
                ]
            )


def export_to_json(incidents, json_path):
    with open(json_path, mode="w", encoding="utf-8") as file:
        json.dump(incidents, file, indent=4)


if __name__ == "__main__":
    closed_incidents = fetch_closed_incidents()

    if closed_incidents:
        logs_dir = "AnsibleServicenow/automation_Project/scripts/logs"
        os.makedirs(logs_dir, exist_ok=True)

        export_to_csv(
            closed_incidents, os.path.join(logs_dir, "resolved_incidents.csv")
        )
        export_to_json(
            closed_incidents, os.path.join(logs_dir, "resolved_incidents.json")
        )

        print(f"Exported {len(closed_incidents)} closed incidents to CSV and JSON.")
    else:
        print("No closed incidents to export.")

import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Load credentials from updated environment variables
SN_INSTANCE = os.getenv("SN_INSTANCE", "https://dev12345.service-now.com")
SN_USERNAME = os.getenv("SN_USERNAME", "admin")
SN_PASSWORD = os.getenv("SN_PASSWORD", "your_password")

# Define the endpoint
INCIDENT_API_URL = f"{SN_INSTANCE}/api/now/table/incident"

# Optional filters (adjust as needed)
FILTER = "state=1^priority=1"  # New and Priority 1 incidents

# Set headers
HEADERS = {
    "Accept": "application/json"
}

def fetch_incidents():
    params = {
        "sysparm_query": FILTER,
        "sysparm_limit": 10
    }

    try:
        response = requests.get(
            INCIDENT_API_URL,
            auth=HTTPBasicAuth(SN_USERNAME, SN_PASSWORD),
            headers=HEADERS,
            params=params
        )

        if response.status_code == 200:
            incidents = response.json().get('result', [])
            print(f"\nFetched {len(incidents)} incident(s):\n")
            for incident in incidents:
                print(f"Number: {incident['number']}")
                print(f"Short Description: {incident['short_description']}")
                print(f"State: {incident['state']}")
                print(f"Priority: {incident['priority']}")
                print("-" * 40)
        else:
            print(f"Failed to fetch incidents. Status Code: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Error fetching incidents: {str(e)}")


if __name__ == "__main__":
    fetch_incidents()

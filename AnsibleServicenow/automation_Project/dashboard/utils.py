import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

SN_INSTANCE = os.getenv("SN_INSTANCE")
SN_USERNAME = os.getenv("SN_USERNAME")
SN_PASSWORD = os.getenv("SN_PASSWORD")

HEADERS = {"Accept": "application/json"}
BASE_URL = f"{SN_INSTANCE}/api/now/table/incident"


def get_incident_counts():
    if not all([SN_INSTANCE, SN_USERNAME, SN_PASSWORD]):
        raise ValueError("Missing ServiceNow credentials in .env")

    counts = {
        "New (1)": get_count_by_state("1"),
        "In Progress (2)": get_count_by_state("2"),
        "Resolved (6)": get_count_by_state("6"),
        "Closed (7)": get_count_by_state("7"),
    }
    return counts


def get_count_by_state(state_code):
    params = {
        "sysparm_query": f"state={state_code}",
        "sysparm_fields": "sys_id",
        "sysparm_limit": "1",
        "sysparm_count": "true",
    }

    response = requests.get(
        BASE_URL,
        headers=HEADERS,
        auth=HTTPBasicAuth(SN_USERNAME, SN_PASSWORD),
        params=params,
    )

    if response.status_code == 200:
        return int(response.headers.get("X-Total-Count", 0))
    else:
        return 0

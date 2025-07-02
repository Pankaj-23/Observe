import os
import requests
from requests.auth import HTTPBasicAuth

def test_servicenow_connection():
    """
    Test basic authentication and API response from ServiceNow instance.
    """

    instance = os.getenv("SERVICENOW_INSTANCE")
    user = os.getenv("SERVICENOW_USER")
    password = os.getenv("SERVICENOW_PASSWORD")

    assert instance is not None, "Missing SERVICENOW_INSTANCE env variable"
    assert user is not None, "Missing SERVICENOW_USER env variable"
    assert password is not None, "Missing SERVICENOW_PASSWORD env variable"

    url = f"{instance}/api/now/table/incident"
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, auth=HTTPBasicAuth(user, password), headers=headers)

    assert response.status_code == 200, f"Failed to connect. Status: {response.status_code}"
    json_data = response.json()
    assert "result" in json_data, "Response missing 'result' key"
    assert isinstance(json_data["result"], list), "'result' is not a list"

def test_fetch_incident_fields():
    """
    Test if required fields exist in incident records.
    """
    instance = os.getenv("SERVICENOW_INSTANCE")
    user = os.getenv("SERVICENOW_USER")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = f"{instance}/api/now/table/incident?sysparm_limit=1"
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, auth=HTTPBasicAuth(user, password), headers=headers)
    data = response.json()["result"]

    assert len(data) > 0, "No incident data returned"
    incident = data[0]

    for field in ["number", "short_description", "state", "priority"]:
        assert field in incident, f"Missing expected field: {field}"

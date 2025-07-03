import os
import unittest
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

class TestServiceNowAPI(unittest.TestCase):

    def setUp(self):
        self.instance = os.getenv("SN_INSTANCE")
        self.username = os.getenv("SN_USERNAME")
        self.password = os.getenv("SN_PASSWORD")

        self.assertIsNotNone(self.instance, "Missing SN_INSTANCE env variable")
        self.assertIsNotNone(self.username, "Missing SN_USERNAME env variable")
        self.assertIsNotNone(self.password, "Missing SN_PASSWORD env variable")

        self.url = f"{self.instance}/api/now/table/incident"
        self.headers = {
            "Accept": "application/json"
        }

    def test_connection(self):
        """Test basic authentication and API response from ServiceNow"""
        response = requests.get(
            self.url,
            auth=HTTPBasicAuth(self.username, self.password),
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200, f"Failed to connect. Status: {response.status_code}")
        json_data = response.json()
        self.assertIn("result", json_data)
        self.assertIsInstance(json_data["result"], list)

    def test_incident_fields(self):
        """Test that essential incident fields exist"""
        response = requests.get(
            f"{self.url}?sysparm_limit=1",
            auth=HTTPBasicAuth(self.username, self.password),
            headers=self.headers
        )
        data = response.json()["result"]
        self.assertGreater(len(data), 0, "No incident data returned")
        incident = data[0]
        for field in ["number", "short_description", "state", "priority"]:
            self.assertIn(field, incident, f"Missing field: {field}")

if __name__ == "__main__":
    unittest.main()

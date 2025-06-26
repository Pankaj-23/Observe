import requests
import pandas as pd
import json
import os

# Load configuration from config.json
config_path = os.path.join(os.path.dirname(__file__), '../config/config.json')
with open(config_path) as f:
    config = json.load(f)

API_KEY = config["api_key"]
BASE_URL = config["base_url"]
ORG_ID = config["org_id"]

HEADERS = {
    "X-Cisco-Meraki-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def get_networks():
    url = f"{BASE_URL}/organizations/{ORG_ID}/networks"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch networks: {response.status_code} - {response.text}")
        return []

    return response.json()

def get_devices(network_id):
    url = f"{BASE_URL}/networks/{network_id}/devices"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"[WARN] Failed to fetch devices for network {network_id}: {response.status_code}")
        return []

    return response.json()

def get_uplink_status(serial):
    url = f"{BASE_URL}/devices/{serial}/uplink"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"[WARN] Could not fetch uplink for device {serial}: {response.status_code}")
        return []

    return response.json()

def collect_health_data():
    data = []
    networks = get_networks()

    if not networks:
        print("[ERROR] No networks found. Exiting.")
        return data

    print(f"Found {len(networks)} networks. Collecting device health data...\n")

    for network in networks:
        print("RAW network object:", network)
        print("TYPE:", type(network))
        
        if not isinstance(network, dict):
            continue

        net_id = network.get("id")
        net_name = network.get("name", "Unnamed Network")
        devices = get_devices(net_id)

        for device in devices:
            serial = device.get("serial")
            name = device.get("name", "Unnamed Device")
            model = device.get("model", "Unknown Model")

            uplinks = get_uplink_status(serial)
            for uplink in uplinks:
                data.append({
                    "Network Name": net_name,
                    "Device Name": name,
                    "Model": model,
                    "Serial": serial,
                    "Interface": uplink.get("interface"),
                    "Status": uplink.get("status"),
                    "IP": uplink.get("ip"),
                    "Public IP": uplink.get("publicIp"),
                    "Gateway": uplink.get("gateway"),
                    "DNS": uplink.get("dns"),
                    "Latency": uplink.get("latency"),
                    "Loss": uplink.get("loss")
                })

    return data

def save_to_csv(data, filename="device_health_report.csv"):
    if not data:
        print("No data to write. Skipping CSV generation.")
        return

    df = pd.DataFrame(data)
    report_dir = os.path.join(os.path.dirname(__file__), '../reports')
    os.makedirs(report_dir, exist_ok=True)
    filepath = os.path.join(report_dir, filename)
    df.to_csv(filepath, index=False)
    print(f"\n✅ Report saved to: {filepath}")

if __name__ == "__main__":
    report_data = collect_health_data()
    save_to_csv(report_data)

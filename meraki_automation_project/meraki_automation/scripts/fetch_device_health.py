import requests
import pandas as pd

# Constants
API_KEY = "6fac7cc5f112b56df26fd11117cc6c2b5b9a38b0"  # Meraki Public Demo Key
ORG_ID = "549236"  # Meraki Demo Org
BASE_URL = "https://api.meraki.com/api/v1"
HEADERS = {
    "X-Cisco-Meraki-API-Key": API_KEY,
    "Content-Type": "application/json"
}


def get_networks():
    url = f"{BASE_URL}/organizations/{ORG_ID}/networks"
    response = requests.get(url, headers=HEADERS)
    return response.json()


def get_devices(network_id):
    url = f"{BASE_URL}/networks/{network_id}/devices"
    response = requests.get(url, headers=HEADERS)
    return response.json()


def get_uplink_status(serial):
    url = f"{BASE_URL}/devices/{serial}/uplink"
    response = requests.get(url, headers=HEADERS)
    return response.json()


def collect_health_data():
    data = []
    networks = get_networks()

    print(f"Found {len(networks)} networks. Collecting device health data...")

    for network in networks:
        net_id = network.get("id")
        devices = get_devices(net_id)

        for device in devices:
            serial = device.get("serial")
            name = device.get("name")
            model = device.get("model")

            try:
                uplinks = get_uplink_status(serial)

                for uplink in uplinks:
                    data.append({
                        "Network Name": network.get("name"),
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

            except Exception as e:
                print(f"[WARN] Could not fetch uplink for {serial}: {e}")

    return data


def save_to_csv(data, filename="device_health_report.csv"):
    df = pd.DataFrame(data)
    df.to_csv(f"../reports/{filename}", index=False)
    print(f"✅ Report saved: ../reports/{filename}")


if __name__ == "__main__":
    report_data = collect_health_data()
    save_to_csv(report_data)

import requests
import pandas as pd
import time

# Constants
API_KEY = "6fac7cc5f112b56df26fd11117cc6c2b5b9a38b0"
ORG_ID = "549236"
BASE_URL = "https://api.meraki.com/api/v1"
HEADERS = {
    "X-Cisco-Meraki-API-Key": API_KEY,
    "Content-Type": "application/json"
}


def get_networks():
    url = f"{BASE_URL}/organizations/{ORG_ID}/networks"
    response = requests.get(url, headers=HEADERS)
    return response.json()


def get_clients(network_id):
    url = f"{BASE_URL}/networks/{network_id}/clients?perPage=1000&timespan=86400"  # last 24 hours
    response = requests.get(url, headers=HEADERS)
    return response.json()


def collect_client_usage():
    data = []
    networks = get_networks()

    print(f"Found {len(networks)} networks. Collecting client usage data...")

    for network in networks:
        net_id = network.get("id")
        net_name = network.get("name")

        try:
            clients = get_clients(net_id)
            print(f" → {net_name}: {len(clients)} clients")

            for client in clients:
                data.append({
                    "Network Name": net_name,
                    "Client MAC": client.get("mac"),
                    "IP": client.get("ip"),
                    "Description": client.get("description"),
                    "Manufacturer": client.get("manufacturer"),
                    "Usage Sent (MB)": round(client.get("usage", {}).get("sent", 0) / (1024 * 1024), 2),
                    "Usage Recv (MB)": round(client.get("usage", {}).get("recv", 0) / (1024 * 1024), 2),
                    "Last Seen": client.get("lastSeen")
                })

            # Respect Meraki API rate limits
            time.sleep(1)

        except Exception as e:
            print(f"[WARN] Failed to fetch clients for {net_name}: {e}")

    return data


def save_to_csv(data, filename="client_usage_report.csv"):
    df = pd.DataFrame(data)
    df.to_csv(f"../reports/{filename}", index=False)
    print(f"✅ Report saved: ../reports/{filename}")


if __name__ == "__main__":
    usage_data = collect_client_usage()
    save_to_csv(usage_data)

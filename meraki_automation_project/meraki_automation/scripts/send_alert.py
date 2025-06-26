import pandas as pd
import os
from datetime import datetime

# Paths to latest alert files
ALERT_DIR = "../reports"
DEVICE_ALERT_PREFIX = "device_alerts_"
CLIENT_ALERT_PREFIX = "client_alerts_"

def get_latest_file(prefix):
    files = [f for f in os.listdir(ALERT_DIR) if f.startswith(prefix)]
    if not files:
        return None
    files.sort(reverse=True)  # Latest first
    return os.path.join(ALERT_DIR, files[0])

def notify_device_alerts(file_path):
    df = pd.read_csv(file_path)
    print("\n🚨 Device Health Alerts 🚨")
    for _, row in df.iterrows():
        print(f"[{row['Network Name']}] {row['Device Name']} ({row['Model']}) "
              f"=> Latency: {row['Latency']} ms, Loss: {row['Loss']}%")

def notify_client_alerts(file_path):
    df = pd.read_csv(file_path)
    print("\n📶 High Usage Client Alerts 📶")
    for _, row in df.iterrows():
        print(f"[{row['Network Name']}] {row['Client MAC']} (IP: {row['IP']}) "
              f"=> Usage: {row['Total Usage (MB)']} MB")


def main():
    device_file = get_latest_file(DEVICE_ALERT_PREFIX)
    client_file = get_latest_file(CLIENT_ALERT_PREFIX)

    if device_file:
        notify_device_alerts(device_file)
    else:
        print("✅ No device alerts found.")

    if client_file:
        notify_client_alerts(client_file)
    else:
        print("✅ No client alerts found.")


if __name__ == "__main__":
    main()

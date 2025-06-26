import pandas as pd
from datetime import datetime

# Thresholds (you can customize these)
LATENCY_THRESHOLD_MS = 150
LOSS_THRESHOLD_PERCENT = 2.0
CLIENT_USAGE_MB = 500  # over 500MB in last 24h

def analyze_device_health(file_path):
    print(" Analyzing device health...")
    try:
        df = pd.read_csv(file_path)
        df['Latency'] = pd.to_numeric(df['Latency'], errors='coerce')
        df['Loss'] = pd.to_numeric(df['Loss'], errors='coerce')

        alerts = df[
            (df['Latency'] > LATENCY_THRESHOLD_MS) |
            (df['Loss'] > LOSS_THRESHOLD_PERCENT)
        ]

        print(f"⚠ {len(alerts)} devices exceeded latency/loss thresholds.")
        return alerts

    except Exception as e:
        print(f"[ERROR] Failed to analyze device health: {e}")
        return pd.DataFrame()


def analyze_client_usage(file_path):
    print(" Analyzing client usage...")
    try:
        df = pd.read_csv(file_path)
        df['Total Usage (MB)'] = df['Usage Sent (MB)'] + df['Usage Recv (MB)']

        heavy_users = df[df['Total Usage (MB)'] > CLIENT_USAGE_MB]

        print(f" {len(heavy_users)} clients exceeded usage threshold.")
        return heavy_users

    except Exception as e:
        print(f"[ERROR] Failed to analyze client usage: {e}")
        return pd.DataFrame()


def save_alerts(dev_alerts, client_alerts):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not dev_alerts.empty:
        dev_alerts.to_csv(f"../reports/device_alerts_{timestamp}.csv", index=False)
        print(f" Device alerts saved to device_alerts_{timestamp}.csv")

    if not client_alerts.empty:
        client_alerts.to_csv(f"../reports/client_alerts_{timestamp}.csv", index=False)
        print(f" Client alerts saved to client_alerts_{timestamp}.csv")


if __name__ == "__main__":
    device_alerts = analyze_device_health("../reports/device_health_report.csv")
    client_alerts = analyze_client_usage("../reports/client_usage_report.csv")

    save_alerts(device_alerts, client_alerts)

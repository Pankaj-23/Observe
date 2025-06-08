import requests
import pandas as pd

def fetch_logs():
    response = requests.get("https://httpbin.org/json")
    if response.status_code == 200:
        return pd.DataFrame([response.json()])
    return pd.DataFrame()

def analyze_logs(df):
    return df[df.columns[:1]]  # dummy logic

if __name__ == "__main__":
    logs = fetch_logs()
    result = analyze_logs(logs)
    print(result)

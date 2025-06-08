import pandas as pd
from scripts.process_logs import analyze_logs


def test_analyze_logs():
    data = pd.DataFrame({"level": ["INFO", "ERROR"], "message": ["ok", "fail"]})
    result = analyze_logs(data)
    assert isinstance(result, pd.DataFrame)

import pandas as pd
from sklearn.ensemble import IsolationForest
import os

def detect_anomalies(file_path="data/system_data.csv"):
    if not os.path.exists(file_path):
        return pd.DataFrame(), pd.DataFrame()

    df = pd.read_csv(file_path)

    if len(df) < 20:
        return df, pd.DataFrame()

    model = IsolationForest(contamination=0.05, random_state=42)

    features = df[["cpu", "memory", "disk"]]
    df["anomaly"] = model.fit_predict(features)

    anomalies = df[df["anomaly"] == -1]

    return df, anomalies
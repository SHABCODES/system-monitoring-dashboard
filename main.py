import threading
from data_collector import collect_data
from anomaly_detector import detect_anomalies
from dashboard import app
import time

def run_collector():
    collect_data()

def run_dashboard():
    app.run(port=5000, debug=False, use_reloader=False)

def run_analysis():
    while True:
        df, anomalies = detect_anomalies()
        if not anomalies.empty:
            print("🚨 Anomaly Detected!")
            print(anomalies.tail())
        time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=run_collector, daemon=True).start()
    threading.Thread(target=run_dashboard, daemon=True).start()
    threading.Thread(target=run_analysis, daemon=True).start()

    while True:
        time.sleep(1)
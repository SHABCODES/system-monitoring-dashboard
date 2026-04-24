import psutil
import time
import pandas as pd
import os

DATA_FILE = "data/system_data.csv"
MAX_ROWS = 1000   # Limit file size (PRO feature)

def collect_data(interval=2):
    if not os.path.exists("data"):
        os.makedirs("data")

    # Create file with headers if not exists
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["time", "cpu", "memory", "disk"])
        df.to_csv(DATA_FILE, index=False)

    while True:
        timestamp = time.time()
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        row = pd.DataFrame([[timestamp, cpu, memory, disk]],
                           columns=["time", "cpu", "memory", "disk"])

        # Append new data
        row.to_csv(DATA_FILE, mode='a', header=False, index=False)

        # Limit file size
        df = pd.read_csv(DATA_FILE)
        if len(df) > MAX_ROWS:
            df = df.tail(MAX_ROWS)
            df.to_csv(DATA_FILE, index=False)

        print(f"[DATA] CPU:{cpu:.2f}% | MEM:{memory:.2f}% | DISK:{disk:.2f}%")

        time.sleep(interval)
# metrics_collector.py
import psutil
import time
import csv
from datetime import datetime

def collect_metrics():
    with open("metrics.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "cpu_percent", "mem_percent"])
        
        while True:
            try:
                cpu = psutil.cpu_percent(interval=1)
                mem = psutil.virtual_memory().percent
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                writer.writerow([timestamp, cpu, mem])
                f.flush()  # Force writing to file
            except Exception as e:
                print(f"Error while collecting metrics: {e}")

if __name__ == "__main__":
    collect_metrics()
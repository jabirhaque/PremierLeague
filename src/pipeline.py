import subprocess
import schedule
import time

def pipeline():
    scripts = [
        'fetch.py',
        'accumulate.py',
        'split.py',
        'train.py',
        'backtest.py',
        'upcoming_fixtures.py'
    ]

    for script in scripts:
        print(f"Running {script}...")
        subprocess.run(['python', script], check=True)
        print(f"Finished running {script}\n")

schedule.every(15).seconds.do(pipeline)

print("Pipeline scheduled to run every 15 seconds. Press Ctrl+C to stop.")

while True:
    schedule.run_pending()
    time.sleep(1)
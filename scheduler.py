# This file runs the full pipeline automatically every hour
# It also includes a notification system: if any stage fails,
# an alert is printed to the console AND written to a log file
# so failures are never silently missed.

import schedule
import time
import traceback
from datetime import datetime
from scripts.extract import extract_all
from scripts.transform import transform
from scripts.load import get_connection, create_table, load

LOG_FILE = "pipeline_alerts.log"


def send_alert(message):
    """
    Notification system: logs a clear alert whenever the pipeline fails.
    Prints to the console (visible during the live demo) and writes
    to a persistent log file so failures can be reviewed later.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert_text = f"[ALERT] {timestamp} — Pipeline failure: {message}"

    print("=" * 60)
    print(alert_text)
    print("=" * 60)

    with open(LOG_FILE, "a") as f:
        f.write(alert_text + "\n")


def run_pipeline():
    print("Starting pipeline...")

    try:
        # Step 1: Extract
        extract_all()
    except Exception as e:
        send_alert(f"EXTRACT step failed — {e}")
        traceback.print_exc()
        return  # stop here, no point continuing if extract failed

    try:
        # Step 2: Transform
        transform()
    except Exception as e:
        send_alert(f"TRANSFORM step failed — {e}")
        traceback.print_exc()
        return

    try:
        # Step 3: Load
        conn = get_connection()
        create_table(conn)
        load(conn)
        conn.close()
    except Exception as e:
        send_alert(f"LOAD step failed — {e}")
        traceback.print_exc()
        return

    print("Pipeline complete!")


# Run immediately once when we start
run_pipeline()

# Then run every hour automatically
schedule.every(1).hours.do(run_pipeline)

print("Scheduler running... press Ctrl+C to stop")

while True:
    schedule.run_pending()
    time.sleep(60)  # check every 60 seconds
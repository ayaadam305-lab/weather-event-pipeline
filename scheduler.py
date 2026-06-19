# This file runs the full pipeline automatically every hour

import schedule   # runs tasks on a timer
import time       # lets us pause between checks
import psycopg2
import os
from dotenv import load_dotenv
from scripts.extract import extract_all
from scripts.transform import transform
from scripts.load import get_connection, create_table, load

load_dotenv()

def run_pipeline():
    print("Starting pipeline...")
    
    # Step 1: Extract
    extract_all()
    
    # Step 2: Transform
    transform()
    
    # Step 3: Load
    conn = get_connection()
    create_table(conn)
    load(conn)
    conn.close()
    
    print("Pipeline complete!")

# Run immediately once when we start
run_pipeline()

# Then run every hour automatically
schedule.every(1).hours.do(run_pipeline)

print("Scheduler running... press Ctrl+C to stop")

while True:
    schedule.run_pending()
    time.sleep(60)  # check every 60 seconds
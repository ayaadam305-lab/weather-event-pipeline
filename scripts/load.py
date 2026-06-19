# This file loads the clean data into PostgreSQL database

import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

def get_connection():
    # Connect to PostgreSQL using our .env credentials
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

def create_table(conn):
    # Create the weather table if it doesn't exist yet
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id          SERIAL PRIMARY KEY,
            city        VARCHAR(100),
            country     VARCHAR(10),
            temperature FLOAT,
            feels_like  FLOAT,
            humidity    INT,
            pressure    INT,
            wind_speed  FLOAT,
            weather     VARCHAR(100),
            description VARCHAR(200),
            timestamp   TIMESTAMP
        );
    """)
    conn.commit()
    cursor.close()
    print("Table ready!")

def load(conn):
    # Read the clean CSV file
    df = pd.read_csv("data/processed/weather_clean.csv")

    cursor = conn.cursor()

    # Insert each row into the database
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO weather
            (city, country, temperature, feels_like, humidity,
             pressure, wind_speed, weather, description, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row["city"], row["country"], row["temperature"],
            row["feels_like"], row["humidity"], row["pressure"],
            row["wind_speed"], row["weather"], row["description"],
            row["timestamp"]
        ))

    conn.commit()
    cursor.close()
    print(f"Loaded {len(df)} rows into the database!")

if __name__ == "__main__":
    conn = get_connection()
    create_table(conn)
    load(conn)
    conn.close()
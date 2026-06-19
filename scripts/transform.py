import json
import pandas as pd
import os
from datetime import datetime

def transform():
    # Open the raw data file we saved in extract.py
    with open("data/raw_weather.json", "r") as f:
        raw_data = json.load(f)

    # Empty list to store each city as a clean row
    rows = []

    for city_data in raw_data:
        # Only process if the API returned valid data
        if city_data.get("cod") != 200:
            print(f"Skipping {city_data.get('name')} - invalid data")
            continue

        row = {
            "city":        city_data["name"],
            "country":     city_data["sys"]["country"],
            "temperature": city_data["main"]["temp"],
            "feels_like":  city_data["main"]["feels_like"],
            "humidity":    city_data["main"]["humidity"],
            "pressure":    city_data["main"]["pressure"],
            "wind_speed":  city_data["wind"]["speed"],
            "weather":     city_data["weather"][0]["main"],
            "description": city_data["weather"][0]["description"],
            "timestamp":   datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        rows.append(row)

    # Convert to a table
    df = pd.DataFrame(rows)

    # --- CLEANING ---
    # 1. Drop rows where city or temperature is missing
    df.dropna(subset=["city", "temperature"], inplace=True)

    # 2. Round numbers to 1 decimal place
    df["temperature"] = df["temperature"].round(1)
    df["feels_like"]  = df["feels_like"].round(1)

    # 3. Capitalize city names consistently
    df["city"] = df["city"].str.title()

    # 4. Uppercase country codes
    df["country"] = df["country"].str.upper() 
    # --- EVENT SAFETY SCORE ---
    def event_status(row):
        if row["wind_speed"] > 5 or row["temperature"] > 35 or row["humidity"] > 80:
            return "POSTPONE"
        elif row["wind_speed"] > 3 or row["temperature"] > 30 or row["humidity"] > 65:
            return "MODIFY"
        else:
            return "GO"

    df["event_status"] = df.apply(event_status, axis=1)
    # Create processed folder if it doesn't exist
    os.makedirs("data/processed", exist_ok=True)

    # Save clean data as CSV
    df.to_csv("data/processed/weather_clean.csv", index=False)

    print("Cleaned data saved to data/processed/weather_clean.csv")
    print(df)
    return df

if __name__ == "__main__":
    transform()

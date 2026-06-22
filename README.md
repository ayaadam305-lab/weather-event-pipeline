# EuroEvents GmbH — Real-Time Weather Monitoring Pipeline

An end-to-end ETL pipeline and Power BI dashboard that helps an outdoor events company decide whether to **GO**, **MODIFY**, or **POSTPONE** events across 8 major European cities, based on real-time weather conditions.

---

## Business case

**EuroEvents GmbH** runs outdoor events (concerts, festivals, markets) across Europe. Bad weather — high wind, extreme heat, heavy rain — can put guests and equipment at risk and cause costly last-minute cancellations.

This pipeline automatically collects live weather data every hour for 8 cities (London, Paris, Berlin, Madrid, Rome, Amsterdam, Vienna, Munich), evaluates each city against safety thresholds, and flags an event decision:

- 🟢 **GO** — conditions are safe
- 🟠 **MODIFY** — conditions require adjustments (e.g. reinforce structures, move indoors temporarily)
- 🔴 **POSTPONE** — conditions are unsafe for an outdoor event

This removes the need for the operations team to manually check weather across 8 cities — the decision is calculated automatically and visualized in a live dashboard.

---

## Architecture

```
OpenWeatherMap API
        │
        ▼
   extract.py        →  fetches raw weather data for 8 cities → data/raw_weather.json
        │
        ▼
  transform.py        →  cleans data with Pandas, calculates event_status
        │                  (GO / MODIFY / POSTPONE) → data/processed/weather_clean.csv
        ▼
    load.py           →  loads cleaned data into PostgreSQL (weather_db)
        │
        ▼
  scheduler.py         →  runs the full pipeline automatically every hour
        │                  (orchestration layer, built with Python's `schedule` library)
        ▼
   Power BI Online      →  2-page interactive dashboard
                            (Operations Overview + City Decision Center)
```

---

## Event decision logic

Each city is classified using the following thresholds, applied to live wind speed, temperature, and humidity:

| Condition | Status |
|---|---|
| Wind > 5 m/s, or Temp > 35°C, or Humidity > 80% | 🔴 POSTPONE |
| Wind > 3 m/s, or Temp > 30°C, or Humidity > 65% | 🟠 MODIFY |
| Otherwise | 🟢 GO |

This logic lives in `scripts/transform.py` as a derived column, `event_status`.

---

## Tech stack

| Component | Tool |
|---|---|
| Data source | [OpenWeatherMap API](https://openweathermap.org/api) |
| Language | Python 3 |
| Data cleaning | Pandas |
| Database | PostgreSQL (via Postgres.app) |
| Orchestration | Python `schedule` library — runs the full pipeline hourly |
| Visualization | Power BI Online (CSV-based, Mac-compatible) |
| Containerization (bonus) | Docker |

---

## Project structure

```
weather-pipeline/
├── scripts/
│   ├── extract.py        # Pulls live weather data from OpenWeatherMap
│   ├── transform.py      # Cleans data, calculates event_status
│   └── load.py            # Loads cleaned data into PostgreSQL
├── data/
│   ├── raw_weather.json
│   └── processed/
│       └── weather_clean.csv
├── scheduler.py            # Orchestrates the pipeline to run hourly
├── requirements.txt
├── .env                     # API key & DB credentials (not committed)
├── .gitignore
└── README.md
```

---

## How to run it

1. Clone the repository:
   ```bash
   git clone https://github.com/ayaadam305-lab/weather-event-pipeline.git
   cd weather-event-pipeline
   ```

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Create a `.env` file with your own credentials:
   ```
   OWM_API_KEY=your_openweathermap_api_key
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=weather_db
   DB_USER=your_postgres_username
   DB_PASSWORD=
   ```

4. Make sure PostgreSQL is running and `weather_db` exists.

5. Run the full pipeline once:
   ```bash
   python3 scripts/extract.py
   python3 scripts/transform.py
   python3 scripts/load.py
   ```

6. Or run the scheduler to automate it every hour:
   ```bash
   python3 scheduler.py
   ```

7. The dashboard is built in Power BI Online using `data/processed/weather_clean.csv` as the data source.

---

## Dashboard

The dashboard has two pages:

- **Operations Overview** — KPI cards (hottest city, average humidity), event status breakdown (GO/MODIFY/POSTPONE), and city-by-city weather comparisons.
- **City Decision Center** — a city slicer with a live event decision card, letting the operations team filter to any single city and see its full weather profile instantly.



---

## Author

Aya — EU Business School Munich, MADSC301 Business Intelligence, Term 3 AY 2025/26

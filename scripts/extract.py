# This file fetches weather data from the OpenWeatherMap API

import requests        # lets us make calls to websites/APIs
import json            # lets us read the data that comes back
import os              # lets us read our .env file
from dotenv import load_dotenv  # loads our secret keys from .env

# Load the secret keys from our .env file
load_dotenv()
API_KEY = os.getenv("OWM_API_KEY")  # gets your API key from .env

# The 8 cities we want weather data for
CITIES = [
    "London", "Paris", "Berlin", "Madrid",
    "Rome", "Amsterdam", "Vienna", "Munich"
]

def get_weather(city):
    # Build the URL to call the API for each city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    # Call the API and get the response
    response = requests.get(url)
    
    # Convert the response to a Python dictionary we can work with
    data = response.json()
    
    return data

def extract_all():
    all_data = []  # empty list to store all cities data
    
    for city in CITIES:
        print(f"Fetching weather for {city}...")  # shows progress
        data = get_weather(city)
        all_data.append(data)  # add this city's data to our list
    
    # Save the raw data to a file in our data/ folder
    with open("data/raw_weather.json", "w") as f:
        json.dump(all_data, f)
    
    print("Done! Raw data saved to data/raw_weather.json")
    return all_data

# This runs the extract when you run this file directly
if __name__ == "__main__":
    extract_all()

    
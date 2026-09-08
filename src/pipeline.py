import os
import re
import json
import logging

import pandas as pd
import requests
from dotenv import load_dotenv
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# ----------------------------
# Config
# ----------------------------
load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    filename="pipeline.log",
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# ----------------------------
# Clean city names
# ----------------------------
def normalize_city(city):
    city = city.strip()
    city = re.sub(r"[^a-zA-Z ]", "", city)
    city = city.title()
    return city


# ----------------------------
# Read CSV data from cities.csv file
# ----------------------------
def load_cities():
    df = pd.read_csv("data/cities.csv")

    df["city"] = df["city"].apply(normalize_city)

    #logging.info("Cities loaded successfully")
    logging_function("Cities loaded successfully", level="INFO")

    return df

#------------------------------
# Logging function
#------------------------------

def logging_function(message, level):
    if level == "INFO":
        logging.info(message)
    elif level == "WARNING":
        logging.warning(message)
    elif level == "ERROR":
        logging.error(message)
    else:
        logging.debug(message)

# ----------------------------
# API Call requests
# ----------------------------
def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation",
        "timezone": "auto",
    }

    #response = requests.get(url, params=params, timeout=30)
    response = requests.get(
    url,
    params=params,
    timeout=30,
    verify=False
)

    return response.json()


# ----------------------------
# Transform data
# ----------------------------
def build_weather_df(city, data):
    #  query parameters to fetch
    df = pd.DataFrame(
        {
            "time": data["hourly"]["time"],
            "temperature": data["hourly"]["temperature_2m"],
            "precipitation": data["hourly"]["precipitation"],
        }
    )

    df["city"] = city

    df["time"] = pd.to_datetime(df["time"])

    df["date"] = df["time"].dt.date

    return df


# ----------------------------
# Main Process
# ----------------------------
def main():
    #call load_cities() function to load cities from CSV
    cities = load_cities()
    #create an empty list to store weather data for all cities
    all_weather = []

    #Sequential loop to request data for all 16 cities contained in the cities.csv file
    
    for _, row in cities.iterrows():

        city = row["city"]

        logging_function(f"Processing {city}", level="INFO")

        weather_json = get_weather(
            row["latitude"],
            row["longitude"],
        )

        weather_df = build_weather_df(
            city,
            weather_json,
        )

        all_weather.append(weather_df)

    weather = pd.concat(all_weather)

    summary = (
        weather.groupby(["city", "date"])
        .agg(
            max_temperature=("temperature", "max"),
            total_precipitation=("precipitation", "sum"),
        )
        .reset_index()
    )

    os.makedirs("reports", exist_ok=True)

    # Excel export
    summary.to_excel(
        "reports/weather_report.xlsx",
        index=False,
    )

    # Alerts > 30C
    alerts = summary[
        summary["max_temperature"] > 30
    ]

    alerts.to_json(
        "reports/weather_alerts.json",
        orient="records",
        indent=4,
    )

    logging_function("Process completed", level="INFO")

    print("Report created successfully")


if __name__ == "__main__":
    main()
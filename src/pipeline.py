import os

# regular expressions library for string manipulation
import re

# import json
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
# Clean city names incorrect characters and formatting
# ----------------------------
def normalize_city(city):
    # remove any leading whietespaces or special characters
    city = city.strip()
    # remove any special characters and numbers, leaving only letters and spaces
    # re.sub(patron, reemplazo, texto)
    # [^a-zA-Z ] it means any character that is not a letter (a-z, A-Z) or a space
    city = re.sub(r"[^a-zA-Z ]", "", city)
    # capitalize the first letter of each word in the city name
    city = city.title()

    return city


# ----------------------------
# Read CSV data from cities.csv file
# ----------------------------
def load_cities():
    # It loads entire csv file into df variable
    df = pd.read_csv("data/cities.csv")
    # It calls the normalize_city function to clean and format the city names in the "city" column of the DataFrame
    df["city"] = df["city"].apply(normalize_city)

    # logging.info("Cities loaded successfully")
    logging_function("Cities loaded successfully", level="INFO")

    return df


# ------------------------------
# Logging function PHASE 2
# ------------------------------


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
# API Call requests PHASE 3
# ----------------------------
def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    # query parameters to fetch
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation",
        "timezone": "auto",
    }

    # response = requests.get(url, params=params, timeout=30)
    response = requests.get(url, params=params, timeout=30, verify=False)
    # It returns the weather according to latitude and longitude in JSON format
    return response.json()


# ----------------------------
# Transform data PHASE 4
# ----------------------------
def build_weather_df(city, data):
    # It receives the city name and the weather data in JSON format, and it builds a DataFrame with the relevant information

    # It creates a XLSX file with the weather data for the specified city, including time, temperature, and precipitation.
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


# ---------------------------------
# Export to Excel and JSON PHASE 5
# ---------------------------------
def export_excel(weather, filename_xlsx, filename_json):
    summary = (
        weather.groupby(["city", "date"])
        .agg(
            max_temperature=("temperature", "max"),
            total_precipitation=("precipitation", "sum"),
        )
        .reset_index()
    )
    # It creates the report folder if it doesn't exist, using os.makedirs() with exist_ok=True to avoid raising an error if the folder already exists.
    os.makedirs("reports", exist_ok=True)

    # It exports the summary DataFrame to an Excel file with the specified filename, without including the index column.
    summary.to_excel(
        filename_xlsx,
        index=False,
    )

    # It adds the alerts > 30C to alert variable and exports it to a JSON file with the specified filename, using the "records" orientation and an indentation of 4 spaces for better readability.
    alerts = summary[summary["max_temperature"] > 30]
    # it export the alerts DataFrame to a JSON file with the specified filename, using the "records" orientation and an indentation of 4 spaces for better readability.
    alerts.to_json(
        filename_json,
        orient="records",
        indent=4,
    )


# ----------------------------
# Main Process
# ----------------------------
def main():
    # call load_cities() function to load cities from CSV
    cities = load_cities()
    # create an empty list to store weather data for all cities
    all_weather = []

    # Sequential loop to request data for all 16 cities contained in the cities.csv file
    for _, row in cities.iterrows():
        city = row["city"]

        logging_function(f"Processing {city}", level="INFO")
        # Call get_weather() function to fetch weather data for the current city using its latitude and longitude
        weather_json = get_weather(
            row["latitude"],
            row["longitude"],
        )
        # Call the build_weather_df() function to create a XLSX file with the weather data for the current city, including time, temperature, and precipitation.
        weather_df = build_weather_df(
            city,
            weather_json,
        )
        # it adds the newly created DataFrame to the all_weather list, which will be used later to create a summary report.
        all_weather.append(weather_df)

    # After processing all cities, it concatenates the individual DataFrames in the all_weather list into a single DataFrame called weather, which contains the weather data for all cities.
    weather = pd.concat(all_weather)

    # Set the file names for the Excel and JSON reports, and call the export_excel() function to generate the reports based on the collected weather data.
    file_name_xlsx = "reports/weather_report.xlsx"
    file_name_json = "reports/weather_alerts.json"
    export_excel(weather, file_name_xlsx, file_name_json)

    logging_function("Process completed", level="INFO")
    print("Report created successfully")


if __name__ == "__main__":
    main()

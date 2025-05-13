import datetime
import os
from typing import List
import pandas as pd
import requests
from dotenv import load_dotenv

from .singleton import Singleton
from .models import TemperatureData, PrecipitationData, LocationWeatherData, WindData

class WeatherDataFetcher(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            load_dotenv()  # Lädt die .env-Datei
            self.api_key = os.getenv('OPENWEATHER_API_KEY')

            if not self.api_key:
                raise ValueError("API-Schlüssel nicht gefunden. Bitte stellen Sie sicher, dass eine .env-Datei mit 'OPENWEATHER_API_KEY' existiert.")

            self.initialized = True  # Verhindert mehrfache Initialisierungen
    

    def get_location_coordinates(self, city_name, state_code: str = None, country_code: str = None) -> tuple[float, float] | List[tuple[float, float]] | None:
        base_url = "http://api.openweathermap.org/geo/1.0/direct"
        
        # Konstruktion der Abfragezeichenfolge mit optionalem Bundesland- und Ländercode (ISO 3166)
        query = city_name
        if state_code:
            query += f",{state_code}"
        if country_code:
            query += f",{country_code}"
        
        params = {
            'q': query,
            'limit': 1,
            'appid': self.api_key
        }

        try:
            # Führt die API-Anfrage aus
            response = requests.get(base_url, params=params)
            response.raise_for_status() 
            data = response.json()

            if data:
                coordinates = []

                if len(data) == 1:
                    # Wenn nur ein Ergebnis zurückgegeben wird, extrahiere die Koordinaten
                    latitude      = data[0].get('lat')
                    longitude     = data[0].get('lon')
                    return (latitude, longitude)
                else:
                    for location in data:
                        latitude      = location.get('lat')  # Extrahiert die Breite
                        longitude     = location.get('lon')  # Extrahiert die Länge
                        coordinates.append((latitude, longitude))
            else:
                raise ValueError("Keine Daten für den angegebenen Ort gefunden.")

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None


    def get_weather_locaiton_forecast_data_by_coordinates(self, location_name: str, latitude: float, longitude: float) -> LocationWeatherData | None:
        base_url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.api_key,
            "exclude": "current,minutely,hourly,alerts",
            "units": "metric"
        }
        
        try:
            # Führt die API-Anfrage aus
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
        
            if data:
                temperature_data   = []
                precipitation_data = []
                wind_data          = []

                # Extrahiert für jeden Tag die Vorhersagedaten (8 Tage)
                forecast_data   = data.get("daily")
                for forecast_day in forecast_data:
                    timestamp       = forecast_day.get("dt")  # Zeitstempel der Vorhersage
                    timezone_offset = data.get("timezone_offset")  # Zeitzonen-Offset
                    
                    # Extrahiert Temperaturdaten
                    temp    = forecast_day.get("temp", {})
                    morning = temp.get("morn")  # Morgentemperatur
                    day     = temp.get("day")   # Tagestemperatur
                    evening = temp.get("eve")   # Abendtemperatur
                    night   = temp.get("night") # Nachttemperatur
                    min     = temp.get("min")   # Minimaltemperatur
                    max     = temp.get("max")   # Maximaltemperatur

                    forecast_day_temperature_data = TemperatureData(
                        timestamp,
                        timezone_offset,
                        date=datetime.date.fromtimestamp(timestamp + timezone_offset).strftime("%d.%m.%Y"),
                        morning=morning,
                        day=day,
                        evening=evening,
                        night=night,
                        min=min,
                        max=max,
                        avg=(morning + day + evening + night) / 4  # Durchschnittstemperatur
                    )
                    temperature_data.append(forecast_day_temperature_data)

                    # Extrahiert Niederschlagsdaten
                    rain        = forecast_day.get("rain", 0)  # Regenmenge
                    snow        = forecast_day.get("snow", 0)  # Schneemenge
                    probability = forecast_day.get("pop", 0)  # Niederschlagswahrscheinlichkeit

                    forecast_day_precipitation_data = PrecipitationData(
                        timestamp,
                        timezone_offset,
                        date=datetime.date.fromtimestamp(timestamp + timezone_offset).strftime("%d.%m.%Y"),
                        rain=rain,
                        snow=snow,
                        probability=probability
                    )
                    precipitation_data.append(forecast_day_precipitation_data)

                    # Extrahiert Winddaten
                    speed   = forecast_day.get("wind_speed", 0)  # Windgeschwindigkeit
                    degrees = forecast_day.get("wind_deg", 0)  # Windrichtung

                    wd = WindData(
                        timestamp,
                        timezone_offset,
                        date=datetime.date.fromtimestamp(timestamp + timezone_offset).strftime("%d.%m.%Y"),
                        speed=speed,
                        degrees=degrees
                    )
                    wind_data.append(wd)

                # Erstellt ein LocationWeatherData-Objekt, um die Wetterdaten zu speichern
                location_weather_data = LocationWeatherData(
                    location_name,
                    latitude,
                    longitude,
                    temperature_data,
                    precipitation_data,
                    wind_data
                )
                
                return location_weather_data
            else:
                raise ValueError("Keine Daten für die angegebenen Koordinaten gefunden.")

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None
        
    
    def get_weather_data_from_csv(self, file_path: str) -> LocationWeatherData | None:
        try:
            # Liest die CSV-Datei ein
            df = pd.read_csv(file_path)
            df.columns = ["date","temp_avg","temp_max","temp_min","precipitation","location_name"]
            
            # Konvertiert die Datumsangaben in das richtige Format
            df["date"] = pd.to_datetime(df["date"], format="%Y-%m")

            # Covert temperature columns to float
            df[["temp_avg", "temp_max", "temp_min", "precipitation"]] = df[["temp_avg", "temp_max", "temp_min", "precipitation"]].astype(float)

            # Replace missing values
            df["temp_max"]      = df.groupby("location_name")["temp_max"].transform(lambda x: x.fillna(x.mean()))
            df["temp_min"]      = df.groupby("location_name")["temp_min"].transform(lambda x: x.fillna(x.mean()))
            df["temp_avg"]      = df.groupby("location_name")["temp_avg"].transform(lambda x: x.fillna(x.mean()))
            df["precipitation"] = df["precipitation"].fillna(0)

            locations_weather_data = []

            grouped = df.groupby("location_name")
            for location_name, group in grouped:
                temperature_data = []
                precipitation_data = []

                for _, row in group.iterrows():
                    temp_data = TemperatureData(
                        timestamp=None,  # No timestamp in CSV
                        timezone_offset=None,  # No timezone offset in CSV
                        date=row["date"],
                        morning=None,  # No morning temperature in CSV
                        day=None,
                        evening=None,  # No evening temperature in CSV
                        night=None,  # No night temperature in CSV
                        min=row["temp_min"],
                        max=row["temp_max"],
                        avg=row["temp_avg"]
                    )
                    temperature_data.append(temp_data)

                    precip_data = PrecipitationData(
                        timestamp=None,  # No timestamp in CSV
                        timezone_offset=None,  # No timezone offset in CSV
                        date=row["date"],
                        rain=row["precipitation"],  # Assuming precipitation is rain
                        snow=0,  # No snow data in CSV
                        probability=0  # No probability data in CSV
                    )
                    precipitation_data.append(precip_data)

                # Erstellen ein LocationWeatherData-Objekt für jeden Standort
                location_weather_data = LocationWeatherData(
                    location_name=location_name,
                    temperature_data=temperature_data,
                    precipitation_data=precipitation_data
                )
                locations_weather_data.append(location_weather_data)

            return locations_weather_data

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None
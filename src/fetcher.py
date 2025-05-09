import os
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

    def get_coordinates_by_location(self, city_name, state_code: str = None, country_code: str = None, limit=1) -> tuple[float, float] | None:
        base_url = "http://api.openweathermap.org/geo/1.0/direct"
        
        # Konstruktion der Abfragezeichenfolge mit optionalem Bundesland- und Ländercode
        query = city_name
        if state_code:
            query += f",{state_code}"
        if country_code:
            query += f",{country_code}"
        
        params = {
            'q': query,
            'limit': limit,
            'appid': self.api_key
        }

        try:
            # Führt die API-Anfrage aus
            response = requests.get(base_url, params=params)
            response.raise_for_status() 
            data = response.json()

            if data:
                for location in data:
                    latitude  = location.get('lat')  # Extrahiert die Breite
                    longitude = location.get('lon')  # Extrahiert die Länge
                    return (latitude, longitude)
            else:
                raise ValueError("Keine Daten für den angegebenen Ort gefunden.")

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None

    def get_weather_forecast_data_by_coordinates(self, location_name: str, latitude: float, longitude: float) -> LocationWeatherData | None:
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
                        morning,
                        day,
                        evening,
                        night,
                        min,
                        max
                    )
                    temperature_data.append(forecast_day_temperature_data)

                    # Extrahiert Niederschlagsdaten
                    rain        = forecast_day.get("rain", 0)  # Regenmenge
                    snow        = forecast_day.get("snow", 0)  # Schneemenge
                    probability = forecast_day.get("pop", 0)  # Niederschlagswahrscheinlichkeit

                    forecast_day_precipitation_data = PrecipitationData(
                        timestamp,
                        timezone_offset,
                        rain,
                        snow,
                        probability
                    )
                    precipitation_data.append(forecast_day_precipitation_data)

                    # Extrahiert Winddaten
                    speed   = forecast_day.get("wind_speed", 0)  # Windgeschwindigkeit
                    degrees = forecast_day.get("wind_deg", 0)  # Windrichtung

                    wd = WindData(
                        timestamp,
                        timezone_offset,
                        speed,
                        degrees
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

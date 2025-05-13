from typing import List
import pandas as pd
from .models import LocationWeatherData

class WeatherHelper:
    def create_dataframe(self, data: LocationWeatherData) -> pd.DataFrame:
        
        if data.wind_data is not None:
            # Wenn Winddaten vorhanden sind, Temperatur-, Niederschlags- und Winddaten zusammenführen (API)
            temp_df = pd.DataFrame([vars(entry) for entry in data.temperature_data])
            temp_df.columns = ["timestamp", "timezone_offset", "date", "temp_morning", "temp_day", "temp_evening", "temp_night", "temp_min", "temp_max", "temp_avg"]

            precip_df = pd.DataFrame([vars(entry) for entry in data.precipitation_data])
            precip_df.drop(columns=["timezone_offset", "date"], inplace=True)

            wind_df = pd.DataFrame([vars(entry) for entry in data.wind_data])
            wind_df.columns = ["timestamp", "timezone_offset", "date", "wind_speed", "wind_degrees"]
            wind_df.drop(columns=["timezone_offset", "date"], inplace=True)

            merged_df = temp_df.merge(precip_df, on="timestamp", how="inner").merge(wind_df, on="timestamp", how="inner")

            merged_df.drop(columns=["timestamp"], errors="ignore", inplace=True)
            merged_df.drop(columns=["timezone_offset"], errors="ignore", inplace=True)
        else:
            # Wenn keine Winddaten vorhanden sind, nur Temperatur- und Niederschlagsdaten zusammenführen (CSV)
            temp_df = pd.DataFrame([vars(entry) for entry in data.temperature_data])
            temp_df.columns = ["timestamp", "timezone_offset", "date", "temp_morning", "temp_day", "temp_evening", "temp_night", "temp_min", "temp_max", "temp_avg"]
            temp_df.drop(columns=["timestamp", "timezone_offset"], inplace=True)

            precip_df = pd.DataFrame([vars(entry) for entry in data.precipitation_data])
            precip_df.drop(columns=["timestamp", "timezone_offset"], inplace=True)

            merged_df = temp_df.merge(precip_df, on="date", how="inner")

        return merged_df
    
    def normalize_dataframes_on_date(self, dataframes: List[pd.DataFrame]) -> List[pd.DataFrame]:
        # Schritt 1: Erstellen einer Liste von Mengen mit allen einzigartigen Daten aus der Spalte "date" jedes DataFrames
        date_sets = []
        for df in dataframes:
            date_sets.append(set(df["date"]))

        # Schritt 2: Berechnung der Schnittmenge aller Datums-Mengen, um gemeinsame Daten in allen DataFrames zu finden
        common_dates = set.intersection(*date_sets)

        # Schritt 3: Filtern jedes DataFrames, um nur Zeilen mit gemeinsamen Daten zu behalten, und Zurücksetzen der Indizes
        normalized = []
        for df in dataframes:
            filtered_df = df[df["date"].isin(common_dates)].reset_index(drop=True)
            normalized.append(filtered_df)

        # Schritt 4: Rückgabe der Liste der normalisierten DataFrames
        return normalized
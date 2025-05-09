from typing import List
import pandas as pd
from src.models import LocationWeatherData

class WeatherAnalyzer:
    def create_forecast_dataframe(self, data: LocationWeatherData) -> pd.DataFrame:
        # Schritt 1: Erstellen eines DataFrames für Temperaturdaten, Umbenennen der Spalten und Berechnung der Durchschnittstemperatur
        temp_df = pd.DataFrame([vars(entry) for entry in data.temperature_data])
        temp_df.rename(columns={
            "timestamp": "timestamp",
            "timezone_offset": "timezone_offset",
            "morning": "temp_morning",
            "day": "temp_day",
            "evening": "temp_evening",
            "night": "temp_night",
            "min": "temp_min",
            "max": "temp_max"
        }, inplace=True)
        temp_df["temp_avg"] = temp_df[["temp_morning", "temp_day", "temp_evening", "temp_night"]].mean(axis=1)

        # Schritt 2: Erstellen eines DataFrames für Niederschlagsdaten und Entfernen der Spalte "timezone_offset"
        precip_df = pd.DataFrame([vars(entry) for entry in data.precipitation_data])
        precip_df.drop(columns=["timezone_offset"], inplace=True)

        # Schritt 3: Erstellen eines DataFrames für Winddaten, Umbenennen der Spalten und Entfernen der Spalte "timezone_offset"
        wind_df = pd.DataFrame([vars(entry) for entry in data.wind_data])
        wind_df.columns = ["timestamp", "timezone_offset", "wind_speed", "wind_degrees"]
        wind_df.drop(columns=["timezone_offset"], inplace=True)

        # Schritt 4: Zusammenführen aller DataFrames anhand der Spalte "timestamp"
        merged_df = temp_df.merge(precip_df, on="timestamp", how="inner").merge(wind_df, on="timestamp", how="inner")

        # Schritt 5: Hinzufügen einer Spalte "date" durch Normalisieren des Timestamps und Formatieren als String
        merged_df.insert(1, "date", pd.to_datetime(merged_df["timestamp"] + merged_df["timezone_offset"], unit="s").dt.normalize().dt.strftime("%d.%m.%Y"))

        # Schritt 6: Entfernen unnötiger Spalten ("timestamp" und "timezone_offset")
        merged_df.drop(columns=["timestamp"], inplace=True)
        merged_df.drop(columns=["timezone_offset"], inplace=True)

        # Schritt 7: Rückgabe des finalen zusammengeführten DataFrames
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
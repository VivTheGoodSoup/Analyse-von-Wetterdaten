import matplotlib.pyplot as plt
import pandas as pd

class WeatherPlotter:

    # Hilfsmethode, um eine Figur und Achsen für das Plotten einzurichten
    def _setup_figure_and_axes(self):
        return plt.subplots(figsize=(12, 6))

    # Hilfsmethode, um gemeinsame Eigenschaften für Achsen festzulegen
    def _set_common_axis_properties(self, ax, title, xlabel, ylabel, xlabels):
        ax.set_title(title, fontweight='bold', pad=15)  # Titel des Plots setzen
        ax.set_xlabel(xlabel, fontweight='bold')  # Beschriftung der x-Achse setzen
        ax.set_ylabel(ylabel, fontweight='bold')  # Beschriftung der y-Achse setzen
        ax.set_xticks(xlabels)  # Positionen der x-Achsen-Ticks setzen
        ax.set_xticklabels(xlabels, rotation=90, ha='center')  # x-Achsen-Beschriftungen drehen für bessere Lesbarkeit
        ax.grid(axis="both", linestyle='--', color='gray')  # Gitterlinien hinzufügen
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))  # Legende außerhalb des Plots platzieren
        plt.tight_layout()  # Layout anpassen, um Überlappungen zu vermeiden
        plt.show()  # Plot anzeigen

    # Hilfsmethode, um gemeinsame Datumswerte aus den Standortdaten zu erhalten
    def _get_common_dates(self, location_data):
        return next(iter(location_data.values()))["date"]

    # Hilfsmethode, um Gesamtwerte (z. B. Gesamtniederschlag oder Gesamtschnee) zu plotten
    def _plot_total_value(self, location_data, column, title, ylabel, color):
        fig, ax = self._setup_figure_and_axes()
        locations = list(location_data.keys())  # Liste der Standorte abrufen
        totals = [df[column].sum() for df in location_data.values()]  # Gesamtwerte für jeden Standort berechnen
        ax.bar(locations, totals, color=color)  # Balkendiagramm erstellen
        ax.set_title(title, fontweight='bold', pad=15)  # Titel des Plots setzen
        ax.set_xlabel("Standort", fontweight='bold')  # Beschriftung der x-Achse setzen
        ax.set_ylabel(ylabel, fontweight='bold')  # Beschriftung der y-Achse setzen
        ax.grid(axis="y", linestyle='--', color='gray')  # Gitterlinien für die y-Achse hinzufügen
        plt.tight_layout()  # Layout anpassen, um Überlappungen zu vermeiden
        plt.show()  # Plot anzeigen

    # Temperaturen für eine bestimmte Tageszeit plotten
    def plot_temperatures_by_time_of_day(self, location_data: dict[str, pd.DataFrame], time_of_day: str):
        fig, ax = self._setup_figure_and_axes()
        for loc, df in location_data.items():
            ax.plot(df["date"], df[f"temp_{time_of_day}"], marker="o", label=loc) 
        dates = self._get_common_dates(location_data)
        self._set_common_axis_properties(ax, f"Temperaturen {time_of_day.capitalize()}", "Datum", "Temperatur (°C)", dates)

    # Bereich der minimalen und maximalen Temperaturen plotten
    def plot_min_max_temperatures(self, location_data: dict[str, pd.DataFrame]):
        fig, ax = self._setup_figure_and_axes()
        for loc, df in location_data.items():
            ax.fill_between(df["date"], df["temp_min"], df["temp_max"], alpha=0.3, label=f"{loc} Bereich")
        dates = self._get_common_dates(location_data)
        self._set_common_axis_properties(ax, "Temperaturbereiche", "Datum", "Temperatur (°C)", dates)

    # Durchschnittstemperaturen plotten
    def plot_avg_temperatures(self, location_data: dict[str, pd.DataFrame]):
        fig, ax = self._setup_figure_and_axes()
        for loc, df in location_data.items():
            ax.plot(df["date"], df["temp_avg"], marker="o", label=loc) 
        dates = self._get_common_dates(location_data)
        self._set_common_axis_properties(ax, "Durchschnittstemperatur", "Datum", "Temperatur (°C)", dates)

    # Windgeschwindigkeit plotten
    def plot_wind_speed(self, location_data: dict[str, pd.DataFrame]):
        fig, ax = self._setup_figure_and_axes()
        for loc, df in location_data.items():
            ax.scatter(df["date"], df["wind_speed"], alpha=0.7, label=loc)
        dates = self._get_common_dates(location_data)
        self._set_common_axis_properties(ax, "Windgeschwindigkeiten", "Datum", "Windgeschwindigkeit (km/h)", dates)
    
    # Gesamtniederschlag für jeden Standort plotten
    def plot_total_rain(self, location_data: dict[str, pd.DataFrame]):
        self._plot_total_value(location_data, "rain", "Gesamtniederschlag", "Gesamt (mm)", color='skyblue')

    # Gesamtschneefall für jeden Standort plotten
    def plot_total_snow(self, location_data: dict[str, pd.DataFrame]):
        self._plot_total_value(location_data, "snow", "Gesamtschneefall", "Gesamt (mm)", color='ivory')
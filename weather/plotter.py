import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

class WeatherPlotter:

    # Erstellt eine Figur und Achsen für das Plotten
    def _setup_figure_and_axes(self):
        return plt.subplots(figsize=(12, 6))

    # Legt gemeinsame Eigenschaften für Achsen fest (Titel, Beschriftungen, Gitter, Legende)
    def _set_common_axis_properties(self, ax, title, xlabel, ylabel, xlabels, xlabel_pos=None):
        ax.set_title(title, fontweight='bold', pad=15)
        ax.set_xlabel(xlabel, fontweight='bold')
        ax.set_ylabel(ylabel, fontweight='bold')
        if xlabel_pos is not None:
            ax.set_xticks(xlabel_pos)
        else:
            ax.set_xticks(xlabels)
        ax.set_xticklabels(xlabels, rotation=90, ha='center')
        ax.grid(axis="both", linestyle='--', color='gray')
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.show()

    # Gibt gemeinsame Datumswerte aus den Standortdaten zurück
    def _get_common_dates(self, location_data):
        return next(iter(location_data.values()))["date"]

    # Erstellt ein Balkendiagramm für Gesamtwerte (z. B. Niederschlag, Schnee)
    def _plot_total_value(self, location_data, column, title, ylabel, color):
        fig, ax = self._setup_figure_and_axes()
        locations = list(location_data.keys())
        totals = [df[column].sum() for df in location_data.values()]
        ax.bar(locations, totals, color=color)
        ax.set_title(title, fontweight='bold', pad=15)
        ax.set_xlabel("Location", fontweight='bold')
        ax.set_ylabel(ylabel, fontweight='bold')
        ax.grid(axis="y", linestyle='--', color='gray')
        plt.tight_layout()
        plt.show()

    # Plottet Temperaturen für eine bestimmte Tageszeit
    def plot_temperatures_by_time_of_day(self, location_data: dict[str, pd.DataFrame], time_of_day: str):
        fig, ax = self._setup_figure_and_axes()
        for loc, df in location_data.items():
            ax.plot(df["date"], df[f"temp_{time_of_day}"], marker="o", label=loc)
        dates = self._get_common_dates(location_data)
        self._set_common_axis_properties(ax, f"Temperatures {time_of_day.capitalize()}", "Date", "Temperature (°C)", dates)

    # Plottet den Bereich zwischen minimalen und maximalen Temperaturen
    def plot_min_max_temperatures(self, location_data: dict[str, pd.DataFrame], xlabels: list[str] = None):
        fig, ax = self._setup_figure_and_axes()
        for loc, df in location_data.items():
            ax.fill_between(df["date"], df["temp_min"], df["temp_max"], alpha=0.3, label=loc)
        dates = self._get_common_dates(location_data)
        if xlabels is not None:
            self._set_common_axis_properties(ax, "Temperature Ranges", "Date", "Temperature (°C)", xlabels, dates)
        else:
            self._set_common_axis_properties(ax, "Temperature Ranges", "Date", "Temperature (°C)", dates)

    # Plottet die Durchschnittstemperaturen
    def plot_avg_temperatures(self, location_data: dict[str, pd.DataFrame]):
        fig, ax = self._setup_figure_and_axes()
        for loc, df in location_data.items():
            ax.plot(df["date"], df["temp_avg"], marker="o", label=loc)
        dates = self._get_common_dates(location_data)
        self._set_common_axis_properties(ax, "Average Temperatures", "Date", "Temperature (°C)", dates)

    # Plottet die Windgeschwindigkeit
    def plot_wind_speed(self, location_data: dict[str, pd.DataFrame]):
        fig, ax = self._setup_figure_and_axes()
        for loc, df in location_data.items():
            ax.scatter(df["date"], df["wind_speed"], alpha=0.7, label=loc)
        dates = self._get_common_dates(location_data)
        self._set_common_axis_properties(ax, "Wind Speeds", "Date", "Wind Speeds (km/h)", dates)

    # Plottet den Gesamtniederschlag für jeden Standort
    def plot_total_rain(self, location_data: dict[str, pd.DataFrame]):
        self._plot_total_value(location_data, "rain", "Total Rain", "Total (mm)", color='skyblue')

    # Plottet den Gesamtschneefall für jeden Standort
    def plot_total_snow(self, location_data: dict[str, pd.DataFrame]):
        self._plot_total_value(location_data, "snow", "Total Snow", "Total (mm)", color='ivory')


    # Plottet die Heatmap für die Durchschnittstemperaturen
    def plot_combined_heatmap(self, df: dict[str, pd.DataFrame]) -> None:
        locations   = ", ".join(df.keys())
        combined_df = pd.concat([data.assign(location=loc) for loc, data in df.items()], ignore_index=True)
        combined_df["location_date"] = combined_df['location'] + " " + combined_df['year'].astype(str)
        pivot_table = combined_df.pivot_table(values="temp_avg", index="location_date", columns="month")

        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="coolwarm")
        plt.title(f"Monatliche Durchschnittstemperaturen {locations}")
        plt.xlabel("Monat")
        plt.ylabel("Stadt & Jahr")
        plt.tight_layout()
        plt.show()

    # Plottet die monatlichen Durchschnittstemperaturen für jeden Standort
    def plot_city_heatmap(self, location_name: str, location_dataframe: pd.DataFrame) -> None:
        location_dataframe["date"]  = pd.to_datetime(location_dataframe["date"])
        location_dataframe["year"]  = location_dataframe["date"].dt.year
        location_dataframe["month"] = location_dataframe["date"].dt.month

        pivot_table = location_dataframe.pivot_table(values="temp_avg", index="year", columns="month")

        plt.figure(figsize=(10, 6))
        sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="coolwarm")
        plt.title(f'Monatliche Durchschnittstemperaturen in {location_name} (°C)')
        plt.xlabel('Monat')
        plt.ylabel('Jahr')
        plt.tight_layout()
        plt.show()
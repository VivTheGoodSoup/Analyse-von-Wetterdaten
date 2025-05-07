import pandas as pd

import numpy as np

#Analyse von Wetterdaten - Staedte: Zuerich, Helsinki und Singapur

#Pfad zur CSV-Datei
csv_path = "data/wetterdaten_2024_drei_staedte.csv"

#Laden der Datei mit Pandas
df = pd.read_csv(csv_path) 

'''
#Spalten anzeigen
print("Spaltennamen:")
print(df.columns)
'''
#Datumsspalte als datetime konvertieren
df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m")

#Temperaturwerte als float behandeln
df[["TAVG", "TMAX", "TMIN", "PRCP"]] = df[["TAVG", "TMAX", "TMIN", "PRCP"]].astype(float)

'''
#Fehlende Werte suchen
print("Fehlende Werte pro Spalte:")
print(df.isnull().sum())
'''
#Fehlenden TMAX Wert mit dem Mittelwert der gleichen Stadt ersetzen
df["TMAX"] = df.groupby("CITY")["TMAX"].transform(lambda x: x.fillna(x.mean()))

# Heathmap ergänzen
#Test Saskia
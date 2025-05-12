# Analyse-von-Wetterdaten

## Beschreibung
Unser Projekt ist eine Anwendung zur Analyse und Visualisierung von Wettervorhersagen-Daten (`daily` 8 Tage Vorhersage) der One Call API von OpenWeatherMap.

## Installation

Um das Projekt auf deinem lokalen Rechner zum Laufen zu bringen, folge bitte diesen Schritten:

### 1. Repository klonen

Klone das GitHub-Repository an dem gewünschten Ort und wechsle dann ich den Ordner des erstellten Repos:


```bash
git clone https://github.com/VivTheGoodSoup/Analyse-von-Wetterdaten.git
cd Analyse-von-Wetterdaten
```

### 2. Virtuelle Umgebung erstellen

Erstelle eine virtuelle Umgebung, um die Python-Abhängigkeiten isoliert zu installieren:

```bash
python -m venv .venv
```
Dies erstellt einen Ordner namens .venv, der deine virtuelle Umgebung enthält.

### 3. Virtuelle Umgebung erstellen
Aktiviere die virtuelle Umgebung, um sicherzustellen, dass du die Pakete nur in diesem speziellen Kontext installierst:

Windows (PowerShell):

```bash
.\.venv\Scripts\Activate.ps1
```

Windows (CMD):

```bash
.\.venv\Scripts\activate.bat
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Wenn die Umgebung erfolgreich aktiviert wurde, siehst du den Präfix (.venv) in deinem Terminal-Prompt.

### 4. Dependencies installieren
Installiere alle erforderlichen Pakete, die für das Projekt notwendig sind:

```bash
pip install -r requirements.txt
```

### 5. API-Schlüssel einrichten
1. Gehe auf [OpenWeatherMap](https://openweathermap.org/api) und melde dich an, um einen API-Schlüssel zu erhalten.
2. Nach der Anmeldung kannst du deinen API-Schlüssel unter "API keys" in deinem Benutzer-Dashboard einsehen.
3. Erstelle eine `.env`-Datei im Root-Verzeichnis deines Projekts.
4. Füge deinen API-Schlüssel in der `.env`-Datei hinzu: `OPENWEATHER_API_KEY=dein_api_schluessel_hier`

### 6. Projekt ausführen
Jetzt kannst du das weather Notebook öffnen und das Projekt ausprobieren.

⚠️ Falls du das Projekt in VS-Code öffnest, musst du evtl. mit `Strg+Shift+P` den richtigen Python Interpreter auswählen (.venv).
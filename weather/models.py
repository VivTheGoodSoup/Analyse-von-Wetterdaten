import datetime

class WeatherData:
    def __init__(
            self, 
            timestamp: int = None,
            timezone_offset: int = None,
            date: datetime.date = None
        ):
        self.timestamp       = timestamp
        self.timezone_offset = timezone_offset
        self.date            = date

    def __repr__(self):
        attrs = ""
        for attr, value in vars(self).items():
            attrs += f"  {attr}={value}\n"
        return f"{self.__class__.__name__}(\n{attrs}\n)"

class TemperatureData(WeatherData):
    def __init__(
        self, 
        timestamp: int = None, 
        timezone_offset: int = None,
        date: datetime.date = None,
        morning: float = None,
        day: float = None,
        evening: float = None,
        night: float = None,
        min: float = None,
        max: float = None,
        avg: float = None
    ):
        super().__init__(timestamp, timezone_offset, date)
        self.morning = morning
        self.day     = day
        self.evening = evening
        self.night   = night
        self.min     = min
        self.max     = max
        self.avg     = avg

class PrecipitationData(WeatherData):
    def __init__(
        self, 
        timestamp: int = None,
        timezone_offset: int = None,
        date: datetime.date = None,
        rain: float = None,
        snow: float = None,
        probability: float = None
    ):
        super().__init__(timestamp, timezone_offset, date)
        self.rain        = rain
        self.snow        = snow
        self.probability = probability


class WindData(WeatherData):
    def __init__(
        self,
        timestamp: int = None,
        timezone_offset: int = None,
        date: datetime.date = None,
        speed: float = None,
        degrees: float = None
    ):
        super().__init__(timestamp, timezone_offset, date)
        self.speed   = speed
        self.degrees = degrees


class LocationWeatherData:
    def __init__(
        self,
        location_name: str,
        latitude: float = None,
        longitude: float = None,
        temperature_data: TemperatureData | list[TemperatureData] = None,
        precipitation_data: PrecipitationData | list[PrecipitationData] = None,
        wind_data: WindData | list[WindData] = None
    ):
        self.location_name      = location_name
        self.latitude           = latitude
        self.longitude          = longitude
        self.temperature_data   = temperature_data
        self.precipitation_data = precipitation_data
        self.wind_data          = wind_data

    def __repr__(self):
        attrs = ""
        for attr, value in vars(self).items():
            attrs += f"  {attr}={value}\n"
        return f"{self.__class__.__name__}(\n{attrs}\n)"

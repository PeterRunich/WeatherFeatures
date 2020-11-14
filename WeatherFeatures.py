#https://openweathermap.org/api/one-call-api docs api.
import requests
from datetime import datetime, timedelta, timezone

# Default units: unix time, temp: kelvin, pressure: hPa, humidity: %, dew_point: kelvin, wind_speed: metre/sec, wind_deg': degrees.
FEATURES = ['dt', 'temp', 'pressure', 'humidity', 'dew_point', 'wind_speed', 'wind_deg']

class WeatherFeatures:
    def __init__(self, lat, lon):
        self.latitude  = lat
        self.longitude = lon
        self.api_key   = '9de243494c0b295cca9337e1e96b00e2' # TODO: вынести api_key к переменным среды.

    @classmethod
    def call(cls, *args):
        return cls(*args).get_features()
    
    def get_features(self) -> dict:
        next_hour = int((datetime.now().replace(microsecond=0, second=0, minute=0) + timedelta(hours=1)).timestamp()) # Return unix timestamp.

        # Optional add units={units} where units (standard, metric and imperial). More info https://openweathermap.org/weather-data.
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={self.latitude}&lon={self.longitude}&exclude=daily,minutely,current&appid={self.api_key}"

        response = requests.get(url)
        next_hour_data = list(filter(lambda x: x['dt'] == next_hour, response.json()['hourly']))[0]
        return { key: next_hour_data[key] for key in next_hour_data if key in FEATURES } # Return only useful features.

# Test.
# print(WeatherFeatures.call(48.069, 39.972))
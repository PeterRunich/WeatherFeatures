# -*- coding: utf-8 -*-
"""
This module is used to obtain next hour weather conditions, by a coordinates from openweathermap.org.
See details about openweathermap.org API at
https://openweathermap.org/api/one-call-api.
"""

import requests
import datetime as dt
from typing import List, TypeVar

#: TypeVar: Generic for short type hint, int and float.
Numeric = TypeVar('Numeric', int, float)

class WeatherFeatures:
    """Is used to obtain next hour weather conditions by a coordinates.

    Attributes:
        latitude(Numeric): Latitude of your point.
        longitude(Numeric): Longitude of your point.

    """

    #: list of str: List of useful features, needed for filtration.
    _FEATURES = ['dt', 'temp', 'pressure', 'humidity', 'dew_point', 'wind_speed', 'wind_deg']

    def __init__(self, lat: Numeric, lon: Numeric) -> None:
        self.latitude  = lat
        self.longitude = lon

        #: str: Key to access the openweathermap.org API.
        self.api_key   = '9de243494c0b295cca9337e1e96b00e2' #: TODO: Need to move api_key to the environment variables.

    @classmethod
    def call(cls, *args) -> dict:
        """Short cut for invoke the method to create instance and call get_features.

        Note:
            First argument must be latitude, second longitude

        Examples:
            An invoke method by .call and send args latitude and longitude, it will return dict of weather conditions.

            >>> WeatherFeatures.call(48.069, 39.972)
            {'dt': 1609689600, 'temp': 273.87, 'pressure': 1033, 'humidity': 96, 'dew_point': 273.31, 'wind_speed': 5.29, 'wind_deg': 120}

        Returns:
            Dict of weather conditions.  

        """
        return cls(*args).get_features()
    
    def get_features(self) -> dict:
        """Is used to obtain next hour weather conditions by a coordinates.

        Note:
            For simple, you should use method .call check it out.

        Returns:
            Dict of weather conditions.  

        """
        next_hour = int((dt.datetime.now().replace(microsecond=0, second=0, minute=0) + dt.timedelta(hours=1)).timestamp()) #: Return unix timestamp.

        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={self.latitude}&lon={self.longitude}&exclude=daily,minutely,current&appid={self.api_key}" #: Optional add units={units} where units (standard, metric and imperial). More info https://openweathermap.org/weather-data.

        response = requests.get(url)
        next_hour_data = list(filter(lambda x: x['dt'] == next_hour, response.json()['hourly']))[0]
        return { key: next_hour_data[key] for key in next_hour_data if key in _FEATURES }
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import requests

class WeatherDataDownload:
    """
    Downloads historical weather and today's weather forecast for a given 
    city, information taken from Open-Meteo API.

    Attributes
    ----------
    city_name : str
        The name of the city that weather data will be downloaded for.
    latitude : float
        The latitude of the given city.
    longitude: float
        The longitude of the given city.
    daily_temperature_2m_max : list of float
        The historical list of maximum daily temperatures(°F) for the city
        for a given year.
    daily_temperature_2m_min : list of float
        The historical list of minimum daily temperatures(°F) for the city 
        for a given year.
    today_max_day_temp : float
        The forecasted maximum temperature(°F) for the city for today.
    today_min_night_temp : float
        The forecasted minimum temperature(°F) for the city for tonight.

    Methods
    -------
    __init_(city_name)
        Initializes the class instance with the given city name and retrieves 
        the city's latitude and longitude coordinates.
    find_lat_long()
        Finds the latitude and longitude for the given city using the Open-
        Meteo geocoding API.
    get_historical_data(year=2023)
        Downloads the historical weather data (daily max and min 
        temperatures) of the given city for the given year, defaults to 2023 
        data.
    get_forecast_data()
        Downloads the weather forecast for the given city for today, 
        including max and min temperatures.
    
    """

    
    def __init__(self, city_name):
        """
        Initializes the class instance with the given city name and retrieves 
        the city's latitude and longitude coordinates.

        Parameters
        ----------
        city_name : str
            The name of the city that weather data will be downloaded for.
        """
        self.city_name = city_name
        latlong = self.find_lat_long()
        self.latitude = latlong[0]
        self.longitude = latlong[1]
        self.daily_temperature_2m_max = [] #list for max temps
        self.daily_temperature_2m_min = [] #list for min temps

    
    def find_lat_long(self):
        """
        External code was moderately adapted to fit the purpose of this class 
        and the WeatherDataStatistics class.
        External Source: DONT FORGET ABOUT THIS OK ASK DAD FOR THE EXTERNAL 
        CODE SOURCE
        Finds the latitude and longitude for the given city using the Open-
        Meteo geocoding API.

        Returns
        -------
        list of str
            A list containing the latitude and longitude as strings. If the 
            city is not found, it says it cannot find the given city.
        """
        #Send a request to Open-Meteo geocoding API to fetch the city's 
        #location data
        result_city = requests.get(url =
        'https://geocoding-api.open-meteo.com/v1/search?name=' + 
        self.city_name + '&count-1&language=en&format=json')
        location = result_city.json()

        #If results exist, extract the city's latitude and longitude data
        if 'results' in location:
            latitude = str(location['results'][0]['latitude'])
            longitude = str(location['results'][0]['longitude'])
            return [latitude, longitude]

        #If results do not exist, tell the user that the location was not 
        #found
        else:
            print('LOCATION', self.city_name, 'NOT FOUND :(')
            return [0, 0]

    
    def get_historical_data(self, year=2023):
        """
        External code was moderately adapted to fit the purpose of this class 
        and the WeatherDataStatistics class.
        External Code Source: https://open-meteo.com/en/docs/historical-
        weather-api#latitude=32.8473&longitude=-117.2742&start_date=2022-01-
        01&end_date=2022-12-31&hourly=&daily=temperature_2m_max,temperature_
        2m_min&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_
        unit=inch&timezone=America%2FLos_Angeles
        
        Downloads the historical weather data (daily max and min 
        temperatures) of the given city for the given year, defaults to 2023 
        data.

        Parameters
        ----------
        year : int, optional
            Historical data for the given city will be retrieved from this 
            year, defaults to 2023.

        Returns
        -------
        None
            The data is saved as instance variables 
            `daily_temperature_2m_max` and `daily_temperature_2m_min`. 
        """
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache',
                        expire_after = -1)
        retry_session = retry(cache_session, retries = 5,
                        backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)

        start_year_date = f'{year}-01-01'  # Jan 1 of the given year
        end_year_date = f'{year}-12-31'  # Dec 31 of the given year
        
        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign 
        #them correctly below
        url = 'https://archive-api.open-meteo.com/v1/archive'
        params = {
        	'latitude': self.latitude,
        	'longitude': self.longitude,
            'start_date': start_year_date,
        	'end_date': end_year_date,
        	'daily': ['temperature_2m_max', 'temperature_2m_min'],
        	'temperature_unit': 'fahrenheit',
        	'wind_speed_unit': 'mph',
        	'precipitation_unit': 'inch',
        	'timezone': 'America/Los_Angeles'
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or 
        #weather models
        response = responses[0]
        '''print(f'Coordinates {response.Latitude()}°N {response.Longitude()}
        °E')
        print(f'Elevation {response.Elevation()} m asl')
        print(f'Timezone {response.Timezone()} 
        {response.TimezoneAbbreviation()}')
        print(f'Timezone difference to GMT+0 {response.UtcOffsetSeconds()} 
        s')'''

        # Process daily data. The order of variables needs to be the same as 
        #requested.
        daily = response.Daily()
        self.daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
        self.daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
        

    def get_forecast_data(self):
        """
        External code was moderately adapted to fit the purpose of this class 
        and the WeatherDataStatistics class.
        External Code Source: https://open-meteo.com/en/docs#latitude=32.
        8473&longitude=-117.2742&hourly=&daily=temperature_2m_max,
        temperature_2m_min&temperature_unit=fahrenheit&wind_speed_unit=
        mph&precipitation_unit=inch&timezone=America%2FLos_Angeles
        &forecast_days=1
        
        Downloads the weather forecast for the given city for today, 
        including max and min temperatures.

        Returns
        -------
        None
            The data is saved as instance variables `today_max_day_temp` and 
            `today_min_night_temp`.
        """
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 
                        3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 
                        0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign 
        #them correctly below
        url = 'https://api.open-meteo.com/v1/forecast'
        params = {
        	'latitude': self.latitude,
        	'longitude': self.longitude,
        	'daily': ['temperature_2m_max', 'temperature_2m_min'],
        	'temperature_unit': 'fahrenheit',
        	'wind_speed_unit': 'mph',
        	'timezone': 'America/Los_Angeles',
        	'forecast_days': 1
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or 
        #weather models
        response = responses[0]
        '''print(f'Coordinates {response.Latitude()}°N {response.Longitude()}
        °E')
        print(f'Elevation {response.Elevation()} m asl')
        print(f'Timezone {response.Timezone()} 
        {response.TimezoneAbbreviation()}')
        print(f'Timezone difference to GMT+0 {response.UtcOffsetSeconds()} 
        s')'''

        # Process daily data. The order of variables needs to be the same as 
        #requested.
        daily = response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
        self.today_max_day_temp = daily_temperature_2m_max[0]
        self.today_min_night_temp = daily_temperature_2m_min[0]
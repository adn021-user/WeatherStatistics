import datetime
from weather_data_download import WeatherDataDownload

class WeatherDataStatistics:
    """
    Manipulates statistical weather data for daily maximum and minimum 
    temperatures to compare with historical data for a given city. Data is 
    retrieved from the methods in WeatherDataDownload.

    Attributes
    ----------
    city_name : str
        The name of the given city, the data for which this class will 
        analyze.
    max_day_temp_month : float
        The historical highest daily maximum temperature recorded for the 
        given month.
    min_day_temp_month : float
        The historical lowest daily maximum temperature recorded for the 
        given month.
    max_night_temp_month : float
        The historical highest daily minimum temperature recorded for the 
        given month.
    min_night_temp_month : float
        The historical lowest daily minimum temperature recorded for the 
        given month.

    Methods
    -------
    __init__(city_name)
        Initializes the class instance with the given city name.
    find_lat_long()
        Finds the latitude and longitude for the given city using the Open-
        Meteo geocoding API, same as in WeatherDataDownload.
    extract_data_for_month(daily_extreme, month)
        Made for match_against_historical_weather(), extracts the daily 
        extreme temperatures for the given month.
    max_temp(daily_temp)
        Finds the max temperature from a list of temperatures.
    min_temp(daily_temp)
        Finds the min temperature from a list of temperatures.
    match_against_historical_weather(today_month, year=2023)
        Compares today's temperatures against historical data for a given 
        month and year.
    compare_day_temps(today_max_day_temp)
        Compares today's maximum daytime temperature to the historical data 
        for the given month.
    compare_night_temps(today_min_night_temp)
        Compares today's minimum nighttime temperature to the historical data 
        for the given month.
    print_range(low_temp, high_temp, today_temp)
        Prints a nice visual of a range of temperatures from low to high, 
        including today's temperature.
    print_range_recursive(i)
        Made for print_range(), uses recursion to print a temperature range 
        with markers for today's temperature.
    """

    def __init__(self, city_name):
        """
        Initializes the class instance with the given city name.

        Parameters
        ----------
        city_name : str
            The name of the city, this class aims to analyze the city's 
            weather data.
        """
        self.city_name = city_name

    #Locates city_name to a real world city with latitude and longitude 
    #coordinates
    def find_lat_long(self):
        """
        Finds the latitude and longitude for the given city using the Open-
        Meteo geocoding API, same as in WeatherDataDownload.

        Returns
        -------
        list of str
            A list containing the latitude and longitude as strings. If the 
            city is not found, it says it cannot find the given city.
        """
        #Send a request to Open-Meteo geocoding API to fetch the city's 
        #location data
        result_city = requests.get(
            url =
            'https://geocoding-api.open-meteo.com/v1/search?name=' + 
            self.city_name + '&count-1&language=en&format=json'
                                  )
        
        location = result_city.json()
        
        #If results exist, extract the city's latitude and longitude data
        if 'results' in location:
            longitude = str(location['results'][0]['longitude'])
            latitude = str(location['results'][0]['latitude'])
            return [latitude, longitude]

        #If results do not exist, tell the user that the location was not 
        #found
        else:
            print('LOCATION', self.city_name, 'NOT FOUND :(')
            return [0, 0]
    
    def extract_data_for_month(self, daily_extreme, month):
        """
        Made for match_against_historical_weather(), extracts the daily 
        extreme temperatures for the given month.

        Parameters
        ----------
        daily_extreme : list of float
            A list of daily extreme temperatures for the year.
        month : int
            The month for which data is to be extracted (1 = January, 2 = 
            February, ..., 12 = December).

        Returns
        -------
        list of float
            A list of daily extreme temperatures for the specified month.
        """
        days_prior = 0
        days_per_month = [31, 28, 31, 30, 31, 30, 30, 31, 30, 31, 30, 31] 
        for idx, i in enumerate(days_per_month):
            if idx + 1 >= month:
                break
            else:
                days_prior = days_prior + i
        
        return daily_extreme[
        days_prior : days_prior + days_per_month[month-1] : 1
        ]

    def max_temp(self, daily_temp): 
        """
        Finds the max temperature from a list of temperatures.

        Parameters
        ----------
        daily_temp : list of float
            A list of daily temperatures.

        Returns
        -------
        float
            The maximum temperature found in the list.
        """
        max_temp = -1000 #impossibly cold initial temperature that any city 
        #on Earth can not be  
        for i in daily_temp:
            if i > max_temp:
                max_temp = i
        return max_temp

    def min_temp(self, daily_temp): 
        """
        Finds the min temperature from a list of temperatures.

        Parameters
        ----------
        daily_temp : list of float
            A list of daily temperatures.

        Returns
        -------
        float
            The minimum temperature found in the list.

        """
        min_temp = 1000 #impossibly warm initial temperature that any city on 
        #Earth can not be
        for i in daily_temp:
            if i < min_temp:
                min_temp = i
        return min_temp

    def match_against_historical_weather(self, today_month, year=2023):
        """
        Compares today's temperatures against historical data for a given 
        month and year.

        Parameters
        ----------
        today_month : int
            The current month (1 = January, 2 = February, ..., 12 = December).
        year : int, optional
            The year for which historical data is to be used, default is 2023.

        Returns
        -------
        None
            Returns nothing but prints out statistical information about the 
            given city's historical data.
        """
        #Placeholder instances to download historical weather
        temporary_downloader = WeatherDataDownload(self.city_name)
        temporary_downloader.get_historical_data(year)

        #Extract temperatures for the given month
        max_temps_month = self.extract_data_for_month(
            temporary_downloader.daily_temperature_2m_max, today_month
        )
        min_temps_month = self.extract_data_for_month(
            temporary_downloader.daily_temperature_2m_min, today_month
        )

        #Find the max/min temperatures of the day and the night for the given 
        #month
        self.max_day_temp_month = self.max_temp(max_temps_month)
        self.min_day_temp_month = self.min_temp(max_temps_month)
        self.max_night_temp_month = self.max_temp(min_temps_month)
        self.min_night_temp_month = self.min_temp(min_temps_month)

        #Print out the analyzed historical data
        print('Max Day Temperature of the Month:   ' ,
              self.max_day_temp_month)
        print('Min Day Temperature of the Month:   ' ,
              self.min_day_temp_month)
        print('Max Night Temperature of the Month: ' ,
              self.max_night_temp_month)
        print('Min Night Temperature of the Month: ' ,
              self.min_night_temp_month)
        
        
    def compare_day_temps(self, today_max_day_temp):
        """
        Compares today's maximum daytime temperature to the historical data 
        for the given month.

        Prints out a message in human language comparing today's temperature 
        with historical data. It also prints out a nice visual of today's 
        temperature in comparision to historical data.

        Parameters
        ----------
        today_max_day_temp : float
            The maximum daytime temperature for today.

        Returns
        -------
        str
            A message indicating how today's daytime temperature compares to 
            historical data. It also prints out a visual of today's daytime 
            temperatures in comparision to historical records.
        """
        #Calculate the month's previous temperature range
        range_day_temp = self.max_day_temp_month - self.min_day_temp_month

        #Calculate statistic quartiles
        quartile_1d = range_day_temp / 4 + self.min_day_temp_month
        quartile_2d =  range_day_temp / 2 + self.min_day_temp_month
        quartile_3d =  range_day_temp * 3 / 4 + self.min_day_temp_month
        
        #Print out the range visual
        self.print_range(self.min_day_temp_month, self.max_day_temp_month,
                         today_max_day_temp)

        #Present a message after comparing today's temperature to history
        if today_max_day_temp > self.max_day_temp_month:
            message = 'Record heat in the day for this month'

        elif today_max_day_temp > quartile_3d:
            message = 'Considerably warm in the day for this month'

        elif today_max_day_temp > quartile_2d:
            message = 'Moderately warm in the day for this month'

        elif round(today_max_day_temp) == round(quartile_2d):
            message = 'Average temperature in the day for this month'
        
        elif today_max_day_temp > quartile_1d:
            message = 'Moderately cold in the day for this month'

        elif today_max_day_temp > self.min_day_temp_month:
            message = 'Considerably cold in the day for this month'

        elif today_max_day_temp <= self.min_day_temp_month:
            message = 'Extremely cold in the day for this month'

        print(message)
        return message


    def compare_night_temps(self,today_min_night_temp):
        """
        Compares today's minimum nighttime temperature to the historical data 
        for the given month.

        Prints out a message in human language comparing today's temperature 
        with historical data. It also prints out a nice visual of today's 
        temperature in comparision to historical data.
        
        Parameters
        ----------
        today_min_night_temp : float
            The maximum nighttime temperature for today.

        Returns
        -------
        str
            A message indicating how today's nighttime temperature compares 
            to historical data. It also prints out a visual of today's 
            nighttime temperatures in comparision to historical records.
        """
        #Calculate the month's previous temperature range
        range_night_temp = (
        self.max_night_temp_month - self.min_night_temp_month)
            
        #Calculate statistic quartiles
        quartile_1n = range_night_temp / 4 + self.min_night_temp_month
        quartile_2n =  range_night_temp / 2 + self.min_night_temp_month
        quartile_3n =  range_night_temp * 3 / 4 + self.min_night_temp_month

        #Print out the range visual
        self.print_range(self.min_night_temp_month, 
                         self.max_night_temp_month, today_min_night_temp)

        #Present a message after comparing today's temperature to history
        if today_min_night_temp < self.min_night_temp_month:
            message = 'Record cold at night for this month'

        elif today_min_night_temp < quartile_1n:
            message = 'Considerably cold at night for this month'

        elif today_min_night_temp < quartile_2n:
            message = 'Moderately cold at night for this month'

        elif round(today_min_night_temp) == round(quartile_2n):
            message = 'Average temperature at night for this month'
        
        elif today_min_night_temp < quartile_3n:
            message = 'Moderately warm at night for this month'

        elif today_min_night_temp < self.max_night_temp_month:
            message = 'Considerably warm at night for this month'

        elif today_min_night_temp >= self.max_night_temp_month:
            message = 'Extremely hot at night for this month'
        
        print(message)
        return message

    
    def print_range(self, low_temp, high_temp, today_temp):
        """
        Prints a nice visual of a range of temperatures from low to high with 
        today's temperature, looks something like:
            low_temp----------------------------(today_temp)-------------
            high_temp

        If today's temperature is below the historical lowest temperature, it 
        will show outside the range on the left, becoming the new lowest 
        temperature. If today's temperature is above the historical highest 
        temperature, it will show outside the range on the right, becoming 
        the new highest temperature.

        Parameters
        ----------
        low_temp : float
            The historical lowest temperature in the range.
        high_temp : float
            The historical highest temperature in the range.
        today_temp : float
            The temperature for today, which will be displayed along the 
            dotted range.

        Returns
        -------
        None
            Prints the temperature range.
        """
        
        #Round all temperatures to nearest integer
        self.low_temp = round(low_temp)
        self.high_temp = round(high_temp)
        self.today_temp = round(today_temp)

        #Create the bounds of the range's visuals
        self.start_range = self.low_temp
        self.end_range = self.high_temp
        
        #Change the start or end of the range if today's temperature is more 
        #extreme than the historical extremes
        if today_temp < low_temp:
            self.start_range = self.today_temp
        elif today_temp > high_temp:
            self.end_range = self.today_temp 

        #Print the range
        self.print_range_recursive(self.start_range)
        print('') #print a new line after the visual


    def print_range_recursive(self, i):
        """
        Made for print_range(), uses recursion to print a temperature range 
        with markers for today's temperature.

        Forms a recursive range starting at `i` and ending at 
        `self.end_range`. It prints the historical lowest and highest 
        temperatures at their respective positions and reveals the position 
        of today's temperature. Any other temperature is displayed as a dash 
        to visualize the temperature distances between the important 
        temperatures.
        
        Parameters
        ----------
        i (int) :
            The current index or starting temperature in the range. The 
            recursion will start at this value.

        Returns
        -------
        None
            Prints the visuals
        """
        #If the temperature gets bigger than the upper range, end recursion
        if i > self.end_range:
            return
        
        #Print today's temperature
        if i == self.today_temp:
            print(f'(today {self.today_temp}F)', end=' ')
    
        #Print the low temperature
        elif i == self.low_temp:
            print(f'{self.low_temp}F', end=' ')
        
        #Print the high temperature
        elif i == self.high_temp:
            print(f'{self.high_temp}F', end=' ')
        
        #For all other temperatures in the range, print dashes
        else:
            print('-', end=' ')

        #Use recursion to call the function with the next temperature in the 
        #range
        self.print_range_recursive(i + 1)
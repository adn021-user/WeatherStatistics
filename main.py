from weather_data_download import WeatherDataDownload
from weather_data_statistics import WeatherDataStatistics

#To run this program, input 2 parameters:
city = 'La Jolla' #where the weather data will be downloaded from
month = 12 #the current month for current weather, or other inputted months
            #for comparision


#Here is an example of how the code should be run to collect historical
#weather data and compare with today's weather

weather_downloader = WeatherDataDownload(city)
weather_downloader.get_historical_data()
weather_downloader.get_forecast_data()
weather_stat = WeatherDataStatistics(city)

weather_stat.match_against_historical_weather(month)

weather_stat.compare_day_temps(weather_downloader.today_max_day_temp)
weather_stat.compare_night_temps(weather_downloader.today_min_night_temp)
from weather_data_download import WeatherDataDownload
from weather_data_statistics import WeatherDataStatistics

def test_find_lat_long():
    """
    Tests the 'find_lat_long' method from 'WeatherDataDownload'.

    This tests that 'find_lat_long' can find and retrieve latitude and 
    longitude coordinates using the given city's name. It accounts for if the 
    city name has a typo or cannot be found in the Open-Meteo API's city name 
    database.

    Raises
    ------
    AssertionError
        Passes silently unless any of the assertions fail.
    """
    #Create test instance and test that coordinates of the city were 
    #correctly retrieved
    weather_down_irvine = WeatherDataDownload('Irvine')
    assert weather_down_irvine.find_lat_long() == ['33.66946', '-117.82311']

    #Create test instance and test for case insensitivity
    weather_down_irvine2 = WeatherDataDownload('irvine')
    assert weather_down_irvine.find_lat_long() == ['33.66946', '-117.82311']

    #Create failing test instance that should not have coordinates, tests 
    #that coordinates of the city could not be retrieved
    weather_down_irvineFAIL = WeatherDataDownload('Irvinewieuhf')
    assert weather_down_irvineFAIL.find_lat_long() == [0, 0]

def test_get_historical_data():
    """
    Tests the 'get_historical_data' method from 'WeatherDataDownload'.

    This tests that 'get_historical_data' gets a list with at least the 
    correct list length.
    
    Raises
    ------
    AssertionError
        Passes silently unless any of the assertions fail.
    """
    #Create test instance and apply get_historical_data(), takes default data 
    #from 2023
    weather_down_hb = WeatherDataDownload('Huntington Beach')
    weather_down_hb.get_historical_data()

    #Test max and min historical data list lengths
    assert len(weather_down_hb.daily_temperature_2m_max) == 365
    assert len(weather_down_hb.daily_temperature_2m_min) == 365

    #Test 2020 for leap year
    weather_down_hb.get_historical_data(2020)
    assert len(weather_down_hb.daily_temperature_2m_max) == 366
    assert len(weather_down_hb.daily_temperature_2m_min) == 366

def test_get_forecast_data():
    """
    Tests the 'get_forecast_data' method from 'WeatherDataDownload'.

    This tests that 'get_forecast_data' correctly collected a number, which 
    presumably represent's today's maximum and minimum temperatures.

    Raises
    ------
    AssertionError
        Passes silently unless any of the assertions fail.
    """
    #Create test instance and apply metod
    weather_down_hb = WeatherDataDownload('Huntington Beach')
    weather_down_hb.get_forecast_data()

    #Test retrieved temperatures are numbers
    assert type(round(weather_down_hb.today_max_day_temp)) == int
    assert type(round(weather_down_hb.today_min_night_temp)) == int

def test_extract_hist_weather_data_and_stats():
    """
    Tests the 'extract_data_for_month' method from 'WeatherDataStatistics'.

    This tests if 'extract_data_for_month' correctly extracts the extreme 
    temperatures needed.

    Raises
    ------
    AssertionError
        Passes silently unless any of the assertions fail.
    """
    #Create test instances, use december as test month
    weather_down_hb = WeatherDataDownload('Huntington Beach')
    weather_down_hb.get_historical_data()
    weather_stat_hb = WeatherDataStatistics('Huntington Beach')
    max_temps_dec2023 = weather_stat_hb.extract_data_for_month(
        weather_down_hb.daily_temperature_2m_max, 12)
    min_temps_dec2023 = weather_stat_hb.extract_data_for_month(
        weather_down_hb.daily_temperature_2m_min, 12)

    #Test that extract_data_for_month creates the correct amount of values 
    #and that those values are correct
    assert (len(max_temps_dec2023)) == 31
    assert (len(min_temps_dec2023)) == 31
    assert round(weather_stat_hb.max_temp(
                    max_temps_dec2023)) == round(74.9957)
    assert round(weather_stat_hb.min_temp(
                    min_temps_dec2023)) == round(46.9157)

    #Assign min and max historical data arrays to shorter, more legible names
    temp_2023_maxs = weather_down_hb.daily_temperature_2m_max
    temp_2023_mins = weather_down_hb.daily_temperature_2m_min

    #Tests for matching positions with the 2023 list of max temps
    assert len(temp_2023_maxs) == 365
    assert round(temp_2023_maxs[0]) == round(59.0657) #jan 1
    assert round(temp_2023_maxs[31]) == round(63.1157) #feb 1
    assert round(temp_2023_maxs[334]) == round(65.9057) #dec 1
    assert round(temp_2023_maxs[364]) == round(59.6057) #dec 31

    #Tests for matching positions with the 2023 list of min temps
    assert len(temp_2023_mins) == 365
    assert round(temp_2023_mins[0]) == round(51.1457) #jan 1
    assert round(temp_2023_mins[31]) == round(42.3257) #feb 1
    assert round(temp_2023_mins[334]) == round(47.8157) #dec 1
    assert round(temp_2023_mins[364]) == round(51.235703) #dec 31

def test_compare_temps_using_2023_hist_data():
    """
    Tests the 'compare_day_temps' and 'compare_night_temps' methods from 
    WeatherDataStatistics using the default 2023 historical data.

    Raises
    ------
    AssertionError
        Passes silently unless any of the assertions fail.
    """
    #Create test instances and match to 2023 data
    weather_stat_hb = WeatherDataStatistics('Huntington Beach')
    weather_stat_hb.match_against_historical_weather(12)

    #Test that each statement is correct for today's possible weather
    assert (weather_stat_hb.compare_day_temps(59) == 
        'Extremely cold in the day for this month')
    assert (weather_stat_hb.compare_day_temps(62) ==
        'Considerably cold in the day for this month')
    assert (weather_stat_hb.compare_day_temps(66) == 
        'Moderately cold in the day for this month')
    assert (weather_stat_hb.compare_day_temps(67.5) == 
        'Average temperature in the day for this month')
    assert (weather_stat_hb.compare_day_temps(69) == 
        'Moderately warm in the day for this month')
    assert (weather_stat_hb.compare_day_temps(72) == 
        'Considerably warm in the day for this month')
    assert (weather_stat_hb.compare_day_temps(76) == 
        'Record heat in the day for this month')
    
    assert (weather_stat_hb.compare_night_temps(46) == 
        'Record cold at night for this month')
    assert (weather_stat_hb.compare_night_temps(48) == 
        'Considerably cold at night for this month')
    assert (weather_stat_hb.compare_night_temps(51) == 
        'Moderately cold at night for this month')
    assert (weather_stat_hb.compare_night_temps(53) == 
        'Average temperature at night for this month')
    assert (weather_stat_hb.compare_night_temps(54) == 
        'Moderately warm at night for this month')
    assert (weather_stat_hb.compare_night_temps(57) == 
        'Considerably warm at night for this month')
    assert (weather_stat_hb.compare_night_temps(59) == 
        'Extremely hot at night for this month')

def test_compare_temps_using_2022_hist_data():
    """
    Tests the 'compare_day_temps' and 'compare_night_temps' methods from 
    WeatherDataStatistics using historical data from 2022.
    
    Raises
    ------
    AssertionError
        Passes silently unless any of the assertions fail.
    """
    #Create test instances and match to 2022 data
    weather_stat_hb = WeatherDataStatistics('Huntington Beach')
    weather_stat_hb.match_against_historical_weather(12, 2022)

    #Test that each statement is correct for today's possible weather
    assert (weather_stat_hb.compare_day_temps(52) == 
        'Extremely cold in the day for this month')
    assert (weather_stat_hb.compare_day_temps(56) == 
        'Considerably cold in the day for this month')
    assert (weather_stat_hb.compare_day_temps(60) == 
        'Moderately cold in the day for this month')
    assert (weather_stat_hb.compare_day_temps(62.75) == 
        'Average temperature in the day for this month')
    assert (weather_stat_hb.compare_day_temps(65) == 
        'Moderately warm in the day for this month')
    assert (weather_stat_hb.compare_day_temps(69) == 
        'Considerably warm in the day for this month')
    assert (weather_stat_hb.compare_day_temps(73) == 
        'Record heat in the day for this month')

    assert (weather_stat_hb.compare_night_temps(41) == 
        'Record cold at night for this month')
    assert (weather_stat_hb.compare_night_temps(43) == 
        'Considerably cold at night for this month')
    assert (weather_stat_hb.compare_night_temps(47) == 
        'Moderately cold at night for this month')
    assert (weather_stat_hb.compare_night_temps(49.4) == 
        'Average temperature at night for this month')
    assert (weather_stat_hb.compare_night_temps(51) == 
        'Moderately warm at night for this month')
    assert (weather_stat_hb.compare_night_temps(54) == 
        'Considerably warm at night for this month')
    assert (weather_stat_hb.compare_night_temps(57) == 
        'Extremely hot at night for this month')

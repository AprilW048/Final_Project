import pandas as pd
import numpy as np




def read_indata(path):
    '''

    :param path: a string of path saved the dataset
    :return: pandas datarame
    '''
    data = pd.read_csv(path)
    return data




## generate new column year for every data

def generate_year_month(df, colname, string):
    '''

    :param df: dataframe we want to add column year and month
    :param colname: a stirng column name in the dataframe saved the dateandtime
    :return: dataframe after adding the column
    '''
    df['year'] = pd.DatetimeIndex(df[colname]).year
    df['month'] = pd.DatetimeIndex(df[colname]).month
    df['indextype'] = str(string)
    return df

### append all weather index by country
def append_weather_index(dflist):
    weather_all = dflist[0]
    for i in range(len(dflist) - 1):
        weather_all = weather_all.append(dflist[i+1])

    return weather_all


def get_city(cityname, citycrime, weather_all):
    city_weather = weather_all[['year', 'month', cityname]]
    citycrime_per_month = citycrime.groupby(['year', 'month']).count()
    citycrime_per_month = pd.DataFrame(citycrime_per_month.reset_index())
    citycrime_per_month.columns = ['year', 'month', 'count']
    citycrime_per_month[['year', 'month']] = citycrime_per_month[['year', 'month']].astype(int)
    city_weather[['year', 'month']] = city_weather[['year', 'month']].astype(int)
    crime_weather = pd.merge(city_weather[['year', 'month', cityname, 'indextype']], citycrime_per_month,
                             on=['year', 'month'], how='left')

    return crime_weather


#### Soluruib

if __name__ == "__main__":

    city_attributes = read_indata('./historical-hourly-weather-data/city_attributes.csv')
    Humiditiy = read_indata('./historical-hourly-weather-data/humidity.csv')
    Pressure = read_indata('./historical-hourly-weather-data/pressure.csv')
    Temperature = read_indata('./historical-hourly-weather-data/temperature.csv')
    weather_description = read_indata('./historical-hourly-weather-data/weather_description.csv')
    wind_direction = read_indata('./historical-hourly-weather-data/wind_direction.csv')
    wind_speed = read_indata('./historical-hourly-weather-data/wind_speed.csv')
    chicago_crime = read_indata('./Chicago_crime_2012-2017.csv')
    airpollution = read_indata('./pollution_us_2000_2016.csv')

    ### ADD YEAR AND MONTH COLUMN TO DATA
    df_list = [Humiditiy, Pressure, Temperature, weather_description, wind_direction,
               wind_speed]
    stringlist = ['Humiditiy', 'Pressure', 'Temperature', 'weather_description', 'wind_direction',
                  'wind_speed']

    for index in range(len(df_list)):
        df = generate_year_month(df_list[index], 'datetime', stringlist[index])

    weather_all = append_weather_index(df_list)

    weather_all.head()

    airpollution = generate_year_month(airpollution, 'Date Local')

    chicago_crime['year'] = chicago_crime.Date.str[6:10]
    chicago_crime['month'] = chicago_crime.Date.str[0:2]

    ## count chicago crime
    chi_crime_per_month = chicago_crime.groupby(['year', 'month']).size()
    chi_crime_per_month = pd.DataFrame(chi_crime_per_month.reset_index())

    chi_crime_per_month.columns = ['year', 'month', 'count']
    print(chi_crime_per_month.head())

    # print head
    city_attributes.head()
    Humiditiy.head()

    Pressure.head()
    Temperature.head()
    weather_description.head()
    wind_direction.head()
    wind_speed.head()
    airpollution.head()

    list(Humiditiy.columns.values)
    list(Pressure.columns.values)
    list(chicago_crime.columns.values)

    weather_all[['year', 'month', 'Chicago', 'indextype']].head()
    chi_crime_per_month.head(15)
    chi_crime_per_month[['year', 'month']] = chi_crime_per_month[['year', 'month']].astype(int)
    weather_all[['year', 'month']] = weather_all[['year', 'month']].astype(int)

crime_weather = pd.merge(weather_all[['year', 'month', 'Chicago', 'indextype']], chi_crime_per_month,
                         on=['year', 'month'], how='left')

crime_weather.head()
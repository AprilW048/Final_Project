import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from datetime import datetime

def read_indata(path):
    '''
    This function is used when given the path read in data

    :param path: a string of path saved the dataset
    :return: pandas datarame
    '''
    data = pd.read_csv(path)
    return data

#generate new column year for every data
def generate_year_month_day(df, colname):
    '''
    This function generate three new columns, which are year, month and day based on the variable
    datetime

    :param df: dataframe we want to add column year and month
    :param colname: a stirng column name in the dataframe saved the dateandtime
    :return: dataframe after adding the column
    >>> raw_data = {'name': ['Willard Morris', 'Al Jennings', 'Omar Mullins', 'Spencer McDaniel'],'birth_date': ['01-02-1996', '08-05-1997', '04-28-1996', '12-16-1995']}
    >>> df = pd.DataFrame(raw_data, index = ['Willard Morris', 'Al Jennings', 'Omar Mullins', 'Spencer McDaniel'])
    >>> df_after=generate_year_month_day(df,'birth_date')
    >>> df['day'].sum()
    51
    '''
    df['year'] = pd.DatetimeIndex(df[colname]).year
    df['month'] = pd.DatetimeIndex(df[colname]).month
    df['day'] = pd.DatetimeIndex(df[colname]).day
    return df


def get_city_weather(cityname, df_list, stringlist):
    """
    Extract the specific city's weather, including temperature, humidity, wind speed, from the
    weather dataset, specify the corresponding dataset in df_list

    :param cityname: a string of cityname, like "Chicago"
    :param df_list: a list of dataframe
    :param stringlist: a list of the name of these dataframe
    :return: a new list of dataframe, with some information updated

    """
    new_df_list = []
    for i in range(len(stringlist)):
        citydf = df_list[i][(df_list[i].year >= 2012) & (df_list[i].year < 2018)].copy(deep=True)
        citydf = citydf[['year', 'month', 'day', cityname]]
        citydf[['year', 'month', 'day']] = citydf[['year', 'month', 'day']].astype(int)
        citydf = pd.DataFrame(citydf.groupby(['year', 'month', 'day']).mean())
        citydf = citydf.reset_index()
        citydf = citydf.rename(columns={cityname: stringlist[i]})

        new_df_list.append(citydf)
    return new_df_list



def merge_dataframe(df1, df2, mergeby):
    """
    Given two dataframe and merged by which column/columns, we are able to get
    the left join dataframe

    :param df1: a dataframe
    :param df2: a dataframe
    :param mergeby: column names referred to merge om
    :return: merged data
    """

    merged_data = pd.merge(df1, df2, on=mergeby, how='left')

    return merged_data


def mergeall_weather(new_df_list, mergeby):
    """
    This function is used to merge all the updated weather dataframe

    :param new_df_list: updated list of weather dataframe from former step
    :param mergeby: column named referred to merge om
    :return: new dataframe merged all weather
    """

    weather_all = new_df_list[0]
    for i in range(len(new_df_list) - 1):
        weather_all = merge_dataframe(weather_all, new_df_list[i + 1], mergeby)
    return weather_all


def get_city(cityname, citycrime, weather_all):
    '''
    This function is used to get the merged crime data and weather data of the pointed city

    :param cityname: a string of the name of the city
    :param citycrime: the crime data of this city
    :param weather_all: new dataframe merged all weather
    :return: new dataframe
    '''

    city_weather = weather_all[['year', 'month', 'day', cityname, 'indextype']].copy(deep=True)
    citycrime_per_month = citycrime.groupby(['year', 'month', 'day']).size()
    citycrime_per_month = pd.DataFrame(citycrime_per_month.reset_index())
    citycrime_per_month = citycrime_per_month.rename(columns={0: 'Count'})
    citycrime_per_month[['year', 'month', 'day']] = citycrime_per_month[['year', 'month', 'day']].astype(int)

    city_weather[['year', 'month', 'day']] = city_weather[['year', 'month', 'day']].astype(int)

    crime_weather = pd.merge(city_weather[['year', 'month', 'day', cityname, 'indextype']], citycrime_per_month,
                             on=['year', 'month'], how='left')

    crime_weather = crime_weather[(crime_weather.year >= 2012) & (crime_weather.year < 2018)]
    crime_weather = crime_weather.rename(columns={cityname: 'indexvalue'})
    return crime_weather

def convert_to_Celsius(df,col):
    """

    :param df: the dataframe that need to do the conversion
    :param col: the colunm that need to do the conversion
    :return: the dataframe after the conversion
    """
    df[col]=df[col]-273.5
    return df



#Humidity comfortable range from 30-60
def vectorize_humidity(df):
    """
    To vectorize the humidity

    :param df: dataframe containing Humidity
    :return: a value after vectorize the humidity
    """
    if df['Humiditiy'] <= 0.45:
        val = 'Low'
    elif df['Humiditiy'] <= 0.65:
        val = 'Normal'
    elif df['Humiditiy'] > 0.65:
        val = 'High'
    return val


def vectorize_temperature(df):
    """
    To vectorize the Temperature

    :param df: dataframe containing temperature
    :return: a value after vectorize
    """

    if df['Temperature'] <= 5:
        val = '0-5'
    elif df['Temperature'] <= 10:
        val = '5-10'
    elif df['Temperature'] <= 15:
        val = '10-15'
    elif df['Temperature'] <= 20:
        val = '15-20'
    elif df['Temperature'] <= 25:
        val = '20-25'
    elif df['Temperature'] <= 30:
        val = '25-30'
    elif df['Temperature'] > 30:
        val = '>30'
    return val


def normalize_humidity(df, colname):
    """
    This function is used to normalized the pointed column

    :param df: dataframe
    :param colname: column name
    :return: dataframe
    """
    minmaxnorm = (df[colname] - df[colname].min()) / (df[colname].max() - df[colname].min())
    df[colname] = minmaxnorm

    return df


#for air pollution part
def city_groupby(df, colname, city_name):
    '''
    This function mainly is used to process the AQI data.
    :param df: dataframe we want to divide base on city name
    :param colname: the column name in the dataframe saved the city name
    :param city_name: the specific city name
    :return: dataframe after filter city and year from 2012 to 2018, group by year and month
    '''
    df = df[(df[colname].str.contains(city_name)) & (df.year>=2012) & (df.year<2018)]
    df = df.groupby(['year','month']).agg({'mean'})

    return df

def crime_count(df, date_colname,per):
    '''
    :param df: dataframe we want to count the number of crime
    :param colname: a string column name in the dataframe saved the date
    :return: dataframe after adding the column
    '''
    df['year'] = df[date_colname].str[6:10].astype(int)
    df['month'] = df[date_colname].str[0:2].astype(int)
    df['day'] =  df[date_colname].str[3:5].astype(int)
    df = df[(df.year>=2012) & (df.year<2018)]
    if per == 'month':
        df_per = df[[date_colname,'year', 'month']].groupby(['year', 'month']).count().rename(columns={date_colname:'count'})
    elif per == 'day':
        df_per = df[[date_colname,'year', 'month','day']].groupby(['year', 'month','day']).count().rename(columns={date_colname:'count'})
    #df['indextype'] = str(string)
    return df_per


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

    #Humiditiy = read_indata('./historical-hourly-weather-data/humidity.csv')
    #Pressure = read_indata('./historical-hourly-weather-data/pressure.csv')
    #Temperature = read_indata('./historical-hourly-weather-data/temperature.csv')
    #chicago_crime = read_indata('./Chicago_crime_2012-2017.csv')



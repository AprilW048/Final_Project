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
    >>> pd=read_indata('./sample_data/pollution_sample.csv')
    >>> pd['AQI'][0]
    53
    '''
    data = pd.read_csv(path)
    return data

#generate new column year for every data
def generate_year_month_day(df, colname,per):
    '''
    This function generate three new columns, which are year, month and day based on the variable
    datetime

    :param df: dataframe we want to add column year and month
    :param colname: a stirng column name in the dataframe saved the dateandtime
    :return: dataframe after adding the column
    >>> air_data=pd.read_csv('./sample_data/pollution_sample.csv')
    >>> results=generate_year_month_day(air_data,'Date','day')
    >>> results['day'][0]
    24
    >>> results2=generate_year_month_day(air_data,'Date','month')
    >>> results2['month'][0]
    12
    '''
    if per =='day':
        df['year'] = pd.DatetimeIndex(df[colname]).year
        df['month'] = pd.DatetimeIndex(df[colname]).month
        df['day'] = pd.DatetimeIndex(df[colname]).day
    elif per=='month':
        df['year'] = pd.DatetimeIndex(df[colname]).year
        df['month'] = pd.DatetimeIndex(df[colname]).month
    return df


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


#Humidity comfortable range from 30-60
def vectorize_humidity(df):
    """
    To vectorize the humidity

    :param df: dataframe containing Humidity
    :return: a value after vectorize the humidity
    >>> raw_data = {'Humiditiy': [0.4,0.6,0.7]}
    >>> df = pd.DataFrame(raw_data)
    >>> df['Humidity'] = df.apply(vectorize_humidity, axis=1)
    >>> df['Humidity'][0]
    'Low'
    >>> df['Humidity'][1]
    'Normal'
    >>> df['Humidity'][2]
    'High'
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
    >>> raw_data = {'Temperature': [4, 8, 11,16,22,27,31]}
    >>> df = pd.DataFrame(raw_data)
    >>> df['Temperature'] = df.apply(vectorize_temperature, axis=1)
    >>> df['Temperature'][0]
    '0-5'
    >>> df['Temperature'][1]
    '5-10'
    >>> df['Temperature'][2]
    '10-15'
    >>> df['Temperature'][3]
    '15-20'
    >>> df['Temperature'][4]
    '20-25'
    >>> df['Temperature'][5]
    '25-30'
    >>> df['Temperature'][6]
    '>30'

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


def city_temp_Celsius(df,city):
    """
    Extract the corresponding city's temperature and convert it to Celsius degree from the
    original Temperature data.
    :param df: the original Temperature data
    :param col: the colunm that need to do the conversion
    :return: the dataframe after the conversion
    >>> temp_date = pd.read_csv('./sample_data/temp_sample.csv')
    >>> temp_date['year'] = pd.DatetimeIndex(temp_date['datetime']).year
    >>> temp_date['month'] = pd.DatetimeIndex(temp_date['datetime']).month
    >>> temp_date['day'] = pd.DatetimeIndex(temp_date['datetime']).day
    >>> results=city_temp_Celsius(temp_date,'Los Angeles')
    >>> results['Los Angeles'][1]<273.5
    True
    """
    city_temp = df[[city, 'year', 'month', 'day']]
    city_temp[city]=city_temp[city]-273.5
    return city_temp

def average_temp(df,city, per):
    """
    This function is mainly useful in calculating the daily and monthly
    average temperature of the specifying cities

    :param df: dataframe that contain a city's temperature data
    :param per: specify whether want to calculate the daily average temperature or monthly average temperature
    :return: a dataframe that contains the results after calculation
    >>> temp_date = pd.read_csv('./sample_data/temp_sample.csv')
    >>> temp_date['year'] = pd.DatetimeIndex(temp_date['datetime']).year
    >>> temp_date['month'] = pd.DatetimeIndex(temp_date['datetime']).month
    >>> temp_date['day'] = pd.DatetimeIndex(temp_date['datetime']).day
    >>> results=average_temp(temp_date,'Chicago','day')
    >>> results2=average_temp(temp_date,'Chicago','month')
    >>> len(results['mean_temp'])
    2
    >>> len(results2['mean_temp'])
    1
    """
    if per=='day':
        df_after=df[[city,'year','month','day']].\
            groupby(['year','month','day'], as_index=False ).agg({'mean'}).\
            reset_index().rename(columns={city:'mean_temp'})
    elif per=='month':
        df_after = df[[city, 'year', 'month']]. \
            groupby(['year', 'month'], as_index=False).agg({'mean'}). \
            reset_index().rename(columns={city: 'mean_temp'})
    df_after.columns=df_after.columns.droplevel(1)
    return df_after


#for air pollution part
def city_groupby(df, colname, city_name):
    '''
    This function mainly is used to process the AQI data.
    :param df: dataframe we want to divide base on city name
    :param colname: the column name in the dataframe saved the city name
    :param city_name: the specific city name
    :return: dataframe after filter city and year from 2012 to 2018, group by year and month
    >>> air_data=pd.read_csv('./sample_data/pollution_sample.csv')
    >>> air_data=air_data[['CBSA', 'Date', 'AQI']]
    >>> air_data['year'] = pd.DatetimeIndex(air_data['Date']).year
    >>> air_data['month'] = pd.DatetimeIndex(air_data['Date']).month
    >>> air_data['day'] = pd.DatetimeIndex(air_data['Date']).day
    >>> results=city_groupby(air_data,'CBSA','Chicago')
    >>> results['AQI']['mean'][0]
    57.125
    '''
    df = df[(df[colname].str.contains(city_name)) & (df.year>=2012) & (df.year<2018)]
    df = df.groupby(['year','month']).agg({'mean'})

    return df

def crime_count(df, date_colname,per):
    ''' This funtion is used to count the number of crime based on month or day
    :param df: dataframe we want to count the number of crime
    :param colname: a string column name in the dataframe saved the date
    :return: dataframe after adding the column
    >>> crime_data = pd.read_csv('./sample_data/LA_crime_sample.csv')
    >>> daily_crime=crime_count(crime_data,'Date Occurred','day')
    >>> daily_crime['count'][1]
    1

    >>> monthly_crime=crime_count(crime_data,'Date Occurred','month')
    >>> monthly_crime['count'][0]
    10
    >>> new_crime=normalize_crime_type(crime_data,'Crime Code Description')
    >>> type_crime=crime_count(new_crime,'Date Occurred','type')
    >>> type_crime['count'][0]
    3

    '''
    df['year'] = df[date_colname].str[6:10].astype(int)
    df['month'] = df[date_colname].str[0:2].astype(int)
    df['day'] =  df[date_colname].str[3:5].astype(int)
    df = df[(df.year>=2012) & (df.year<2018)]
    if per == 'month':
        df_per = df[[date_colname,'year', 'month']].groupby(['year', 'month']).count().rename(columns={date_colname:'count'})
    elif per == 'day':
        df_per = df[[date_colname,'year', 'month','day']].groupby(['year', 'month','day']).count().rename(columns={date_colname:'count'})
    elif per == 'type':
        df_per = df[[date_colname, 'year', 'month', 'type']].groupby(['year', 'month', 'type']).count().rename(columns={date_colname: 'count'})
    return df_per

def crime_type_word_count(crime_df, type_colname):
    """This function is used to count the frequency of word in the type column.
    It could help classify the current crime type into a more general category

    :param crime_df:  dataframe we want to count the number of words crime type
    :param type_colname: a string column name in the dataframe saved the crime type
    :return: return the frequency of each word
    >>> crime_data = pd.read_csv('./sample_data/LA_crime_sample.csv')
    >>> word_frequency=crime_type_word_count(crime_data,'Crime Code Description')
    >>> word_frequency[word_frequency.index=='ROBBERY'][0]
    2

    """
    crime_word = crime_df[type_colname].str.split('\s|,', expand=True)
    word_count = crime_word.stack().value_counts()
    return word_count

def normalize_crime_type(crime_df, type_colname):
    """This function is used to normailize the crime type in different city.

    :param crime_df: data frame that contain crime data
    :param type_colname: the name the column that indicate crime type
    :return: return the crime data frame with a new column 'type'
    >>> crime_data = pd.read_csv('./sample_data/LA_crime_sample.csv')
    >>> crime_data['Crime Code Description'][3]
    'BATTERY - SIMPLE ASSAULT'
    >>> new_crime=normalize_crime_type(crime_data,'Crime Code Description')
    >>> new_crime['type'][3]
    'ASSAULT'

    """
    crime_type = crime_df[[type_colname]].replace(
        regex=[r'^.*ASSAULT.*$', r'^.*BATTERY.*$', r'^.*INTIMATE.*$', r'^.*RAPE.*$', r'^.*KIDNAPPING.*$',
               r'^.*ASSLT.*$', ], value='ASSAULT')
    crime_type = crime_type[[type_colname]].replace(
        regex=[r'^.*OFF.*$', r'^.*MISCHIEF.*$', r'^.*HARRASSMENT.*$', r'^.*EXTORTION.*$',
               r'^.*JOSTLING.*$', r'^.*OBSCENITY.*$', r'^.*STALK.*$', r'^.*INDECENT.*$', r'^.*PEEP.*$',
               r'^.*INTIMIDATION.*$', r'^.*THREAT.*$'], value='OFFENSES')
    crime_type = crime_type[[type_colname]].replace(
        regex=[r'^.*DAMAGE.*$', r'^.*VANDALISM.*$', r'^.*IMPAIRED.*$', r'^.*ARSON.*$', r'^.*WRECK.*$'],
        value='VANDALISM')

    crime_type = crime_type[[type_colname]].replace(regex=[r'^.*BURGLAR.*$'], value='BURGLARY')
    crime_type = crime_type[[type_colname]].replace(regex=[r'^.*ROBBERY.*$'], value='ROBBERY')
    crime_type = crime_type[[type_colname]].replace(
        regex=[r'^.*THEFT.*$', r'^.*LARCENY.*$', r'^.*STOLEN.*$', r'^.*SNATCHING.*$', r'^.*PROWLER.*$',
               r'^.*PICKPOCKET.*$', ], value='THEFT')
    crime_type = crime_type[[type_colname]].replace(regex=[r'^.*DRUG.*$', r'^.*NARCOTIC.*$'], value='DRUG')
    crime_type = crime_type[[type_colname]].replace(
        regex=[r'^.*VIOLATION.*$', r'^.*GAMBL.*$', r'^.*LEWD.*$', r'^.*ALCOHOL.*$',
               r'^.*ESCAPE.*$', r'^.*RESIST.*$', r'^.*CONTEMPT.*$', r'^.*YIELD.*$',
               r'^.*DISTURB.*$', r'^.*DISRUPT.*$', r'^.*PUB.*$', r'^.*DISORDER.*$', r'^.*SCARE.*$',
               r'^.*WEAPON.*$', r'^.*SHOT.*$', r'^.*FIREARM.*$',
               r'^.*LOITERING.*$', r'^.*UNAUTHORIZED.*$', r'^.*THROW.*$', r'^.*DUMP.*$',
               r'^.*TRESPASS.*$', r'^.*DRIVING.*$', r'^.*TRAFFIC.*$'], value='VIOLATION')
    crime_type = crime_type[[type_colname]].replace(
        regex=[r'^.*DECEPTIVE.*$', r'^.*FRAUD.*$', r'^.*FORGERY.*$', r'^.*CONCEALED.*$', r'^.*COUNTERFEIT.*$'],
        value='DECEPTIVE')

    crime_type = crime_type[[type_colname]].replace(regex=[r'^.*HOMICIDE.*$', r'^.*MURDER.*$', r'^.*MANSLAUGHTER.*$'],
                                                    value='HOMICIDE')

    crime_type = crime_type[[type_colname]].replace(
        regex=[r'^.*OTHER.*$', r'^.*ATTEMPT.*$', r'^.*NON.*$', r'^.*FALSE.*$',
               r'^.*CHILD.*$', r'^.*CHL.*$', r'^.*ANIMAL.*$', r'^.*DOCUMENT.*$',
               r'^.*SEX.*$', r'^.*PIMP.*$', r'^.*PROSTITUTION.*$', r'^.*PANDER.*$', r'^.*COPULATION.*$',
               r'^.*CODE.*$', r'^.*LAW.*$', r'^.*MISCELLANEOUS.*$'], value='OTHERS')

    crime_df['type'] = crime_type
    return crime_df






if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

    #Humiditiy = read_indata('./historical-hourly-weather-data/humidity.csv')
    #Pressure = read_indata('./historical-hourly-weather-data/pressure.csv')
    #Temperature = read_indata('./historical-hourly-weather-data/temperature.csv')
    #chicago_crime = read_indata('./Chicago_crime_2012-2017.csv')



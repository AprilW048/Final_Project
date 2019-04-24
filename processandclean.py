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

def generate_year_month_day(df, colname, string):
    '''
    :param df: dataframe we want to add column year and month
    :param colname: a stirng column name in the dataframe saved the dateandtime
    :return: dataframe after adding the column
    '''
    df['year'] = pd.DatetimeIndex(df[colname]).year
    df['month'] = pd.DatetimeIndex(df[colname]).month
    df['day'] = pd.DatetimeIndex(df[colname]).day
    return df


def get_city_weather(cityname, df_list, stringlist):
    new_df_list = []
    for i in range(len(stringlist)):
        citydf = df_list[i][(df_list[i].year>=2012) & (df_list[i].year<2018)].copy(deep=True)
        citydf = citydf[['year', 'month', 'day', cityname]]
        citydf[['year', 'month', 'day']] = citydf[['year', 'month', 'day']].astype(int)
        citydf = pd.DataFrame(citydf.groupby(['year', 'month', 'day']).mean())
        citydf = citydf.reset_index()
        citydf = citydf.rename(columns={cityname: stringlist[i]})

        new_df_list.append(citydf)
    return new_df_list



def merge_dataframe(df1, df2, mergeby):

    merged_data = pd.merge(df1, df2, on=mergeby, how='left')

    return merged_data


## merge all weather index by city
def mergeall_weather(new_df_list, mergeby):
    weather_all = new_df_list[0]
    for i in range(len(new_df_list) - 1):
        weather_all = merge_dataframe(weather_all, new_df_list[i+1], mergeby)
    return weather_all


def get_city(cityname, citycrime, weather_all):
    city_weather = weather_all[['year', 'month','day', cityname,'indextype']].copy(deep = True)
    citycrime_per_month = citycrime.groupby(['year', 'month', 'day']).size()
    citycrime_per_month = pd.DataFrame(citycrime_per_month.reset_index())
    citycrime_per_month = citycrime_per_month.rename(columns = {0:'Count'})
    citycrime_per_month[['year', 'month', 'day']] = citycrime_per_month[['year', 'month', 'day']].astype(int)

    city_weather[['year', 'month', 'day']] = city_weather[['year', 'month', 'day']].astype(int)

    crime_weather = pd.merge(city_weather[['year', 'month', 'day',cityname, 'indextype']], citycrime_per_month,
                             on=['year', 'month'], how='left')

    crime_weather = crime_weather[(crime_weather.year >= 2012) & (crime_weather.year < 2018)]
    crime_weather = crime_weather.rename(columns={cityname: 'indexvalue'})

    return crime_weather



#### Humidity comfortable range from 30-60
def vectorize_humidity(df):
    if df['Humiditiy'] <= 45:
        val = 'Low'
    elif df['Humiditiy'] <= 60:
        val = 'Normal'
    elif df['Humiditiy'] > 60:
        val = 'High'
    return val








#### Solution

if __name__ == "__main__":

    Humiditiy = read_indata('./historical-hourly-weather-data/humidity.csv')
    Pressure = read_indata('./historical-hourly-weather-data/pressure.csv')
    Temperature = read_indata('./historical-hourly-weather-data/temperature.csv')
    weather_description = read_indata('./historical-hourly-weather-data/weather_description.csv')
    wind_direction = read_indata('./historical-hourly-weather-data/wind_direction.csv')
    wind_speed = read_indata('./historical-hourly-weather-data/wind_speed.csv')
    chicago_crime = read_indata('./Chicago_crime_2012-2017.csv')

    ### ADD YEAR AND MONTH COLUMN TO DATA
    df_list = [Humiditiy, Pressure, Temperature, wind_direction,wind_speed]
    stringlist = ['Humiditiy', 'Pressure', 'Temperature', 'wind_direction', 'wind_speed']

    for index in range(len(df_list)):
        df = generate_year_month_day(df_list[index], 'datetime', stringlist[index])

    ### Chicago
    new_df_list = get_city_weather('Chicago', df_list, stringlist)
    weather_all = mergeall_weather(new_df_list, ['year', 'month', 'day'])


    chicago_crime['year'] = chicago_crime.Date.str[6:10]
    chicago_crime['month'] = chicago_crime.Date.str[0:2]
    chicago_crime['day'] = chicago_crime.Date.str[3:5]

    ## count chicago crime

    chi_crime_per_day = chicago_crime.groupby(['year', 'month', 'day', 'Primary Type', 'Arrest',  'Domestic']).size()
    chi_crime_per_day= pd.DataFrame(chi_crime_per_day.reset_index())
    chi_crime_per_day = chi_crime_per_day.rename(columns = {0:'Count'})
    chi_crime_per_day[['year', 'month', 'day']] = chi_crime_per_day[['year', 'month', 'day']].astype(int)

    crime_weather= merge_dataframe(weather_all,chi_crime_per_day,['year', 'month', 'day'])
    crime_weather = crime_weather.dropna()
    crime_weather.iloc[:,4:8]
    set(crime_weather['Primary Type'])

    ### humidity versus crime type
    subset = crime_weather[['year', 'month', 'day','Humiditiy', 'Count','Primary Type']].copy(deep = True)
    subset['Reltaive Humidity'] = subset.apply(vectorize_humidity, axis = 1)

    ### ignore the time, overall weather and crime
    crime_count = pd.DataFrame(subset.groupby(['Primary Type','Reltaive Humidity']).agg({'Count':np.sum}))
    crime_count = crime_count.reset_index()

    crime_count = crime_count.loc[crime_count['Primary Type'].isin(['ASSAULT','BATTERY', 'CRIMINAL DAMAGE','HOMICIDE'])]
    fig, ax = plt.subplots()
    N = len(set(crime_count['Primary Type']))
    HighCounts = tuple(crime_count.loc[crime_count['Reltaive Humidity'] == 'High', 'Count'])
    NormalCounts = tuple(crime_count.loc[crime_count['Reltaive Humidity'] == 'Normal', 'Count'])
    LowCounts = tuple(crime_count.loc[crime_count['Reltaive Humidity'] == 'Low', 'Count'])
    ind = np.arange(N)
    width = 0.35

    p1 = ax.bar(ind, LowCounts, witdth,color='Yellow')
    p2 = ax.bar(ind, NormalCounts, witdth, color='Orange', bottom = LowCounts)
    p3 = ax.bar(ind, HighCounts, witdth, color = 'Red', bottom = NormalCounts)
    ax.set_ylabel('Count')
    ax.set_xlabel('Relative Humidity')
    ax.set_title('Count by Relative Humidity')
    ax.set_xticks(ind + width / 2.)
    #ax.set_yticks(np.arange(0, 81, 10))
    ax.set_xticklabels(('ASSAULT','BATTERY', 'CRIMINAL DAMAGE','HOMICIDE'))
    plt.show()
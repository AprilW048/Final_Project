#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


def read_indata(path):
    '''
    :param path: a string of path saved the dataset
    :return: pandas datarame
    '''
    data = pd.read_csv(path)
    return data


## generate new column year for every data

def generate_year_month(df, colname):
    '''
    :param df: dataframe we want to add column year and month
    :param colname: a stirng column name in the dataframe saved the dateandtime
    :return: dataframe after adding the column
    '''
    df['year'] = pd.DatetimeIndex(df[colname]).year
    df['month'] = pd.DatetimeIndex(df[colname]).month
    #df['indextype'] = str(string)
    return df


# In[5]:


# In[39]:


def city_groupby(df, colname, city_name):
    '''
    :param df: dataframe we want to divide base on city name
    :param colname: the column name in the dataframe saved the city name
    :param city_name: the specific city name 
    :return: dataframe after filter city and year from 2012 to 2018, group by year and month
    '''
    df = df[(df[colname]==city_name) & (df.year>=2012) & (df.year<2018)]
    df = df.groupby(['year','month']).agg({'mean'})

    return df


# In[86]:
if __name__ == '__main__':

    Chicago_airpollution = city_groupby(airpollution, 'City', 'Chicago')
    Chicago_airpollution.head()
    airpollution[(airpollution['City']=='Chicago')]
    #NYC_airpollution = city_groupby(airpollution, 'City', 'New York')
    #NYC_airpollution.head()

    #LA_airpollution = city_groupby(airpollution, 'City', 'Los Angeles')
    #LA_airpollution.head()


    # In[35]:


    chicago_crime = read_indata('./Chicago_crime_2012-2017.csv')
    chicago_crime.head()
    ## count chicago crime
    #chi_crime_per_month = chicago_crime[['ID', 'year', 'month']].groupby(['year', 'month']).size()


    # In[36]:


    generate_year_month(chicago_crime, 'Date').head()


    # In[66]:


    chicago_crime = chicago_crime[(chicago_crime.year>=2012) & (chicago_crime.year<2018)]
    chi_crime_per_month = chicago_crime[['ID', 'year', 'month']].groupby(['year', 'month']).count().rename(columns={'ID':'count'})
    chi_crime_per_month.head()


    # In[75]:


    pd.merge(Chicago_airpollution, chi_crime_per_month,on=['year','month'])


    # In[76]:


    Chicago_airpollution


    # In[ ]:

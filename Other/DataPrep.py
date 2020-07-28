#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 17:19:20 2020

@author: tanyaedwards
"""
import pandas as pd

def prepare_location_weather_data(location_data_path, weather_data_df):
  for filename in os.listdir(location_data_path):
    if filename.endswith(".csv"):
      filepath = os.path.join(location_data_path, filename)
      # print(filename[:-4])
      
      # Read the country specific weather data from csv
      # the data has intraday weather information, lets merge them and keep the last time instance of any day
      country_weather_df = pd.read_csv(filepath)
      country_weather_df['date_time'] = pd.to_datetime(country_weather_df['date_time'])
      country_weather_df['date_time'] = country_weather_df['date_time'].dt.strftime('%-m/%-d/%y')
      country_weather_df_unique = country_weather_df.reset_index().drop_duplicates(subset=['date_time'], keep='last').set_index('index')

      #create a temporary dataframe where we convert the data into required structure aligned with JHU CSSE
      data_df = pd.DataFrame()
      data_df['date_time'] = country_weather_df_unique['date_time']
      data_df['maxtempC'] = country_weather_df_unique['maxtempC']
      data_df['mintempC'] = country_weather_df_unique['mintempC']
      data_df['humidity'] = country_weather_df_unique['humidity']
      data_df = data_df.T
      data_df = data_df.rename(columns=data_df.iloc[0])
      data_df = data_df.drop(data_df.index[0])
      data_df.insert(0, 'weather_param', data_df.index)
      data_df.reset_index(drop=True, inplace=True)
      data_df.insert(0, 'Country/Region', filename[:-4])
      
      # appending to a master dataframe
      weather_data_df = weather_data_df.append(data_df)
      weather_data_df.reset_index(drop=True, inplace=True)
  
  return weather_data_df

weather_data_df = pd.DataFrame()
weather_data_df = prepare_location_weather_data('regions', weather_data_df)
print(weather_data_df)
print(weather_data_df.shape)

weather_data_df.to_csv('weather_data_countries.csv')
weather_data_df = pd.read_csv('regions/weather_data_countries.csv')
weather_data_df.head()






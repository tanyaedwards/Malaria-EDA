#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:46:27 2020

@author: tanyaedwards
"""

from wwo_hist import retrieve_hist_data
import os

os.chdir('regions')

frequency = 3
#start_date = '11-DEC-2018'
#end_date = '11-MAR-2019'
start_date = '1-JAN-2013'
end_date = '31-DEC-2013'
api_key = '5cd589dc43ae41e6958142328202807'

location_list = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 
                 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 
                 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 
                 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 
                 'Burkina Faso', 'Burma', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 
                 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Congo (Brazzaville)', 
                 'Congo (Kinshasa)', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 
                 'Czechia', 'Denmark', 'Diamond Princess', 'Djibouti', 'Dominica', 'Dominican Republic', 
                 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 
                 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 
                 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 
                 'Guyana', 'Haiti', 'Holy See', 'Honduras', 'Hungary', 'Iceland', 'India', 
                 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 
                 'Jordan', 'Kazakhstan', 'Kenya', 'Korea, South', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 
                 'Laos', 'Latvia', 'Lebanon', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 
                 'Luxembourg', 'MS Zaandam', 'Madagascar', 'Malaysia', 'Maldives', 'Mali', 'Malta', 
                 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 
                 'Morocco', 'Mozambique', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 
                 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 
                 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 
                 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 
                 'Saint Lucia', 'Saint Vincent and the Grenadines', 'San Marino', 'Saudi Arabia', 
                 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 
                 'Slovenia', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 
                 'Sweden', 'Switzerland', 'Syria', 'Taiwan*', 'Tanzania', 'Thailand', 'Timor-Leste', 
                 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'United States', 'Uganda', 
                 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'Uzbekistan', 
                 'Venezuela', 'Vietnam', 'West Bank and Gaza', 'Zambia', 'Zimbabwe']

#'Angola','Botswana','Lesotho','Malawi','Mozambique','Namibia',
#'South_Africa','Zambia','Zimbabwe','Comoros','Djibouti','Eritrea','Ethiopia','Kenya','Madagascar',
#'Mauritius','Rwanda','Seychelles','Somalia',

AU_list=[
         'South_Sudan','Sudan',
         'Tanzania','Uganda','Burundi','Cameroon','Central_African_Republic',
         'Chad','Congo','Congo','Equatorial_Guinea','Gabon',
         'Sao_Tome_and_Principe','Algeria','Egypt','Libya','Morocco','Tunisia',
         'Benin','Burkina_Faso','Cape Verde', "Cote d'Ivoire",'Gambia','Ghana','Guinea',
         'Guinea-Bissau','Liberia','Mali','Niger','Nigeria','Senegal','Sierra_Leone','Togo',
         'Mauritania']


hist_weather_data = retrieve_hist_data(api_key,
                                AU_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = False)


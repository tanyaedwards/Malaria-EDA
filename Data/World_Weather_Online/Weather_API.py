#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:46:27 2020

@author: tanyaedwards
"""

from wwo_hist import retrieve_hist_data
import os

year = 2009

os.chdir('countries/{}'.format(year))

frequency = 24
start_date = '1-JAN-{}'.format(year)
end_date = '31-DEC-{}'.format(year)
api_key = '5cd589dc43ae41e6958142328202807'

AU_list=['Angola','Botswana','Lesotho','Malawi','Mozambique','Namibia','South_Sudan','Sudan',
         'South_Africa','Zambia','Zimbabwe','Comoros','Djibouti','Eritrea','Ethiopia','Kenya',
         'Madagascar','Tanzania','Uganda','Burundi','Cameroon','Central_African_Republic',
         'Chad','Democratic_Republic_of_Congo','Congo','Equatorial_Guinea','Gabon','Mauritius','Rwanda','Seychelles',
         'Somalia','Sao_Tome_and_Principe','Algeria','Egypt','Libya','Morocco','Tunisia',
         'Benin','Burkina_Faso','Cape_Verde', "Cote_d'Ivoire",'Gambia','Ghana','Guinea',
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

    

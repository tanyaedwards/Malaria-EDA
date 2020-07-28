#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 13:40:51 2020

@author: tanyaedwards

Malaria
WHO DATA
"""

import pandas as pd
from matplotlib import pyplot as plt

#read in csv files
est_cases_master = pd.read_csv('cases/malaria_estimated_cases.csv', skiprows=1)
inc_cases =  pd.read_csv('cases/malaria_case_incidence_per_1000_pop_at_risk.csv', skiprows=1)
countries_WHO_region = pd.read_csv('countries.csv')
#reorder df
cols = est_cases_master.columns.tolist()
cols = cols[::-1]
cols = cols[-1:] + cols[:-1]
est_cases_master = est_cases_master[cols]
cols_inc = inc_cases.columns.tolist()
cols_inc = cols_inc[::-1]
cols_inc = cols_inc[-1:] + cols_inc[:-1]
inc_cases = inc_cases[cols_inc]

#check which countries are mislabelled and are not in study
#Naming discrepancies between WHO Malaria data and WHO country list definitions
#Comoros needed to be added to list of countries
countries_study=est_cases_master['Country'].tolist()
#countries_study=inc_cases['Country'].tolist()
countries_WHO = countries_WHO_region['Country'].tolist()
for country_study in countries_study:
    if country_study not in countries_WHO:
        print('Mislabelled: {}'.format(country_study))
        for country_WHO in countries_WHO:
            if (country_study[-3:] or country_study[:3]) in country_WHO:
                print('''Could be this name {}
                '''.format(country_WHO))

#No. of countries not inluded in study = 86
#No. of countries in study = 107
#Together 193 official UN member states. 2 countries are non-member observer states:
#the Holy See and the State of Palestine
countries_not_in_study=0
for country_WHO in countries_WHO:
    if country_WHO not in countries_study:
        countries_not_in_study+=1

#Assign World Regions according to WHO system
#WHO_WorldRegions = ['Africa','Eastern_Mediterranean','Europe',
#                    'Americas','Southeast_Asia','Western_Pacific']
country_region=[]
for country in countries_study:
    country_df = countries_WHO_region.loc[countries_WHO_region['Country']==country]
    region_name = country_df.values.tolist()[0][0]
    country_region.append(region_name)
est_cases_master.insert(1,'WHO_Region',country_region,True)

#Creating separate df for median, min, max
est_cases = est_cases_master.copy()    #.copy() ensures the original is not altered
est_cases_min = est_cases_master.copy()
est_cases_max = est_cases_master.copy()
est_cases_key_list = est_cases.columns.values.tolist()
est_cases_key_list = est_cases_key_list[2:]

for key in est_cases_key_list:
    est_cases_minmax_list=[]
    for num in est_cases_min[key].values:
        if '[' in num:
            est_cases_minmax_list.append(num)
        else:
            est_cases_minmax_list.append('nan')
    est_cases_min[key] = est_cases_minmax_list
    est_cases_max[key] = est_cases_minmax_list

#list1 = [num for num in range(10) if num<5 else num]
#print(list1)
for key in est_cases_key_list:
    est_cases[key] = [num.split('[')[0].replace(' ','') for num in est_cases[key].values]
    est_cases_min[key] = [num.split('[')[-1].split('-')[0].replace(' ','') for num in est_cases_min[key].values]
    est_cases_max[key] = [num.split('-')[-1].replace(']','').replace(' ','') for num in est_cases_max[key].values]
for key in est_cases_key_list:
    est_cases[key] = [int(num) for num in est_cases[key].values]
    est_cases_min[key] = [float(num) for num in est_cases_min[key].values]
    est_cases_max[key] = [float(num) for num in est_cases_max[key].values]

#Plotting cases by continent
WHO_region = est_cases.groupby('WHO_Region').sum().reset_index() #sums all data values by 'WHO_Region'
years = est_cases.columns.tolist()[2:]
WHO_year_sum=[]
for year in years:
    WHO_year_sum.append(est_cases[year].sum())

plt.figure()
ax=plt.subplot()
WHO_REGIONS = WHO_region['WHO_Region'].tolist()
for region in WHO_REGIONS:
    df = WHO_region[WHO_region['WHO_Region']==region]
    #total cases
    l = df.values.tolist()[0][1:]
    l = [num/(10**6) for num in l]
    plt.plot(range(len(years)), l, label=region)

ax.set_xticks(range(len(years)))
ax.set_xticklabels(years)
plt.xlabel('Year')
plt.ylabel('Cases (million people)')
plt.title('Total Number of Estimated Cases of Malaria by Region')
plt.legend()

# Pie Chart with Plotly Package
import plotly.express as px
fig1 = px.pie(WHO_region, values='2017', names='WHO_Region',
             title='Percentage of Worldwide Cases by WHO Region')
#fig.show(renderer='browser')
fig1.write_image("MalariaCasesPerc2017_WHOregion.pdf")

#Bar chart with Plotly
WHO_region_pivot = WHO_region.melt(id_vars='WHO_Region',
                                   var_name='Year',
                                   value_name='Cases')
WHO_region_pivot = WHO_region_pivot.pivot(
        columns='WHO_Region',
        index='Year',
        values='Cases').reset_index()
fig2 = px.bar(WHO_region_pivot,
              x='Year',
              y=WHO_region_pivot.columns.tolist()[1:],
              title='Worldwide Cases of Malaria',
              labels={'value':'Malaria Cases (million people)',
                      'variable':'WHO Region'})
fig2.write_image('MalariaCases2010_2017_WHOregion.pdf')

#Percentage of total worldwide cases
yearly_sum=[]
for year in years:
    yearly_sum.append(est_cases[year].values.sum())

plt.figure()
for region in WHO_REGIONS:
    row_list = WHO_region[WHO_region['WHO_Region']==region].values.tolist()[0][1:]
    perc_list = [(num1/num2)*100 for num1,num2 in zip(row_list,yearly_sum)]
    plt.plot(years, perc_list, label=region)
plt.xlabel('Year')
plt.ylabel('Total Share of World Cases (%)')
plt.title('Percentage of Worldwide Cases by Region')
plt.legend()

#incidence rate by continent
countries_study_inc=inc_cases['Country'].tolist()
inc_country_region=[]
for country in countries_study_inc:
    inc_country_region.append(countries_WHO_region[countries_WHO_region['Country']==country].values.tolist()[0][0])

inc_cases.insert(1,'WHO_Region',inc_country_region,True)
inc_cases_region = inc_cases.groupby('WHO_Region').mean().reset_index()
inc_years=inc_cases.columns.tolist()[2:]

plt.figure()
ax=plt.subplot()
for region in WHO_REGIONS:
    y = inc_cases_region[inc_cases_region['WHO_Region']==region].values.tolist()[0][1:]
    plt.plot(inc_years, y, label=region)

ax.set_xticks(range(len(inc_years)))
ax.set_xticklabels(inc_years, rotation=45)
plt.legend()
plt.xlabel('Year')
plt.ylabel('Estimated Cases (Number/1000 people at risk)')
plt.title('Estimated Incidence of Malaria Cases per 1000 people at risk')

SA=['Angola','Botswana','Eswatini','Lesotho','Malawi','Mozambique',
    'Namibia','South Africa','Zambia','Zimbabwe']
EA=['Comoros','Djibouti','Eritrea','Ethiopia','Kenya','Madagascar',
    'Mauritius','Rwanda','Seychelles','Somalia','South Sudan','Sudan',
    'United Republic of Tanzania','Uganda']
CA=['Burundi','Cameroon','Central African Republic','Chad',
    'Congo','Democratic Republic of Congo',
    'Equatorial Guinea','Gabon','Sao Tome and Principe']
NA=['Algeria','Egypt','Libyan Arab Jamahiriya','Morocco','Tunisia']
WA=['Benin','Burkina Faso','Cape Verde','Côte d\'Ivoire',
    'Gambia','Ghana','Guinea','Guinea-Bissau','Liberia',
    'Mali','Niger','Nigeria','Senegal','Sierra Leone','Togo','Mauritania']

Africa_REGIONS=[SA,EA,CA,NA,WA]
#Cross checking WHO and AU naming system
#rename mislabelled countries
for region in Africa_REGIONS:
    for country in region:
        if country not in countries_WHO:     #countries_WHO
            print('**Mislabelled: {}'.format(country))
            for name in African_countries_WHO:
                #print(country, name)
                if (country[-3:] or country[:3]) in name:
                    print('Could be this name {}'.format(name))

#Making a country list of the AU regions above
AU_country_list=[]
for region in Africa_REGIONS:
    for country in region:
        AU_country_list.append(country)
inc_cases_africa = inc_cases[inc_cases['Country'].isin(AU_country_list)].reset_index(drop=True)
inc_cases_africa = inc_cases_africa.drop('WHO_Region',axis=1)
inc_cases_africa_countrylist = inc_cases_africa['Country'].tolist()

AU_Dict={
        'SA':['Angola','Botswana','Eswatini','Malawi','Mozambique',
              'Namibia','South Africa','Zambia','Zimbabwe'],

        'EA':['Comoros','Djibouti','Eritrea','Ethiopia','Kenya','Madagascar',
              'Mauritius','Rwanda','Seychelles','Somalia','South Sudan','Sudan',
              'United Republic of Tanzania','Uganda'],

        'CA':['Burundi','Cameroon','Central African Republic','Chad',
              'Congo','Democratic Republic of Congo',
              'Equatorial Guinea','Gabon','Sao Tome and Principe'],

        'NA':['Algeria','Egypt','Libyan Arab Jamahiriya','Morocco','Tunisia'],

        'WA':['Benin','Burkina Faso','Cape Verde','Côte d\'Ivoire',
              'Gambia','Ghana','Guinea','Guinea-Bissau','Liberia',
              'Mali','Niger','Nigeria','Senegal','Sierra Leone','Togo','Mauritania']
        }

#Assiging an AU subregion to each African country
inc_cases_africa_regionlist=[]
for country in inc_cases_africa_countrylist:
    for region,countries in AU_Dict.items():
        if country in countries:
            inc_cases_africa_regionlist.append(region)

#print(inc_cases_africa_regionlist)
inc_cases_africa.insert(1,'AU_Region',inc_cases_africa_regionlist,True)

#Plotting subregions
inc_AU_region = inc_cases_africa.groupby('AU_Region').mean().reset_index()
plt.figure()
ax=plt.subplot()
for region,countries in AU_Dict.items():
    y = inc_AU_region[inc_AU_region['AU_Region']==region].values.tolist()[0][1:]
    plt.plot(inc_years, y, label=region)
ax.set_xticks(range(len(inc_years)))
ax.set_xticklabels(inc_years,rotation=45)
plt.legend()
plt.title('Incidence of Malaria by African Subregion')
plt.xlabel('Years')
plt.ylabel('Malaria Cases (Number/1000 people at risk)')

#Outcomes:
''' Figure 4 Shows the same trend for all African regions. Surprising.
Could be an indication that climat factors are important prevalence...
but not necessarily trend. Has climate changed trendwise?
    Do all African regions have a combined growth in:
        GDP
        Medical Funding / Net an Treatment Funding
    Does it have something to do with CLimate change, Mosquito prevalence,
    Rainfall/water prevalence trends etc.?
'''

#Plotting cases by selected African countries
plt.figure()
ax=plt.subplot()
i=1
for country in inc_cases_africa_countrylist:
        y = inc_cases_africa[inc_cases_africa['Country']==country].values.tolist()[0][2:]
        if i>=40 and i<50:
            plt.plot(inc_years, y, label=country)
        i+=1
plt.title('Incidence rate in selected countries')
plt.xlabel('Years')
plt.ylabel('Malaria Cases (Number/1000 people at risk)')
plt.legend()
ax.set_xticks(range(len(inc_years)))
ax.set_xticklabels(inc_years, rotation=45)
#num_afr = inc_cases_africa['Country'].nunique()
#print(num_afr)

#Plotting countries within selected African subregion
Africa_REGIONS_name=['SA','EA','CA','NA','WA']
chosen_region = 'SA'

plt.figure()
ax=plt.subplot()
for index,row in inc_cases_africa.iterrows():
    region = row.values.tolist()[1]
    if region == 'EA':
        y = row.values.tolist()[2:]
        country = row.values.tolist()[0]
        plt.plot(inc_years, y, label=country)

ax.set_xticks(range(len(inc_years)))
ax.set_xticklabels(inc_years, rotation=45)
plt.title('Incidence rate in selected countries')
plt.xlabel('Years')
plt.ylabel('Malaria Cases (Number/1000 people at risk)')
plt.legend()

#bar chart countries africa - total cases - Plotly
est_cases_african_countries = est_cases[est_cases['WHO_Region']=='Africa'].reset_index(drop=True)
est_cases_african_countries['est_cases_max_2017'] = est_cases_max[est_cases_max['WHO_Region']=='Africa']['2017'].reset_index(drop=True) - est_cases_african_countries['2017']
est_cases_african_countries['est_cases_min_2017'] = est_cases_african_countries['2017'] - est_cases_min[est_cases_min['WHO_Region']=='Africa']['2017'].reset_index(drop=True)
est_cases_african_countries = est_cases_african_countries.sort_values('2017')
fig4 = px.bar(est_cases_african_countries, x='2017', y='Country',
              title='Estimated Cases of Malaria in Africa', orientation='h',
              error_x_minus='est_cases_min_2017',
              error_x='est_cases_max_2017',
              labels={'2017':'Estimated Malaria Cases',
                      'Country':''
                      })
fig4.update_traces(error_x_color='blue',error_x_thickness=1)
fig4.write_image('EstimatedCases_Africa.pdf')
#print(fig4)


#bar chart countries africa - incidence cases
inc_cases_africa=inc_cases_africa.sort_values('2018').reset_index(drop=True)
fig3 = px.bar(inc_cases_africa, x='2018', y='Country', title='Estimated Incidence of Malaria Cases in Africa in 2018',
              color = 'AU_Region', color_discrete_sequence=px.colors.qualitative.Bold,
              orientation='h',
              labels={
                      '2018':'Incidene of Malaria Cases (Number/1000 people at risk)',
                      'Country':'',
                      'AU_Region':'African Union Region'
                      })
fig3.update_layout(yaxis_categoryorder = 'total ascending')

AU_Dict={'NA':'Northern Afica','WA':'Western Africa','SA':'Southern Africa',
         'CA':'Central Africa','EA':'Eastern Africa'}
for trace in fig3.data:
    for key,value in AU_Dict.items():
        if trace.name == key:
            trace.name=value
            break
fig3.write_image('Inc_Malaria_AfricanCountries.pdf')
#inc_cases_africa=inc_cases_africa.sort_values('Country').reset_index(drop=True)


####===============Correlations===================================
#Temperature
temp_df = pd.read_csv('climate/GlobalLandTemperaturesByCountry.csv')
temp_df = temp_df[temp_df['Country'].isin(inc_cases_africa_countrylist)].reset_index(drop=True)
temp_df['Year'] = [num.split('-')[0] for num in temp_df.Date.values]
temp_df= temp_df.groupby(['Country','Year']).mean().reset_index()
list5 = [str(num) for num in range(2000,2014)]
temp_df = temp_df[temp_df['Year'].isin(list5)].reset_index(drop=True)

temp_df_allyears=pd.DataFrame({'Country':[],'Year':[],'AverageTemperature':[],
        'AverageTemperatureUncertainty':[],'Malaria_Cases_Year':[]})
for Selected_Year in list5:
#Selected_Year='2010'
    temp_df_year = temp_df[temp_df['Year']==Selected_Year].reset_index(drop=True)
    temp_df_countries = temp_df_year['Country'].tolist()
    inc_cases_africa_chopped=inc_cases_africa[inc_cases_africa['Country'].isin(temp_df_countries)].reset_index(drop=True)

    temp_df_year=temp_df_year.sort_values('Country').reset_index(drop=True)
    inc_cases_africa_chopped=inc_cases_africa_chopped.sort_values('Country').reset_index(drop=True)
    temp_df_year['Malaria_Cases_Year']=inc_cases_africa_chopped[Selected_Year]
    temp_df_allyears=temp_df_allyears.append(temp_df_year)

fig5=px.scatter(temp_df_allyears, x='AverageTemperature', y='Malaria_Cases_Year')
fig5.show(renderer='browser')



# Rainfall







#================================================================================

'''Could fit a line to every country and figure out which has different trends
    Fit line to African regions, identify outlying countries
    sugges p
    Bar chart for malaria cases by Afrcan country in 2018 and in 2000
'''

"""
Line plots:
    1) Percentage of worldwide deaths due to Malaria?
    1) State absolute number of deaths per year worldwide
    1) Continets absolute and relative values
            i)Takeaways: percentage of world total
            ii) questions: why? What influencial factors?
    2) African countries averaged by subregion
    3) Plot cases per pop against possible influencial factors
    4) Plot cases against above for a sepcific year to find clusters
            (combine with clustering ML method?)


    5) Wich country accounts for highest share of worldwide cases
    6) Share of worldwide disease deaths

Could correlate with following data:
    Trend in average population age per region
    GDP growth per region
    % land that is water
    mosquito types
    healthcare funding
    parisite resistance to treatment
    moquito insecticide resistance
"""

#Workflow
'''
1) Establishing Africa is by far the highest absolute and relative cases
2) Break into subregions to find different trends
2) Looking into possible correlations (justify why I chose variables)
    a) plot line graphs and compare trend in years for same region/country
3) Looking for clusters by eye and with ML methods
'''


#Insights gained from Study
'''
Total number of worldwide cases in 2017: 219,001,657
#Worldwide_cases_2017 = WHO_region['2017'].sum()
#print('Worldwide cases in 2017: {}'.format(Worldwide_cases_2017))

Normalizing to the population, Africa is still many times higher
than the rest of the world (figure 3)
'''
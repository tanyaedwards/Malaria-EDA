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
import plotly.express as px
import math

def Names_Crosscheck(DF1_col, DF2_col, print_out=True):
    for country in DF1_col.tolist():
        if country not in DF2_col.tolist():
            if print_out==True:
                print(country)
            else:
                pass

def Rename(old_names, new_names, DF):
    for i in range(len(old_names)):
        DF = DF.replace(old_names[i],new_names[i])
    return DF
                    

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
fig1 = px.pie(WHO_region, values='2017', names='WHO_Region',
             title='Percentage of Worldwide Cases by WHO Region in 2017')
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
#with Plotly
years_list_inc = [str(num) for num in range(2000,2019)]
inc_cases_region_ = pd.melt(inc_cases_region, id_vars=['WHO_Region'], value_vars=years_list_inc,
                        var_name='Year', value_name='Inc_Cases')
fig7 = px.line(inc_cases_region_, x='Year', y='Inc_Cases', color='WHO_Region',
               title='Estimated Incidence of Malaria Cases per 1000 people at risk',
               labels={'Inc_Cases':'Estimated Cases (Number/1000 people at risk)'})
fig7.write_image('Figures/Inc_Malaria_WHORegion.pdf')

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
#with Plotly
inc_AU_region = pd.melt(inc_AU_region, id_vars=['AU_Region'], value_vars=years_list_inc,
                        var_name='Year', value_name='Inc_Cases')
fig8 = px.line(inc_AU_region, x='Year', y='Inc_Cases',
               title='Incidence of Malaria by African Subregion', color='AU_Region',
               labels={'Inc_Cases':'Malaria Cases (Number/1000 people at risk)'})
fig8.write_image('Figures/Inc_Malaria_AURegion.pdf')

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
              title='Estimated Cases of Malaria in Africa in 2017', orientation='h',
              error_x_minus='est_cases_min_2017',
              error_x='est_cases_max_2017',
              width=500,
              height=1500,
              labels={'2017':'Estimated Malaria Cases',
                      'Country':''
                      })
fig4.update_traces(error_x_color='blue',error_x_thickness=1)
fig4.write_image('EstimatedCases_Africa.pdf')
#print(fig4)

#top 5 countries as percentage of worldwide cases
total_cases = est_cases['2017'].sum()
est_cases['2017_Perc'] = (est_cases['2017']/total_cases)*100
est_cases_top5=est_cases[est_cases['2017_Perc']>3.8].sort_values('2017_Perc')
fig5 = px.bar(est_cases_top5, x='2017_Perc', y='Country',
              title='Highest Share of Estimated Malaria Cases',
              labels={'2017_Perc':'Percentage of Worldwide Cases (%)',
                      'Country':''
                      })
fig5.write_image('Top5.pdf')
est_cases = est_cases.drop('2017_Perc',axis=1)
#36% (over a third) of all cases are shared between two countries: Nigeria and DRC
#50% of all cases are come from 5 countries


#bar chart countries africa - incidence cases
inc_cases_africa=inc_cases_africa.sort_values('2018').reset_index(drop=True)
fig3 = px.bar(inc_cases_africa, x='2018', y='Country', title='Estimated Incidence of Malaria Cases in Africa in 2018',
              color = 'AU_Region', color_discrete_sequence=px.colors.qualitative.Bold,
              orientation='h',
              width=500,
              height=1500,
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
    temp_df_year = temp_df[temp_df['Year']==Selected_Year].reset_index(drop=True)
    temp_df_countries = temp_df_year['Country'].tolist()
    inc_cases_africa_chopped=inc_cases_africa[inc_cases_africa['Country'].isin(temp_df_countries)].reset_index(drop=True)

    temp_df_year=temp_df_year.sort_values('Country').reset_index(drop=True)
    inc_cases_africa_chopped=inc_cases_africa_chopped.sort_values('Country').reset_index(drop=True)
    temp_df_year['Malaria_Cases_Year']=inc_cases_africa_chopped[Selected_Year]
    temp_df_allyears=temp_df_allyears.append(temp_df_year)

fig5=px.scatter(temp_df_allyears, x='AverageTemperature', y='Malaria_Cases_Year')
#fig5.show(renderer='browser')
fig5.write_image('scatter.pdf')


#Reading and Organising World Weather Online Data
WWO_Africa_list=['Angola','Botswana','Lesotho','Malawi','Mozambique','Namibia','South_Sudan','Sudan',
             'South_Africa','Zambia','Zimbabwe','Comoros','Djibouti','Eritrea','Ethiopia','Kenya',
             'Madagascar','Tanzania','Uganda','Burundi','Cameroon','Central_African_Republic',
             'Chad','Democratic_Republic_of_Congo','Congo','Equatorial_Guinea','Gabon','Mauritius','Rwanda','Seychelles',
             'Somalia','Sao_Tome_and_Principe','Algeria','Egypt','Libya','Morocco','Tunisia',
             'Benin','Burkina_Faso','Cape_Verde', "Cote_d'Ivoire",'Gambia','Ghana','Guinea',
             'Guinea-Bissau','Liberia','Mali','Niger','Nigeria','Senegal','Sierra_Leone','Togo',
             'Mauritania']

WWO_years = [str(num) for num in range(2009,2018)] 
WWO_df_master = pd.read_csv('WeatherData_API/countries/2013/Algeria.csv')
WWO_df_columns = WWO_df_master.columns.tolist()
WWO_df_columns = WWO_df_columns[0:3] + WWO_df_columns[16:21] + WWO_df_columns[24:25]
WWO_df = pd.DataFrame()

for year in WWO_years:
    for country in WWO_Africa_list:
        WWO_df_master = pd.read_csv('WeatherData_API/countries/{}/{}.csv'.format(year,country))
        WWO_df = WWO_df.append(WWO_df_master[WWO_df_columns], ignore_index=True)

WWO_df['Year'] = [date.split('-')[0] for date in WWO_df['date_time'].values]
WWO_df = WWO_df.groupby(['location','Year']).mean().reset_index()
WWO_inc = inc_cases.drop(['WHO_Region'],axis=1)
WWO_inc = pd.melt(inc_cases, id_vars=['Country'], value_vars=WWO_years,
                  var_name='Year', value_name='Inc_Cases')

#cross checking WWO_inc naming system with WWO_df names
WWO_df['WWO_Country'] = [name.replace('_',' ') for name in WWO_df['location'].values]
Names_Crosscheck(WWO_df['WWO_Country'], WWO_inc['Country'], print_out=False)
old_names = ["Cote d'Ivoire",'Lesotho','Tanzania']       
new_names = ["Côte d'Ivoire",'Eswatini','United Republic of Tanzania']
for i in range(3):
    WWO_df['WWO_Country'] = [name.replace(old_names[i],new_names[i]) for name in WWO_df['WWO_Country'].values]
WWO_df = WWO_df.drop(['location'],axis=1)

#merging data frames
WWO_df = pd.merge(WWO_df, WWO_inc, how='inner', left_on=['WWO_Country','Year'], right_on=['Country','Year'])
WWO_df = WWO_df.drop('WWO_Country',axis=1)
WWO_Final_columns = WWO_df.columns.tolist()
WWO_Final_columns = [WWO_Final_columns.pop(8)] + WWO_Final_columns
WWO_df = WWO_df[WWO_Final_columns]

#Plotting Weather Features (World Weather Online) against Malaria Cases
for name in WWO_Final_columns[2:9]:
    fig6=px.scatter(WWO_df, x=name, y='Inc_Cases')
    fig6.write_image('Figures/scatter/{}.pdf'.format(name))
    
    
###---------------------------To Delete
# =============================================================================
# #Mosquito Nets
# #Does not state whether total nets or only nets provided by government / charities
# GlobalFund_df_master = pd.read_csv('Data/Global_Fund/GlobalFund_Malaria.csv')
# GlobalFund_df = GlobalFund_df_master[GlobalFund_df_master['Indicator'] == 'Mosquito nets distributed']
# GlobalFund_df = GlobalFund_df.rename(columns={'Location':'Country','Period':'Year'})
# 
# #Africa_list2 = [name.replace('_',' ') for name in WWO_Africa_list]
# Africa_list2=['Angola','Botswana','Eswatini','Malawi','Mozambique','Namibia','South Sudan','Sudan',
#               'South Africa','Zambia','Zimbabwe','Comoros','Djibouti','Eritrea','Ethiopia','Kenya',
#               'Madagascar','United Republic of Tanzania','Uganda','Burundi','Cameroon','Central African Republic',
#               'Chad','Democratic Republic of Congo','Congo','Equatorial Guinea','Gabon','Mauritius',
#               'Somalia','Sao Tome and Principe','Algeria','Egypt','Libya','Morocco','Tunisia',
#               'Benin','Burkina Faso','Cape Verde', "Côte d'Ivoire",'Gambia','Ghana','Guinea',
#               'Guinea-Bissau','Liberia','Mali','Niger','Nigeria','Senegal','Sierra Leone','Togo',
#               'Mauritania','Rwanda','Seychelles']
# # =============================================================================
# # print(GlobalFund_df_master['Location'].tolist())
# # print('')
# # for name in Africa_list2:
# #     if name not in GlobalFund_df_master['Location'].tolist():
# #         print(name)
# # =============================================================================
# GlobalFund_df = GlobalFund_df[GlobalFund_df['Country'].isin(Africa_list2)]
# Names_Crosscheck(GlobalFund_df_master['Location'], est_cases['Country'])
# =============================================================================

###----------------------------------------

#Pesticide 


#Malaria Cases Treated

#Funding per Capita by Country and Year
Funding_df = pd.read_excel('Data/WHO/funding.xls',sheet_name='Funding')
column_list = ['Unnamed: {}'.format(str(num)) for num in range(7,15)]
Funding_df = Funding_df.drop(column_list,axis=1)
column_list = ['Country', 'Year', 'Global_Fund', 'PMI_USAID', 'World_Bank', 'UK', 'Government (local)']
Funding_df.columns = column_list
Funding_df = Funding_df.drop([0,1,2,3],axis=0)
Funding_df = Funding_df.drop(range(289,302),axis=0)
row_list = ['AFRICAN','SOUTH-EAST ASIA','AMERICAS','EASTERN MEDITERRANEAN','WESTERN PACIFIC']
for i in range(len(row_list)):
    Funding_df = Funding_df.drop(Funding_df[Funding_df['Country']==row_list[i]].index,axis=0)
Funding_df = Funding_df.replace(['United Republic of Tanzania9'],'United Republic of Tanzania')
Funding_df = Funding_df.replace(['South Sudan8'],'South Sudan')
Funding_df = Funding_df.reset_index(drop=True)
Funding_df = Funding_df.drop([279],axis=0)
count=0
for cell in Funding_df['Country'].values:
    if count%3 == 0:
        country = cell
    if count%3 != 0:
        Funding_df.at[count, 'Country'] = country
    count += 1
    
#remove Parag. bc no Government data given
Funding_df = Funding_df.drop([188],axis=0).reset_index(drop=True)
#convert values to float and sum rows
column_list = ['Global_Fund', 'PMI_USAID', 'World_Bank', 'UK', 'Government (local)']
Funding_df[column_list] = Funding_df[column_list].apply(pd.to_numeric)

#Could find exchange rate for each country and apply it to Government column
Funding_exchange = pd.read_csv('Data/World_Bank/Exchange_Rates/Exchange_Rates.csv')
Funding_exchange = Funding_exchange.drop(['Country Code','Indicator Name','Indicator Code','Unnamed: 64'],axis=1)
Funding_exchange = Funding_exchange.rename(columns={'Country Name':'Country'})
years=[str(num) for num in range(2016,2019)]
Funding_exchange = pd.melt(Funding_exchange, id_vars='Country', value_vars=years,
                           var_name='Year', value_name='Exchange_Rate')
Funding_exchange['Year'] = pd.to_numeric(Funding_exchange['Year'])
Funding_df = pd.merge(Funding_df, Funding_exchange, how='left', left_on=['Country','Year'],
                      right_on=['Country','Year'])
Funding_df['Government (USD)'] = Funding_df['Government (local)']/Funding_df['Exchange_Rate']
#crosschecking and renaming country names
Funding_df.loc[Funding_df['Country']=='Democratic Republic of the Congo', ['Country']] = 'Democratic Republic of Congo'
old_names = ['Congo, Dem. Rep.','Congo, Rep.',"Cote d'Ivoire",'Gambia, The','Tanzania']
new_names = ['Democratic Republic of Congo','Congo',"Côte d'Ivoire",'Gambia',
             'United Republic of Tanzania']
Funding_exchange = Rename(old_names, new_names, Funding_exchange)
Names_Crosscheck(Funding_df['Country'],Funding_exchange['Country'], print_out=False)
#summing Malaria Funding
column_list_funding = ['Global_Fund', 'PMI_USAID', 'World_Bank', 'UK', 'Government (USD)']
Funding_df['Total_Funding'] = Funding_df[column_list_funding].sum(axis=1)
for i in Funding_df.index:
    if math.isnan(Funding_df.at[i,'Exchange_Rate'])==True:
        Funding_df.at[i,'Total_Funding'] = float('NaN')

Funding_df['Year'] = pd.to_numeric(Funding_df['Year'])
Funding_inc = inc_cases_africa.drop('AU_Region',axis=1)

#cross checking names in first data frame
Africa_list=['Angola','Botswana','Eswatini','Malawi','Mozambique','Namibia','South Sudan','Sudan',
             'South Africa','Zambia','Zimbabwe','Comoros','Djibouti','Eritrea','Ethiopia','Kenya',
             'Madagascar','United Republic of Tanzania','Uganda','Burundi','Cameroon','Central African Republic',
             'Chad','Democratic Republic of the Congo','Congo','Equatorial Guinea','Gabon','Mauritius',
             'Somalia','Sao Tome and Principe','Algeria','Egypt','Libya','Morocco','Tunisia',
             'Benin','Burkina Faso','Cape Verde', "Côte d'Ivoire",'Gambia','Ghana','Guinea',
             'Guinea-Bissau','Liberia','Mali','Niger','Nigeria','Senegal','Sierra Leone','Togo',
             'Mauritania','Rwanda','Seychelles']
for name in Africa_list:
   if name not in Funding_df['Country'].tolist():
       #print(name)
       pass
#cross checking names between DF
Names_Crosscheck(Funding_inc['Country'], Funding_df['Country'], print_out=False)      
Funding_years = [str(num) for num in range(2000,2019)]
Funding_inc = pd.melt(inc_cases_africa, id_vars='Country', value_vars=Funding_years,
                      var_name='Year', value_name='Inc_Cases')
Funding_inc['Year'] = pd.to_numeric(Funding_inc['Year'])
Funding_df = pd.merge(Funding_df, Funding_inc, how='inner', 
                      left_on=['Country','Year'], right_on=['Country','Year'])

#Need to plot Total_Funding/population for that year
Pop_df = pd.read_csv('Data/World_Bank/Population/Population.csv')
Pop_df = Pop_df.drop(['Country Code','Indicator Name','Indicator Code','Unnamed: 64'],axis=1)
Pop_years = [str(num) for num in range(2016,2019)]
Pop_df = pd.melt(Pop_df, id_vars='Country Name', value_vars=Pop_years,
                 var_name='Year', value_name='Population')

Names_Crosscheck(Funding_df['Country'], Pop_df['Country Name'], print_out=False)  
Pop_df = Rename(old_names, new_names, Pop_df)
Pop_df['Year'] = pd.to_numeric(Pop_df['Year'])
Funding_df = pd.merge(Funding_df, Pop_df, how='inner', 
                      left_on=['Country','Year'], right_on=['Country Name',"Year"])
Funding_df = Funding_df.drop('Country Name',axis=1)
Funding_df['Funding_per_capita'] = Funding_df['Total_Funding']/Funding_df['Population']

#Anomoly_list = Funding_df.index[Funding_df['Funding_per_capita']>300].tolist()

#adding est_cases to data frame
years=[str(num) for num in range(2016,2018)]
Funding_est = pd.melt(est_cases, id_vars='Country', value_vars=years,
                      var_name='Year', value_name='Est_Cases')
Funding_est['Year'] = pd.to_numeric(Funding_est['Year'])
Funding_df = pd.merge(Funding_df, Funding_est, how='left', left_on=['Country','Year'],
                      right_on=['Country','Year'])

#adding est perc of population with Malaria
Funding_df['Pop_Perc_Est_Cases'] = Funding_df['Est_Cases']/Funding_df['Population']

#adding percentage of population with ITN access to dataframe
Funding_ITN = pd.read_excel('Data/WHO/ITN.xls', sheet_name='ITN')
Funding_ITN_columns = Funding_ITN.columns.tolist()
Funding_ITN = Funding_ITN.rename(columns={'WHO region\nCountry/area':'Country',
                                          'Modelled percentage of population with access to an ITN':'Pop_Perc_ITN'})
for i in Funding_ITN.index:
    if Funding_ITN.at[i,'Pop_Perc_ITN'] == '-':
        #print(i)
        Funding_ITN = Funding_ITN.drop([i],axis=0)
Funding_ITN = Funding_ITN.reset_index(drop=True)
count=0
for cell in Funding_ITN['Country'].values:
    if count%3 == 0:
        country = cell
    if count%3 != 0:
        Funding_ITN.at[count, 'Country'] = country
    count += 1
Names_Crosscheck(Funding_ITN['Country'], Funding_df['Country'], print_out=False)
Funding_ITN = pd.merge(Funding_ITN, Funding_df, how='inner', left_on=['Country','Year'],
                       right_on=['Country','Year'])

#Plotting
fig9 = px.scatter(Funding_df, x='Funding_per_capita', y='Inc_Cases')#range_x=[0,50]
fig9.write_image('Figures/scatter/Funding.pdf')

fig12 = px.scatter(Funding_df, x='Total_Funding', y='Pop_Perc_Est_Cases')
fig12.write_image('Figures/scatter/Funding_PopPercCases.pdf')

#plotting avg funding_per_capita and inc_cases by year
Funding_Africa_Year = Funding_df.groupby('Year').mean().reset_index()
for value in ['Funding_per_capita','Inc_Cases','Est_Cases']:
    fig10 = px.bar(Funding_Africa_Year, x='Year', y=value)
    fig10.write_image('Figures/Funding_{}.pdf'.format(value))
    
fig11 = px.scatter(Funding_ITN, x='Pop_Perc_ITN', y='Inc_Cases')
fig11.write_image('Figures/scatter/ITN_Inc.pdf')

fig12 = px.scatter(Funding_ITN, x='Pop_Perc_ITN', y='Pop_Perc_Est_Cases')
fig12.write_image('Figures/scatter/ITN_PopPercCases.pdf')





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
    mosquito type?
    Malaria Funding
    mosquito nets
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

#Suggestions to look into
'''
Whether increased Pesticide use coincides with higher rates of other illnesses
'''

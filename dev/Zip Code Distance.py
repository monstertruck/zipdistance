
# coding: utf-8

# ## Data Question
# How much of a difference does it make to use Zip distances over geocoded address (lat/lon) distances?

# In[2]:

import numpy as np
import pandas as pd
import csv
import urllib
import matplotlib.pyplot as plt
from geopy.distance import vincenty
from collections import defaultdict
import configparser
import folium
import json

# Manage the API keys in a separate .ini file.
APIKEYS = configparser.ConfigParser()
APIKEYS.read('../APIKeys.ini');

# Get the keyname (client_id?) and actual API key.
keyname = APIKEYS['opendata']['keyname']
thekey = APIKEYS['opendata']['key']

# Generate the correct API call.
schfile = "https://data.cityofnewyork.us/resource/9pyc-nsiu.json?$limit=100000&$$" + keyname + "=" + thekey + "&$order=ats_system_code"

# Get school locations from NYC OpenData API
schresp  = urllib.request.urlopen(schfile).read()
sch_data = pd.read_json(schresp)

# print(list(sch_data))

# Only take the columns we need.
sch = sch_data[['administrative_district_code', 'ats_system_code','beds_number','school_year','latitude','longitude','primary_address','zip']]

# Do a little 'cleaning'
sch = sch[sch['school_year'] == '2015-16']
sch = sch[sch['latitude']    != None]
sch = sch[sch['longitude']   != 0]

# Also want CSD schools and not district 75 (special ed)
sch = sch[sch['administrative_district_code'] < 40]


# In[13]:




# In[23]:

# choropleth map
# geo_str = json.dumps(json.load(open(geo_path, 'r')))
# threshold_scale = np.linspace(df['2013'].min(),
#                               df['2013'].max(), 6, dtype=int).tolist()

mapa = folium.Map(location=[40.739666, -73.983314], width = '70', 
                  tiles="Mapbox Bright",
                  zoom_start=11)

# mapa.geo_json(geo_str=geo_str,
#               data=df,
#               columns=['state', '2013'],
#               fill_color='YlGn',
#               key_on='feature.id',
#               threshold_scale=threshold_scale)

mapa

# location map


# ## Question 1: What is the longest distance between schools in the same zip code?

# In[3]:

zips = np.unique(sch['zip'])

# Find the max by BRUTE FORCE    
school1   = np.array(range(len(zips)), dtype='a7')
school2   = np.array(range(len(zips)), dtype='a7')
maxdistance = np.empty(len(zips))

for i in range(len(zips)):
    # Schzip now has all of the schools in the zip code
    schzip = sch[sch['zip'] == zips[i]]
          
    distance  = np.empty(len(schzip))
    distancey = np.empty(len(schzip))
    schooly   = np.array(range(len(schzip)), dtype='a7')
    
    # Loop through 
    for j in range(len(schzip)):
        for k in range(len(schzip)):
            # Calculate the distance between each 
            try:
                distance[k] = vincenty(schzip[['latitude','longitude']].iloc[j],schzip[['latitude','longitude']].iloc[k]).miles
            except UnboundLocalError:
                distance[k] = 0
        # Get the maximum distance over the second dimension ('school y')
        distancey[j] = max(distance)
        # Record the school name for the longest distance over y dimension.
        schooly[j]   = schzip['ats_system_code'].iloc[np.argmax(distance)]
    # Now get the maximum distance over the first dimension (over maxed second dimensions)
    maxdistance[i] = max(distancey)
    # This is the school of the y dimension
    school1[i] = schzip['ats_system_code'].iloc[np.argmax(distancey)]
    # This is the school of the x dimension.
    school2[i] = schooly[np.argmax(distancey)]
        
print(school1)
print(school2)
print(maxdistance)


# Assemble an array of [Zip, Distance, School1, School2]


# In[12]:




# ## Question 2: What is the average distance between schools in the zip code?

# ## Question X: What is the transit time for the longest 

# In[ ]:




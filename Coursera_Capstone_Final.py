#!/usr/bin/env python
# coding: utf-8

# In[133]:


import numpy as np
import pandas as pd
from pandas import DataFrame
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
import requests
from pandas.io.json import json_normalize
#!conda install -c conda-forge folium=0.5.0 --yes
import folium


print('Completed')


# In[134]:


client_id = 'IWHVMX4LERJWS0TVZAQKIMNKSV112LMFATGEDOGMB0IBI0UH'
client_secret = '2PEAYMQS2ZUEOCLWZ1CMUEYL3SVUACGIMYV5S1MKVAORORUN'
version = '20180604'
limit = 100
print('Connected to FourSquare')

#add cities to lookup
cities = ['New York, NY','San Francisco, CA', 'Baltimore, MD', 'Boston, MA', 'Philadelphia, PA', 'New Orleans, LA', 'Seattle, WA', 'Los Angeles, CA', 'Chicago, IL', 'Washington DC']
results = {}
for city in cities:
    url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&near={}&limit={}&categoryId={}'.format(
        client_id, 
        client_secret, 
        version, 
        city,
        limit,
        "4bf58dd8d48988d181941735") # Museum category
    results[city] = requests.get(url).json()


# In[135]:


#create dataframe for Museums
df_venues={}
for city in cities:
    venues = json_normalize(results[city]['response']['groups'][0]['items'])
    df_venues[city] = venues[['venue.name', 'venue.location.address', 'venue.location.lat', 'venue.location.lng']]
    df_venues[city].columns = ['Name', 'Address', 'Lat', 'Lng']


# In[136]:


df_venues


# In[137]:


#create dataframe for cities researching
cities_df = DataFrame(cities, columns = ['City'])
cities_df


# In[138]:


#all of the information from foursquare
results


# In[139]:


#creating maps for all cities
maps = {}
#creating a list of all mean distances
meandist = []
#creating a list of total museums
count = []
#creating a list for central location
central = []
for city in cities:
    city_lat = np.mean(results[city]['response']['geocode']['center']['lat'])
    city_lng = np.mean(results[city]['response']['geocode']['center']['lng'])
    maps[city] = folium.Map(location=[city_lat, city_lng], zoom_start=11)
    venues_coor = [df_venues[city]['Lat'].mean(), df_venues[city]['Lng'].mean()]
    for lat, lng, label in zip(df_venues[city]['Lat'], df_venues[city]['Lng'], df_venues[city]['Name']):
        # marker for museums
        label = folium.Popup(label, parse_html=True)
        folium.CircleMarker(
            [lat, lng],
            radius=5,
            popup=label,
            color='blue',
            fill=True,
            fill_color='#3186cc',
            fill_opacity=0.7,
            parse_html=False).add_to(maps[city])  
        #marker for central point
        label = folium.Popup("Center Point", parse_html=True)
        folium.CircleMarker(
            venues_coor,
            radius=5,
            popup=label,
            color='black',
            fill=True,
            fill_color='black',
            fill_opacity=0.7,
            parse_html=False).add_to(maps[city])      
    #print information about each city    
    print(f"Total number of museums in {city} = ", results[city]['response']['totalResults'])
    if results[city]['response']['totalResults'] > 100:
        print("Showing Top 100")
        print("Mean Distance from Center Point is:")
        print(np.mean(np.apply_along_axis(lambda x: np.linalg.norm(x - venues_coor),1,df_venues[city][['Lat','Lng']].values)))
    else: 
        print("Showing All ", results[city]['response']['totalResults'])
        print("Mean Distance from Center Point is:")
        print(np.mean(np.apply_along_axis(lambda x: np.linalg.norm(x - venues_coor),1,df_venues[city][['Lat','Lng']].values)))
    
    #adding data to the lists created above
    meandist.append(np.mean(np.apply_along_axis(lambda x: np.linalg.norm(x - venues_coor),1,df_venues[city][['Lat','Lng']].values)))
        
    count.append(results[city]['response']['totalResults'])
    
    central.append(venues_coor)


# In[140]:


#show New York
print(cities[0])
print(meandist[0])
maps[cities[0]]


# In[141]:


#show San Francisco
print(cities[1])
print(meandist[1])
maps[cities[1]]


# In[142]:


#Show Baltimore
print(cities[2])
print(meandist[2])
maps[cities[2]]


# In[143]:


#Show Boston
print(cities[3])
print(meandist[3])
maps[cities[3]]


# In[144]:


#Show Philadelphia
print(cities[4])
print(meandist[4])
maps[cities[4]]


# In[145]:


#Show New Orleans
print(cities[5])
print(meandist[5])
maps[cities[5]]


# In[146]:


#Show Seattle
print(cities[6])
print(meandist[6])
maps[cities[6]]


# In[147]:


#Show Los Angeles
print(cities[7])
print(meandist[7])
maps[cities[7]]


# In[148]:


#Show Chicago
print(cities[8])
print(meandist[8])
maps[cities[8]]


# In[149]:


#Show Washington DC
print(cities[9])
print(meandist[9])
maps[cities[9]]


# In[152]:


#Add Mean distance and total museums to dataframe
cities_df['Mean Distance'] = meandist
cities_df['Total Museums'] = count
cities_df['Max Museums Reviewed'] = np.where(cities_df['Total Museums']>100,100,cities_df['Total Museums'])
cities_df['Latitude, Longitude'] = central
cities_df = cities_df.set_index("City", drop = True)


# In[153]:


#Show dataframe
cities_df


# In[154]:


#connecting to foursquare and finding the closest hotel near the central location
client_id = 'IWHVMX4LERJWS0TVZAQKIMNKSV112LMFATGEDOGMB0IBI0UH'
client_secret = '2PEAYMQS2ZUEOCLWZ1CMUEYL3SVUACGIMYV5S1MKVAORORUN'
version = '20180604'
limit = 1
search_query = 'Hotel'
latlong = '38.89751372885385, -77.02835154630353'
radius = 500

#add LatLong to lookup
results = {}
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={}&v={}&query={}&radius={}&limit={}'.format(
        client_id, 
        client_secret, 
        latlong,
        version,
        search_query,
        radius,
        limit)
results = requests.get(url).json()


# In[155]:


#closest hotel to central location of museums
results


# In[157]:


hotels = results['response']['venues']
dataframe = json_normalize(hotels)
filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
dataframe_filtered = dataframe.loc[:, filtered_columns]
# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]
#showing the closest hotel
dataframe_filtered


# In[ ]:





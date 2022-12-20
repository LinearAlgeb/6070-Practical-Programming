import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## Web-Scraping

# Scraping passengers' hometown to a new dataset

wiki1 = pd.read_html('https://en.wikipedia.org/w/index.php?title=Passengers_of_the_RMS_Titanic&oldid=883859055', header=0)[0]
wiki2 = pd.read_html('https://en.wikipedia.org/w/index.php?title=Passengers_of_the_RMS_Titanic&oldid=883859055', header=0)[1]
wiki3 = pd.read_html('https://en.wikipedia.org/w/index.php?title=Passengers_of_the_RMS_Titanic&oldid=883859055', header=0)[2]

wiki1.head()
wiki2.head()
wiki3.head()

wiki3['Hometown'] = wiki3['Hometown'] + ', ' + wiki3['Home country']
wiki3 = wiki3.drop('Home country', axis=1, errors='ignore')

wiki = pd.concat([wiki1, wiki2, wiki3], ignore_index=True)
wiki

## World Map

wiki = wiki[['Name','Hometown']]
wiki.sort_values(by=['Name'],ascending=True)

wiki.dtypes

wiki[['city','H1']] = wiki['Hometown'].str.split(',', 1, expand=True)
wiki[['state','H2']] = wiki['H1'].str.split(',', 1, expand=True)
wiki[['province','country']] = wiki['H2'].str.split(',', 1, expand=True)
wiki

wiki['H2'] = wiki['H2'].fillna(wiki.pop('state'))
wiki['province'] = wiki['province'].fillna(wiki.pop('H2'))
wiki['country'] = wiki['country'].fillna(wiki.pop('province'))
wiki

#calculate the population who share the same home country
w2 = pd.DataFrame(wiki['country'].value_counts().reset_index())
w2.columns = ['country', '#ofpassengers']
print(w2.shape)
print(w2.dtypes)
w2
#pay attention to ['country'] with [note #], e.g.German Empire, Ottoman Empire, etc.
#and also [England, Ireland, UK, etc.]
#Manual work needed

#w2.to_csv('/content/drive/MyDrive/Final_Project/w2.csv')

#after manual work done on w2.csv, reload
w3 = pd.read_csv('/content/drive/MyDrive/Final_Project/w2.csv')
w3 = w3[['Country','#ofpassengers']]
w3

#Hometown World Map
!pip install geojson
!pip install geopandas

import geopandas as gp
import geojson as gpd

worldmap = gp.read_file('/content/drive/MyDrive/Final_Project/world.geojson')
worldmap.head(3)

worldmap.rename(columns={'NAME': 'Country','NAME_LONG': 'Country_long'}, inplace=True)
worldmap

w = worldmap.merge(w3, on='Country')
print(w.shape)
w
# Pay attention to 'Unknown' and 'Monaco'.
# Monaco not found in geojson.

# Plot
fig, ax = plt.subplots(1, 1, figsize = (32,20))

w.plot(column='#ofpassengers', ax=ax, edgecolor='#a2cccc', cmap='GnBu', legend = True)

for idx, row in w.iterrows():
    plt.annotate(s=row['ADM0_A3'], xy=row['coords'],
                 horizontalalignment='center')
plt.title('Hometown of Passengers', fontsize = 24)

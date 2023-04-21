# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 11:45:36 2023

@author: Dev_Env
"""

import urllib.request
import json
import plotly.express as px

# Download the world countries dataset from Natural Earth as a GeoJSON file
url = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_countries.geojson"
filename = "world_countries.geojson"
urllib.request.urlretrieve(url, filename)

# Load the GeoJSON file into a dataframe using Plotly Express
with open(filename) as f:
    geojson_data = json.load(f)

df = px.data.geojson(geojson_data)

# Create a Choropleth map using the dataframe and a Carto base map
fig = px.choropleth(df, color="your_variable_here", geojson=geojson_data['features'],
                    locations=df.index, featureidkey="properties.sov_a3",
                    projection="mercator", scope="world",
                    color_continuous_scale="Viridis",
                    basemap=px.maps.carto.WorldDark)
fig.show()

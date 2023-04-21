import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import geopandas as gpd

from geopy.geocoders import Nominatim


# Read the CSV file into a pandas DataFrame
df = pd.read_csv('Methane_final.csv')

# Drop rows where the country is "world"
df = df.drop(df[df['country'] == 'World'].index)

# Group the remaining rows by country and sum the values
df_grouped = df.groupby('country').sum().reset_index()

# Download the GeoJSON file for world countries
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the GeoDataFrame with your DataFrame
merged = world.merge(df_grouped, left_on='name', right_on='country')

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Choropleth Map'),
    dcc.Graph(
        id='choropleth-map',
        figure=px.choropleth_mapbox(
            data_frame=merged,
            geojson=merged['geometry'],
            locations='country',
            color='emissions',
            featureidkey='properties.name',
            mapbox_style='carto-positron',
            center={'lat': 50, 'lon': 50},
            zoom=2,
            opacity=0.5,
            labels={'emissions': 'Emissions'}
        ),
        style={'height': '1200px'}
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(port=8050)
    
    
    
    
    
    
    
    
# Print out the merged DataFrame
print(merged)

# Check for missing values in the "geometry" column
print(merged['geometry'].isnull().sum())

import plotly.io as pio
pio.renderers.default = "browser"
import plotly.express as px

fig = px.choropleth_mapbox(
    merged, 
    geojson=merged.geometry, 
    locations=merged.index, 
    color='emissions',
    featureidkey='properties.name',
    mapbox_style='carto-positron',
    center={'lat': 50, 'lon': 50},
    zoom=2,
    opacity=0.5,
    labels={'emissions': 'emissions'}
)

fig.show()
import dash
import json
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
import plotly.graph_objs as go
# Read the CSV file into a pandas DataFrame
df = pd.read_csv('Methane_final.csv')

# Drop rows where the country is "world"
df = df.drop(df[df['country'] == 'World'].index)

# Group the remaining rows by country and sum the values
df_grouped = df.groupby('country').sum().reset_index()

world_path = pd.read_json('custom.geo.json', encoding='UTF-8')
#world_path = ('custom.geo.json',encoding='UTF-8')
#world_path=open('custom.geo.json',encoding='utf-8')
with open('custom.geo.json', encoding='utf-8') as f:
    geo_world = json.load(f)





from pathlib import Path
import json

world_path = Path('custom.geo.json')
with world_path.open(encoding='utf-8') as f:
    geo_world = json.load(f)
    

# Instanciating necessary lists
found = []
missing = []
countries_geo = []

# For simpler acces, setting "zone" as index in a temporary dataFrame
tmp = df_grouped.set_index(["emissions"])


# Looping over the custom GeoJSON file
for country in geo_world['features']:
    
    # Country name detection
    country_name = country['properties']['name'] 
    
    # Checking if that country is in the dataset
    if country_name in tmp.index:
        
        # Adding country to our "Matched/found" countries
        found.append(country_name)
        
        # Getting information from both GeoJSON file and dataFrame
        geometry = country['geometry']
        
        # Adding 'id' information for further match between map and data 
        countries_geo.append({
            'type': 'Feature',
            'geometry': geometry,
            'id':country_name
        })
        
    # Else, adding the country to the missing countries
    else:
        missing.append(country_name)

# Displaying metrics
print(f'Countries found    : {len(found)}')
print(f'Countries not found: {len(missing)}')
geo_world_ok = {'type': 'FeatureCollection', 'features': countries_geo}


print(found)
















df.head

# Create a Dash app
app = dash.Dash()

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Choropleth World Map'),
    dcc.Graph(
        id='world-map',
        figure={
            'data': [go.Choropleth(
                locations=df_grouped['country'],
                z=df_grouped['emissions'],
                text=df_grouped['country'],
                colorscale='Viridis',
                autocolorscale=False,
                reversescale=True,
                marker_line_color='darkgray',
                marker_line_width=0.5,
                colorbar_title='GDP per capita'
            )],
            'layout': go.Layout(
                title='GDP per capita by country',
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type='equirectangular'
                )
            )
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
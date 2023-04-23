# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 00:29:11 2023

@author: Mathias Profft
"""

#Import necessary libraries

import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Load data from CSV file
df = pd.read_csv('Methane_final.csv', usecols=['baseYear', 'region', 'country', 'segment', 'emissions'])

#Filter data for the year 2022 and exclude the 'World' region
df = df.query('baseYear == "2022" and region != "World"')

#Group data by country and segment, aggregate emissions, and keep the first values of baseYear and region columns
df = df.groupby(['country', 'segment']).agg({
    'emissions': 'sum',  # sum the emissions column
    'baseYear': 'first',  # keep the first value of the baseYear column
    'region': 'first'  # keep the first value of the region column
}).reset_index()


#Group data by country and segment, sum the emissions, and reset the index
grouped_df = df.groupby(['country', 'segment']).sum().reset_index()

#Group data by region and segment, sum the emissions, and reset the index
region_segment_df = grouped_df.groupby(['region', 'segment']).sum().reset_index()

#Count the number of unique countries in each region and calculate the emissions per country
country_count = region_segment_df.groupby('region')['country'].count()
region_segment_df['emissions'] = region_segment_df['emissions'] / region_segment_df['region'].map(country_count)

#Merge the grouped data with the emissions per country data and keep only the necessary columns
result_df = grouped_df.merge(region_segment_df[['region', 'segment', 'emissions']], on=['region', 'segment'], how='left')

#Create a Dash application
app = dash.Dash(__name__)

# Define options for dropdown filters for segment
segment_options = [{'label': i, 'value': i} for i in df['segment'].unique()]

# Define layout for stacked bar chart
stacked_bar_chart_layout = dict(title=None, height=800, width=700, margin=dict(l=0, r=0, t=40, b=0))
stacked_bar_chart_trace = dict(x='emissions', y='region', color='country', barmode='stack', orientation='h', hovertemplate="Country: %{color}<br>Region: %{y}<br>Emissions: %{x}")

#Define layout for choropleth map
choropleth_map_layout = dict(title='Emissions by Country', height=800, width=950, margin=dict(l=0, r=0, t=40, b=0))
choropleth_map_trace = dict(locations='country', locationmode='country names', color='emissions', projection='orthographic', hover_name='country')

# Define options for dropdown filters for projection
projection_options = [{'label': 'Equirectangular', 'value': 'equirectangular'}, {'label': 'Mercator', 'value': 'mercator'}, {'label': 'Orthographic', 'value': 'orthographic'}, {'label': 'Natural Earth', 'value': 'natural earth'}, {'label': 'Kavrayskiy7', 'value': 'kavrayskiy7'}, {'label': 'Miller', 'value': 'miller'}, {'label': 'Robinson', 'value': 'robinson'}, {'label': 'Eckert4', 'value': 'eckert4'}, {'label': 'Azimuthal Equal Area', 'value': 'azimuthal equal area'}, {'label': 'Azimuthal Equidistant', 'value': 'azimuthal equidistant'}, {'label': 'Conic Equal Area', 'value': 'conic equal area'}, {'label': 'Conic Conformal', 'value': 'conic conformal'}, {'label': 'Conic Equidistant', 'value': 'conic equidistant'}, {'label': 'Gnomonic', 'value': 'gnomonic'}, {'label': 'Stereographic', 'value': 'stereographic'}, {'label': 'Mollweide', 'value': 'mollweide'}, {'label': 'Hammer', 'value': 'hammer'}, {'label': 'Transverse Mercator', 'value': 'transverse mercator'}]

# Define main layout
app.layout = html.Div([
    html.H1("Methane Emissions of different segments in 2022"),
    html.Button('Country View/Accumulated Region', id='switch_data_button', n_clicks=0),
    html.Div([
        html.Div([
            html.Label("Segment"),
            dcc.Dropdown(id='segment_dropdown',
                         options=segment_options,
                         value=[df['segment'].iloc[7]],
                         multi=True)
        ], className="filter", style={"width": "50%", "display": "inline-block"}),
        html.Div([
            html.Label("Projection"),
            dcc.Dropdown(id='projection_dropdown',
                         options=projection_options,
                         value='orthographic')
        ], className="filter", style={"width": "50%", "display": "inline-block"}),
    ], className="filter-container"),
    html.Div([
        html.Div([
            dcc.Graph(id="stacked_bar_chart", figure=dict(layout=stacked_bar_chart_layout, data=[]))
        ], className="chart-container", style={"width": "50%"}),
        html.Div([
            dcc.Graph(id="choropleth_map", figure=dict(layout=choropleth_map_layout, data=[])),
            
        ], className="chart-container", style={"width": "50%"})
    ], className="chart-section", style={"display": "flex"}),
    
])


# Define callback function to update figures based on user input
@app.callback(
    [Output('stacked_bar_chart', 'figure'),
     Output('choropleth_map', 'figure')],
    [Input('segment_dropdown', 'value'),
     Input('projection_dropdown', 'value'),
     Input('switch_data_button', 'n_clicks'),])
def update_figures(segment_value, projection_value, n_clicks):
    # Declare global variables
    global filtered_df
    global df
    global new_df
    # Update filtered dataframe based on user input
    if n_clicks % 2 == 0:
        filtered_df = df[df['segment'].isin(segment_value)]
    
        # Create stacked bar chart
        stacked_bar_chart = px.bar(filtered_df, x='emissions', y='region', color='country', barmode='stack', orientation='h')
        stacked_bar_chart.update_layout(title=f"Emissions by Region ({', '.join(segment_value)})")
        stacked_bar_chart.update_traces(hovertemplate="Emissions: %{x}")
        stacked_bar_chart.update_xaxes(title_text='Emissions (kt of CO2 equivalent)')

        # Create choropleth map
        choropleth_map = px.choropleth(filtered_df, locations='country', locationmode='country names', color='emissions',projection=projection_value, hover_name='country')
        choropleth_map.update_layout(title=f"Emissions by Country ({', '.join(segment_value)})", geo=dict(showframe=False, showcoastlines=True, projection_scale=1))
    else:
        filtered_df = result_df[result_df['segment'].isin(segment_value)]

    # Create stacked bar chart
        stacked_bar_chart = px.bar(filtered_df, x='emissions_y', y='region', color='region')
        stacked_bar_chart.update_layout(title=f"Emissions by Region ({', '.join(segment_value)})")
        stacked_bar_chart.update_traces(hovertemplate="Emissions: %{x}")
        stacked_bar_chart.update_xaxes(title_text='Emissions')

    # Create choropleth map
        choropleth_map = px.choropleth(filtered_df, locations='country', locationmode='country names', color='region',
                                    projection=projection_value, hover_name='region')
        choropleth_map.update_layout(title=f"Emissions by Country ({', '.join(segment_value)})",
                                 geo=dict(showframe=False, showcoastlines=True, projection_scale=1))
    return [stacked_bar_chart, choropleth_map]


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False ,use_reloader=False)


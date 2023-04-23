# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 00:29:11 2023

@author: Mathias Profft
"""

import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Load data
df = pd.read_csv('Methane_final.csv', usecols=['baseYear', 'region', 'country', 'segment', 'emissions'])
df = df.loc[df['baseYear'] == "2022"]
df = df.loc[df['region'] != "World"]

new_col = df['region'].copy().rename('country_r')
new_df = pd.concat([df, new_col], axis=1)
#region_df = df.groupby(['region','segment'])['emissions'].sum().reset_index()

# Create app
app = dash.Dash(__name__)

# Define options for dropdown filters
segment_options = [{'label': i, 'value': i} for i in df['segment'].unique()]

# Define layout
stacked_bar_chart_layout = dict(title=None, height=800, width=700, margin=dict(l=0, r=0, t=40, b=0))
stacked_bar_chart_trace = dict(x='emissions', y='region', color='country', barmode='stack', orientation='h', hovertemplate="Country: %{color}<br>Region: %{y}<br>Emissions: %{x}")
choropleth_map_layout = dict(title='Emissions by Country', height=800, width=950, margin=dict(l=0, r=0, t=40, b=0))
choropleth_map_trace = dict(locations='country', locationmode='country names', color='emissions', projection='orthographic', hover_name='country')

# Define options for dropdown filters
projection_options = [{'label': 'Equirectangular', 'value': 'equirectangular'},                      {'label': 'Mercator', 'value': 'mercator'},                      {'label': 'Orthographic', 'value': 'orthographic'},                      {'label': 'Natural Earth', 'value': 'natural earth'},                      {'label': 'Kavrayskiy7', 'value': 'kavrayskiy7'},                      {'label': 'Miller', 'value': 'miller'},                      {'label': 'Robinson', 'value': 'robinson'},                      {'label': 'Eckert4', 'value': 'eckert4'},                      {'label': 'Azimuthal Equal Area', 'value': 'azimuthal equal area'},                      {'label': 'Azimuthal Equidistant', 'value': 'azimuthal equidistant'},                      {'label': 'Conic Equal Area', 'value': 'conic equal area'},                      {'label': 'Conic Conformal', 'value': 'conic conformal'},                      {'label': 'Conic Equidistant', 'value': 'conic equidistant'},                      {'label': 'Gnomonic', 'value': 'gnomonic'},                      {'label': 'Stereographic', 'value': 'stereographic'},                      {'label': 'Mollweide', 'value': 'mollweide'},                      {'label': 'Hammer', 'value': 'hammer'},                      {'label': 'Transverse Mercator', 'value': 'transverse mercator'}]

# Define layout
app.layout = html.Div([
    html.H1("Emissions of different segments in 2022"),
    html.Button('Switch Data', id='switch_data_button', n_clicks=0),
    html.Div([
        html.Div([
            html.Label("Segment"),
            dcc.Dropdown(id='segment_dropdown',
                         options=segment_options,
                         value=[df['segment'].iloc[11]],
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
            dcc.Graph(id="choropleth_map", figure=dict(layout=choropleth_map_layout, data=[]))
        ], className="chart-container", style={"width": "50%"})
    ], className="chart-section", style={"display": "flex"}),
])

@app.callback(
    [Output('stacked_bar_chart', 'figure'),
     Output('choropleth_map', 'figure')],
    [Input('segment_dropdown', 'value'),
     Input('projection_dropdown', 'value'),
     Input('switch_data_button', 'n_clicks')])
def update_figures(segment_value, projection_value, n_clicks):
    global filtered_df
    global df
    global new_df
    if n_clicks % 2 == 0:
        filtered_df = df[df['segment'].isin(segment_value)]
    
        # Create stacked bar chart
        stacked_bar_chart = px.bar(filtered_df, x='emissions', y='region', color='country', barmode='stack', orientation='h')
        stacked_bar_chart.update_layout(title=f"Emissions by Region ({', '.join(segment_value)})")
        stacked_bar_chart.update_traces(hovertemplate="Emissions: %{x}")
        stacked_bar_chart.update_xaxes(title_text='Emissions (kt of CO2 equivalent)')

        # Create choropleth map
        choropleth_map = px.choropleth(filtered_df, locations='country', locationmode='country names', color='emissions',projection=projection_value, hover_name='country')
        choropleth_map.update_layout(title=f"Emissions by Country ({', '.join(segment_value)})", geo=dict(showframe=False, showcoastlines=False, projection_scale=0.5))
    
    else:
        filtered_df = new_df[new_df['segment'].isin(segment_value)]

    # Create stacked bar chart
        stacked_bar_chart = px.bar(filtered_df, x='emissions', y='region', color='region', barmode='stack', orientation='h')
        stacked_bar_chart.update_layout(title=f"Emissions by Region ({', '.join(segment_value)})")
        stacked_bar_chart.update_traces(hovertemplate="Emissions: %{x}")
        stacked_bar_chart.update_xaxes(title_text='Emissions (kt of CO2 equivalent)')

    # Create choropleth map
        choropleth_map = px.choropleth(filtered_df, locations='country', locationmode='country names', color='emissions',
                                    projection=projection_value, hover_name='region')
        choropleth_map.update_layout(title=f"Emissions by Country ({', '.join(segment_value)})",
                                 geo=dict(showframe=False, showcoastlines=False, projection_scale=0.5))
    
    return [stacked_bar_chart, choropleth_map]


# Run app
if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False)


# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 22:12:59 2023

@author: Mathias Profft
"""

import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Load data
df = pd.read_csv('Methane_final.csv')
df = df[df['baseYear'] == "2022"]
df = df[df['region'] != "World"]

# Create app
app = dash.Dash(__name__)

# Define options for dropdown filters
segment_options = [{'label': i, 'value': i} for i in df['segment'].unique()]

# Define layout
app.layout = html.Div([
    html.H1("Emissions Data"),
    html.Div([
        html.Div([
            html.Label("Segment"),
            dcc.Dropdown(id='segment_dropdown',
                         options=segment_options,
                         value=df['segment'].iloc[0],
                         clearable=False)
        ], className="filter")
    ], className="filter-container"),
    html.Div([
        html.Div([
            dcc.Graph(id="stacked_bar_chart")
        ], className="chart-container"),
        html.Div([
            dcc.Graph(id="choropleth_map")
        ], className="chart-container")
    ], className="chart-section")
])

# Define callbacks
@app.callback(
    [Output('stacked_bar_chart', 'figure'),
     Output('choropleth_map', 'figure')],
    [Input('segment_dropdown', 'value')])
def update_figures(segment_value):
    # Filter data based on dropdown selections
    filtered_df = df[(df['segment']==segment_value)]
    
    # Create stacked bar chart
    stacked_bar_chart = px.bar(filtered_df, x='region', y='emissions', color='country', barmode='stack')
    stacked_bar_chart.update_layout(title=f"Emissions by Region ({segment_value})")
    stacked_bar_chart.update_traces(hovertemplate="Country: %{x}<br>Emissions: %{y}")
    
    # Create choropleth map
    choropleth_map = px.choropleth(filtered_df, locations='country', locationmode='country names', color='emissions',
                                   projection='orthographic', hover_name='country', title='Emissions by Country')
    choropleth_map.update_layout(height=1000, width=1600)
    return stacked_bar_chart, choropleth_map

# Run app
if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False)

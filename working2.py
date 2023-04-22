# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 23:06:29 2023

@author: Mathias Profft
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 22:12:59 2023
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
    html.H1("Emissions of different segments in 2022"),
    html.Div([
        html.Div([
            html.Label("Segment"),
            dcc.Dropdown(id='segment_dropdown',
                         options=segment_options,
                         value=[df['segment'].iloc[11]],
                         multi=True)
        ], className="filter")
    ], className="filter-container"),
    html.Div([
        html.Div([
            dcc.Graph(id="stacked_bar_chart")
        ], className="chart-container", style={"width": "50%"}),
        html.Div([
            dcc.Graph(id="choropleth_map")
        ], className="chart-container", style={"width": "50%"})
    ], className="chart-section", style={"display": "flex"}),
])

# Define callbacks
@app.callback(
    [Output('stacked_bar_chart', 'figure'),
     Output('choropleth_map', 'figure')],
    [Input('segment_dropdown', 'value')])
def update_figures(segment_value):
    # Filter data based on dropdown selections
    filtered_df = df[df['segment'].isin(segment_value)]
    
    # Create stacked bar chart
    stacked_bar_chart = px.bar(filtered_df, x='emissions', y='region', color='country', barmode='stack', orientation='h')
    stacked_bar_chart.update_layout(title=f"Emissions by Region ({', '.join(segment_value)})")
    stacked_bar_chart.update_traces(hovertemplate="Emissions: %{x}")
    stacked_bar_chart.update_layout(height=800, width=700)
    stacked_bar_chart.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    
    # Create choropleth map
    choropleth_map = px.choropleth(filtered_df, locations='country', locationmode='country names', color='emissions',
                                   projection='orthographic', hover_name='country', title='Emissions by Country')
    choropleth_map.update_layout(height=800, width=950)
    choropleth_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    #choropleth_map.update_geos(bgcolor='blue')
    return stacked_bar_chart, choropleth_map

# Run app
if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False)
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 14:32:13 2023
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('Methane_final.csv')

# Drop rows where the country is "world"
df = df.drop(df[df['country'] == 'World'].index)

# Group the remaining rows by country and sum the values
df_grouped = df.groupby('country').sum().reset_index()



















# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Choropleth Map'),
    dcc.Graph(
        id='choropleth-map',
        figure=px.choropleth(df_grouped, locations='country',locationmode='country names', color='emissions', hover_name='country')
        )
]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

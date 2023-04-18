# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 14:13:04 2023

@author: Dev_Env
"""

import pandas as pd
import plotly.io as pio
pio.renderers.default='browser'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('Methane_final.csv')

# View the first 5 rows of the DataFrame to make sure it was imported correctly
print(df.head())


import plotly.express as px

# Create a scatter plot
fig = px.scatter(df, x='region', y='emissions')

# Show the plot
fig.show()

df_grouped = df.groupby('country').sum().reset_index()
# Drop rows where the country is "world"
df_grouped = df_grouped.drop(df_grouped[df_grouped['country'] == 'World'].index)

fig = px.choropleth(df_grouped, locations='country',locationmode='country names', color='emissions', hover_name='country')
fig.show()

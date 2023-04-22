# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 13:06:30 2023

@author: Dev_Env
"""
import plotly.io as pio
pio.renderers.default = "browser"
import pandas as pd
import plotly.express as px
# Read the CSV file into a pandas DataFrame
df = pd.read_csv('Methane_final.csv')

# Drop rows where the country is "world"
df = df.drop(df[df['country'] == 'World'].index)

# Group the remaining rows by country and sum the values
df_grouped = df.groupby(['country','region','type']).sum().reset_index()


fig = px.scatter(df_grouped, x="emissions", y="type",
	         size="emissions", color="region",
                 hover_name="country", log_x=True, size_max=60)
fig.show()

df.head

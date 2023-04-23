# Emission_project
Global Emission visual project

This code is a Python script that uses the Plotly and Dash libraries to create interactive visualizations of methane emissions data. The script reads in a CSV file containing emissions data for various countries and regions, and creates two different types of visualizations: a stacked bar chart that shows emissions by region and country, and a choropleth map that shows emissions by country.

The script also includes dropdown filters that allow the user to select which segment(s) of the emissions data they want to view, as well as which projection to use for the choropleth map. The filters are implemented using Dash's Input and Output objects, which allow the script to update the visualizations in real-time based on the user's selections.

The stacked bar chart is created using Plotly's px.bar function, which takes the emissions data and uses it to create a horizontal bar chart where each bar represents a region and is divided into segments representing the emissions from each country. The choropleth map is created using Plotly's px.choropleth function, which takes the emissions data and maps it onto a world map using colors to represent the magnitude of emissions from each country.

The code also includes various layout and formatting options for the visualizations, such as title and margin settings, and hovertemplate strings that define what information is displayed when the user hovers over different parts of the visualizations.

Overall, this code provides a powerful tool for exploring and visualizing methane emissions data, and could be useful for researchers, policymakers, and anyone else interested in tracking and analyzing global emissions trends.
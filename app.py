


import plotly.express as px
import pandas as pd
import seaborn as sn
import matplotlib as plt
import plotly.graph_objects as go




import dash

from dash import Dash, html, dcc
import dash_table
from dash.dependencies import Input, Output

import plotly.express as px


import dash_bootstrap_components as dbc 


# Importing DF

df = pd.read_csv('weather_df.csv')








df['country'].unique()


# Select the countries you want to include in the choropleth map
selected_countries = ['Germany', 'France', 'Australia', 'Indonesia', 'Mexique', 'Brazil',
       'South Africa', 'United Arab Emirates', 'Thailand',
       'United States of America', 'Spain', 'Marokko', 'Cambodia',
       'Mauritius', 'Croatia', 'Peru', 'Oman', 'Sri Lanka', 'Kenya',
       'Portugal']  # Example countries

# Filter the DataFrame for the selected countries
filtered_df = df[df['country'].isin(selected_countries)]

# Create the animated choropleth map
fig_choropleth = px.choropleth(
    data_frame=filtered_df,
    locations="country",
    locationmode='country names',  # Use the 'country' column directly
    color="avgtemp_c",  # You can choose maxtemp_c, mintemp_c, or avgtemp_c
    hover_name="country",
    projection='natural earth',
    animation_frame="date",
    title="Temperature Variation Over Time",
    color_continuous_scale=px.colors.sequential.YlOrRd,
    labels={'avgtemp_c': 'Average Temperature (°C)'}
)

fig_choropleth.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="white")

fig_choropleth.show()




graph1 = dcc.Graph(figure=fig_choropleth)

#Create scattermap of all the locations in the data.**

# Create a scatter map of all locations with color based on average temperature
fig_scatter_map = px.scatter_geo(
    data_frame=df,
    lat='lat',  # Latitude data
    lon='lon',  # Longitude data
    text='city',  # Text to display on hover (city names)
    color='avgtemp_c',  # Color based on average temperature
    color_continuous_scale=px.colors.sequential.YlOrRd,  # Choose your color scale
    title='Weather Stations / Cities with Average Temperature',
    projection='orthographic',  # You can change the projection as needed
)

fig_scatter_map.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="white")

fig_scatter_map.show()


#Create warming stripes for one station over time to inspect warming over time.**


# specific city
city_name = "Berlin"

# Filter data for the specific city
city_data = df[df['city'] == city_name]

# Sort the data by date for a chronological order
city_data['date'] = pd.to_datetime(city_data['date'])
city_data = city_data.sort_values(by='date')

# Create warming stripes plot
fig_warming_stripes = px.bar(
    city_data,
    x='date',
    y='avgtemp_c',
    labels={'avgtemp_c': 'Average Temperature (°C)'},
    title=f'Warming Stripes for {city_name}',
    template="plotly_white",  # Use a white template for clearer visualization
    color='avgtemp_c',
    color_continuous_scale="RdYlBu_r",  
)
# Customize the layout (optional)
fig_warming_stripes.update_layout(
    xaxis_title='Year',
    yaxis_title='Average Temperature (°C)',
    showlegend=False,
)
fig_warming_stripes.update_xaxes(
    showline=True, showgrid=False
)
fig_warming_stripes.show()




graph2 = dcc.Graph(figure=fig_warming_stripes)

selected_country = ['Germany']  

# Filter the DataFrame for the selected country
df_germany = df[df['country'].isin(selected_country)]

df_germany

#Average daily temperature over time**




fig_avg_temp = px.line(df_germany, x='date', y='avgtemp_c', title='Average daily temperature over time')
fig_avg_temp.update_xaxes(title='Date')
fig_avg_temp.update_yaxes(title='Average daily temperature (°C)')
fig_avg_temp.show()


#Distribution of maximum temperatures (histogram):**

fig_max_temp = px.histogram(df_germany, x='maxtemp_c', nbins=15, title='Distribution of maximum temperatures')
fig_max_temp.update_xaxes(title='Maximum temperature (°C)')
fig_max_temp.update_yaxes(title='Quantity')
fig_max_temp.show()


#Average temperature by day of the month (boxplot):**

# Define the correct order of months
correct_month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Create a box plot for the average temperature by month
fig_avg_temp_month = px.box(
    df_germany, x='Month', y='avgtemp_c',
    title='Average Temperature by Month',
    category_orders={"Month": correct_month_order}
)
fig_avg_temp_month.update_xaxes(title='Month')
fig_avg_temp_month.update_yaxes(title='Average Temperature (°C)')
fig_avg_temp_month.show()

graph3 = dcc.Graph(figure=fig_avg_temp_month)



# Group the data by month and calculate the maximum temperature for each month
monthly_max_temp = df.groupby('Month')['maxtemp_c'].max().reset_index()

# Create a bar graph for maximum temperature by month
fig_max_temp_monthly = px.bar(
    monthly_max_temp,
    x='Month',
    y='maxtemp_c',
    title='Maximum Temperature by Month',
    labels={'maxtemp_c': 'Max Temperature (°C)'},
)

fig_max_temp_monthly.show()




#Correlation Heatmap:**

import plotly.express as px

# Create the correlation matrix
correlation_matrix = df_germany.corr()

# Change the color scale for the heatmap
fig_corr_heatmap = px.imshow(
    correlation_matrix, 
    zmin=-1, 
    zmax=1, 
    title='Correlation Heatmap',
    color_continuous_scale='RdYlGn'  # Change to a different color scale (Red-Yellow-Green)
)

fig_corr_heatmap.show()



graph4 = dcc.Graph(figure=fig_corr_heatmap)





# Create a dash app

import dash
from dash import html, dcc
from dash import Dash, html, dcc
import dash_table
from dash.dependencies import Input, Output

import plotly.express as px


import dash_bootstrap_components as dbc 




selected_country = ['Germany']  

# Filter the DataFrame for the selected country
df_germany = df[df['country'].isin(selected_country)]



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

# Sample DataTable
d_table = dash_table.DataTable(df_germany.to_dict('records'),
                                  [{"name": i, "id": i} for i in df_germany.columns],
                               style_data={'color': 'black','backgroundColor': 'white'},
                              style_header={
                                  'backgroundColor': 'rgb(210, 180, 210)',
                                  'color': 'black','fontWeight': 'bold'
    })







app.layout = html.Div([html.H1('Temperature Analysis Dashboard', style={'textAlign': 'center', 'color': 'coral'}), 
                       html.H2('Welcome', style ={'paddingLeft': '30px'}),
                       html.H3('These are the Graphs'),
                       html.Div([html.Div('Germany', 
                                          style={'backgroundColor': 'coral', 'color': 'white', 'width': "Germany"}),d_table, graph1])

                    
])

if __name__ == '__main__':
     app.run_server(debug=True, port=8052)
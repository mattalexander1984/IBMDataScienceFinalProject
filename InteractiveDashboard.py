#Which site has the largest successful launches?
#Which site has the highest launch success rate?
#Which payload range(s) has the highest launch success rate?
#Which payload range(s) has the lowest launch success rate?
#Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
#launch success rate?

import dash_bootstrap_components as dbc

import dash
import pandas as pd
import requests

requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
spacex_df = pd.read_csv("spacex_launch_dash.csv")
requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py")

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
             html.Div(
                dcc.Dropdown(id ='site-dropdown',
                options = [{'label': 'All Sites', 'value': 'ALL'},
                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                placeholder= 'Select a Launch Site Here',
                searchable = True,
                value = 'All')
                        )]

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
        names='pie chart names',
        title='title')
        return fig
    else:
        fig = px.pie(filtered_df(' ')  , value='class')
             )
#### Need to pull data from correct column, possibly label Success vs Failure
    html.Div(
        dcc.RangeSlider(id='Payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       100: '100'},
                value=[min_payload, max_payload])
    )

@app.callback(
[Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")],
Output(component_id='success-payload-scatter-chart', component_property='figure')
)

def get_scatter_plot(entered_site, payload):
    filtered_df = spacex_df
    if entered_site == 'All':
        fig = px.scatter(x = 'Payload Mass (kg)', y = 'class')
        names = 'Scatter Plot Names'
        title = "Title"
        color = "Booster Version Category"
    else:
        dfsdf
        something

        color = "Booster Version Category"



#A If-Else statement to check if ALL sites were selected or just a specific launch site was selected
#If ALL sites are selected, render a scatter plot to display all values for variable Payload Mass (kg) and variable class.
#In addition, the point color needs to be set to the booster version i.e., color="Booster Version Category"
#If a specific launch site is selected, you need to filter the spacex_df first, and render a scatter chart to show
#values Payload Mass (kg) and class for the selected site, and color-label the point using Boosster Version Category likewise.
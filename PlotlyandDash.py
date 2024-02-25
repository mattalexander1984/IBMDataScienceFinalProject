import requests

requests.get("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-DV0101EN-Coursera/labs/v4/Final_Project/DV0101EN-Final_Assign_Part_2_Questions.py")


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

app = dash.Dash(__name__)


app.title = "Automobile Statistics Dashboard"

dcc.Dropdown(id='Dropdown Statistics',
                   options=[
                           {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                           {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                           ],
                  placeholder= 'Select a Report Type',
                  value = "Select Statistics"
             )

year_list = [i for i in range(1980, 2024, 1)]

dcc.Dropdown(id='select-year',
             options=[{'label': i, 'value': i} for i in year_list],
             placeholder='Year',
             )

app.layout = html.Div([
    # TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard"),

    html.Div([  # TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics'
        )
    ]),
    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        value='Select-year'
    )),

    html.Div([#TASK 2.3: Add a division for output display
        html.Div(id='output-container',
                 className='chart-grid',
                 style={'display':'flex'}),])
])

#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
###1st callback
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics':
        return False
    else:
        return True

###2nd callback

# Callback for plotting
        @app.callback(
            Output(component_id='output-container', component_property='children'),
            [Input(component_id='dropdown-statistics', component_property='value'),
             Input(component_id='select-year', component_property='value')])
        def update_output_container(selected_statistics, input_year):
            if selected_statistics == 'Recession Period Statistics':
                recession_data = data[data['Recession'] == 1]

# TASK 2.5: Create and display graphs for Recession Report Statistics

# Plot 1 Automobile sales fluctuate over Recession Period (year wise)
            yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
            R_chart1 = dcc.Graph(figure=px.line(yearly_rec,
                                                x='Year',
                                                y='Automobile_Sales',
                                                title="Average Automobile Sales fluctuation over Recession Period"))

# Plot 2 Calculate the average number of vehicles sold by vehicle type
            average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
            R_chart2 = dcc.Graph(figure=px.line(average_sales,
                                                x='Vehicle_Type',
                                                y='Automobile_Sales',
                                                title='Average Automobile Sales for each Vehicle Type in the Recession Period'))

# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
            exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
            R_chart3 = dcc.Graph(figure=px.pie(exp_rec,
                                               values='Advertising_Expenditure',
                                               names='Vehicle_Type',
                                               title='Total Expenditure for each Vehicle Type during the Recession'))

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
            unemp_data = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])[
                'Automobile_Sales'].mean().reset_index()
            R_chart4 = dcc.Graph(
                figure=px.bar(
                    unemp_data,
                    x='unemployment_rate',
                    y='Automobile_Sales',
                    color='Vehicle_Type',
                    labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                    title="Effect of Unemployment Rate on Sales of various Vehicle Types")
            )

            return [
                html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)],
                         style={'display': 'flex'}),
                html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)],
                         style={'display': 'flex'})
            ]

# TASK 2.6: Create and display graphs for Yearly Report Statistics
    elif (input_year and selected_statistics == 'Yearly Statistics'):
    yearly_data = data[data['Year'] == input_year]

# Plot 1 Yearly Automobile sales using line chart for the whole period.
    yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
    Y_chart1 = dcc.Graph(figure=px.line(yas,
                                        x='Year',
                                        y='Automobile_Sales',
                                        title="Average Automobile Sales fluctuation over Recession Period (Year Wise)"))

# Plot 2 Total Monthly Automobile sales using line chart
    total_monthly_sales = data.groupby('Month')['Automobile_Sales'].mean().reset_index()
    Y_chart2 = dcc.Graph(figure=px.line(total_monthly_sales,
                                        x='Month',
                                        y='Automobile_Sales',
                                        title="Total Monthly Automobile Sales"))

# Plot 3 Plot bar chart for average number of vehicles sold during that given year
    avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()
    Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata,
                                       x='Vehicle_Type',
                                       y='Automobile_Sales',
                                       title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

# Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
    exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
    Y_chart4 = dcc.Graph(figure=px.pie(exp_data,
                                       names='Vehicle_Type',
                                       values='Advertising_Expenditure',
                                       title='Total Advertisement Expenditure by Vehicle Type in the year {}'.format(
                                           input_year)))

    return [
        html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)],
                 style={'display': 'flex'}),
        html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)],
                 style={'display': 'flex'})
    ]

    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
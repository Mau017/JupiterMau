# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div([
                                    dcc.Dropdown(
                                        id='site-dropdown',
                                        options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                        ],
                                        value='ALL',  # Default value
                                        placeholder="Select a Launch Site",
                                        style={'width': '50%'}
                                    )
                                ]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=100,
                                    marks={0: '0', 10000: '10000'},
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(launch_site):
    if launch_site == 'ALL':
        filtered_df = spacex_df
        fig = px.pie(filtered_df, names='class', title='Total Successful Launches for All Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == launch_site]
        fig = px.pie(filtered_df, names='class', title=f'Success vs Failed Launches for {launch_site}')
    return fig

# TASK 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(launch_site, payload_range):
    min_payload_slider, max_payload_slider = payload_range
    if launch_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload_slider) & 
                                (spacex_df['Payload Mass (kg)'] <= max_payload_slider)]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         title='Payload vs Launch Success for All Sites')
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == launch_site) & 
                                (spacex_df['Payload Mass (kg)'] >= min_payload_slider) & 
                                (spacex_df['Payload Mass (kg)'] <= max_payload_slider)]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         title=f'Payload vs Launch Success for {launch_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

options_list = [{'label': 'All Sites', 'value': 'ALL'}]
sites = spacex_df['Launch Site'].unique().tolist()

for site in sites:
    new_option = [{'label':site,'value':site}]
    options_list = options_list + new_option

print (options_list)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=options_list,
                                value='ALL',
                                placeholder="place holder here",
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output




@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def get_graph(launch_site):    
    print ("Graph input:", launch_site)
    if (launch_site != 'ALL'):
        results =  (spacex_df[spacex_df['Launch Site']==launch_site]).groupby('Mission Outcome').size().reset_index(name='Cnt')
    else:
        results =  spacex_df.groupby('Mission Outcome').size().reset_index(name='Cnt')
    print(results)
    print (type(results))
    fig = px.pie(results,values='Cnt',names='Mission Outcome')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
© 2021 GitHub, Inc.
Terms
Privacy
Security
Status
Docs

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

years = ['2019-2020']
all_options = {
    'Team': ['Warriors'],
    'Player': ['Stephen Curry']
}

ppg_data = {
    'Stephen Curry': 29.8,
    'Warriors': 13.4,
    'NBA': 9.7
}

player_team_map = {
    'Stephen Curry': 'Warriors',
    'Warriors': 'NBA'
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Welcome to NBA Stats'),
    
    html.Div([
            dcc.Dropdown(
                id='years-dropdown',
                options=[{'label': i, 'value': i} for i in years],
                value='2019-2020',
                placeholder='Select a Year'
            )
    ]
    ),
    
    html.Div([
            dcc.Dropdown(
                id='groups-dropdown',
                options=[{'label': i, 'value': i} for i in all_options.keys()],
                value='Team',
                placeholder='Select a Group'
            )
    ]
    ),

        html.Div([
            dcc.Dropdown(id='people-dropdown'),
    ]
    ),

    html.Div(children='''
        NBA Stats : A web applications for viewing NBA Statistics
    '''),

    dcc.Graph(id='ppg-graph')

    # dcc.Graph(
    #     id='example-graph',
    #     figure={
    #         'data': [
    #             {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
    #             {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
    #         ],
    #         'layout': {
    #             'title': 'NBA Statistics Data Visualization'
    #         }
    #     }
    # )
])

#  Callback updates options for people-dropdown based on group selected
@app.callback(
    Output('people-dropdown', 'options'),
    [Input('groups-dropdown', 'value')])
def set_people_options(group):
    return [{'label': i, 'value': i} for i in all_options[group]]

#  Callback updates value for people-dropdown based on player/team selected
@app.callback(
    Output('people-dropdown', 'value'),
    [Input('people-dropdown', 'options')])
def set_people_value(available_options):
    return available_options[0]['value']

#  Callback updates graph based on player/team selected
@app.callback(
    Output('ppg-graph','figure'),
    [Input('groups-dropdown','value'),
     Input('people-dropdown','value')])
def update_ppg_figure(group_selected, player_team_selected):
    
    if(group_selected == 'Team'):
        x1_data = player_team_selected  # Team Name
        y1_data = ppg_data[player_team_selected] # Team Avg PPG
        x2_data = player_team_map[player_team_selected]  # NBA Name
        y2_data =  ppg_data[player_team_map[player_team_selected]]  # NBA Avg PPG
        name1 =  player_team_selected  # Team Name
        name2 =  player_team_map[player_team_selected]  # NBA Name
    else: # group_selected == 'Player
        x1_data =  player_team_selected  # Player Name
        y1_data =  ppg_data[player_team_selected]# Player Avg PPG
        x2_data =  player_team_map[player_team_selected]# Team Name
        y2_data =  ppg_data[player_team_map[player_team_selected]]# Team Avg PPG
        name1 =  player_team_selected# Player Name
        name2 =  player_team_map[player_team_selected]# Team Name
    return{
            'data': [
                {'x': [x1_data], 'y': [y1_data], 'type': 'bar', 'name': name1},
                {'x': [x2_data], 'y': [y2_data], 'type': 'bar', 'name': name2},
            ],
            'layout': {
                'title': 'Points Per Game Data Visualization'
            }
        }

if __name__ == '__main__':
    app.run_server(debug=True)
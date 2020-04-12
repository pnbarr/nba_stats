# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

years = ['2015-2016']
all_options = {
    'Team': ['Warriors', 'Cavaliers'],
    'Player': ['Stephen Curry', 'Klay Thompson', 'Draymond Green', 'Kyrie Irving', 'Kevin Love','LeBron James']
}

ppg_data = {
    'Stephen Curry': 30.1,
    'Klay Thompson': 22.1,
    'Draymond Green': 14,
    'Kyrie Irving': 19.6,
    'Kevin Love': 16.0,
    'LeBron James': 25.3,
    'Cavaliers': 12.7,
    'Warriors': 13.4,
    'NBA': 9.7
}

player_team_map = {
    'Stephen Curry': 'Warriors',
    'Klay Thompson': 'Warriors',
    'Draymond Green': 'Warriors',
    'Kevin Love': 'Cavaliers',
    'LeBron James': 'Cavaliers',
    'Kyrie Irving': 'Cavaliers',
    'Warriors': 'NBA',
    'Cavaliers': 'NBA',

}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Welcome to NBA Stats'),
    
    html.Div([
            dcc.Dropdown(
                id='years-dropdown',
                options=[{'label': i, 'value': i} for i in years],
                value='2015-2016',
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
    return{
            'data': [
                {'x': [player_team_selected], 'y': [ppg_data[player_team_selected]], 'type': 'bar', 'name': player_team_selected},
                {'x': [player_team_map[player_team_selected]], 'y': [ppg_data[player_team_map[player_team_selected]]], 'type': 'bar', 'name': player_team_map[player_team_selected]},
            ],
            'layout': {
                'title': 'Average Points Per Game Data Visualization'
            }
        }

if __name__ == '__main__':
    app.run_server(debug=True)
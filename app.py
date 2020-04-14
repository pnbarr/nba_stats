# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonallplayers, leaguegamefinder, commonplayerinfo, playercareerstats, teamyearbyyearstats
from nba_api.stats.library.parameters import Season
import plotly.graph_objects as go
import plotly.express as px 
import pandas as pd 

# ==================================== SandBox Area ==================================================== #
nba_teams = teams.get_teams()  # nba_teams is a list of dictionaries
#print('First NBA team data example.')
#print(nba_teams[0])  
# KEYS
# 'id'
# 'full_name'
# 'abbreviation'
# 'nickname'
# 'city'
# 'state'
# 'year_founded'

nba_players = players.get_players()  # nba_players is a list of dictionaries
#print('Frist NBA player data example.')
#print(nba_players[0])
# KEYS
# 'id'
# 'full_name'
# 'first_name'
# 'last_name'
# 'is_active'

team_example = teamyearbyyearstats.TeamYearByYearStats(team_id=nba_teams[0]['id'])
team_example_df = team_example.get_data_frames()[0]

# Function should take a year season as an input and return list of players who played that year
player_example = playercareerstats.PlayerCareerStats(player_id=nba_players[0]['id'])
player_example_df = player_example.get_data_frames()[0]

# ======================================================================================================= #
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

group_options = ['Team', 'Player']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Welcome to NBA Stats'),
    
    html.Div([
            dcc.Dropdown(
                id='groups-dropdown',
                options=[{'label': i, 'value': i} for i in group_options],
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

    dcc.Graph(id='stats-graph')
])

#  Callback updates options for people-dropdown based on group selected
@app.callback(
    Output('people-dropdown', 'options'),
    [Input('groups-dropdown', 'value')])
def set_people_options(group):
    if group == 'Team':
        nba_team_list =[]
        for team in nba_teams:
            nba_team_list.append(team['full_name'])
        return [{'label': i, 'value': i} for i in nba_team_list]
    else:
        nba_player_list =[]
        for player in nba_players:
            nba_player_list.append(player['full_name'])
        return [{'label': i, 'value': i} for i in nba_player_list]

#  Callback updates graph based on player/team selected
@app.callback(
    Output('stats-graph','figure'),
    [Input('groups-dropdown','value'),
     Input('people-dropdown','value')])
def update_statsgraph_figure(group_selected, player_team_selected):
    selected_year = '2018-19'  # TODO : Make this a slider input
    if group_selected == 'Team':
        team_info = [team for team in nba_teams
                     if team['full_name'] == player_team_selected][0]
        team_id = team_info['id']
        team_yby_data = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id)
        team_yby_df = team_yby_data.get_data_frames()[0]
        selected_year_data = team_yby_df.loc[team_yby_df['YEAR'] == selected_year]
        filtered_team_yby_df = selected_year_data[['GP','WINS','LOSSES','CONF_RANK']]
        labels = ['WINS','LOSSES']
        values = [filtered_team_yby_df.iloc[0]['WINS'], filtered_team_yby_df.iloc[0]['LOSSES']]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        return fig

    else:  # Put player logic here
        player_info = [player for player in nba_players
                     if player['full_name'] == player_team_selected][0]
        player_id = player_info['id']
        player_career_data = playercareerstats.PlayerCareerStats(player_id=player_id)
        player_career_df = player_career_data.get_data_frames()[0]
        selected_year_data = player_career_df.iloc[0]  #  TODO : Currently grabbing first year player played
                                                       #  TODO : Include logic to average player's stats if 
                                                       #         played for more than one team in a given
                                                       #         season, need to normalize w/ respect to GP 
        filtered_player_df = selected_year_data[['REB','AST','STL','BLK','TOV','PTS']]
        return{
                'data': [
                    {'x': ['REB','AST','STL','BLK','TOV','PTS'], 'y': [filtered_player_df.loc['REB'],filtered_player_df.loc['AST'],
                                                                       filtered_player_df.loc['STL'],filtered_player_df.loc['BLK'],
                                                                       filtered_player_df.loc['TOV'],filtered_player_df.loc['PTS']],
                                                                        'type': 'bar', 'name': player_team_selected},
                ],
                'layout': {
                    'title': 'Player Performance Statistics'
                }
            }


#  Callback updates value for people-dropdown based on player/team selected
@app.callback(
    Output('people-dropdown', 'value'),
    [Input('people-dropdown', 'options')])
def set_people_value(available_options):
    return available_options[0]['value']

if __name__ == '__main__':
    app.run_server(debug=True)
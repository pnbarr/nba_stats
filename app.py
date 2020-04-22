# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonallplayers, leaguegamefinder, commonplayerinfo, playercareerstats, teamyearbyyearstats, shotchartdetail
from nba_api.stats.endpoints import shotchartlineupdetail
from nba_api.stats.library.parameters import Season
import plotly.graph_objects as go
import plotly.express as px 
import pandas as pd 
import numpy as np

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

# Shot Chart Detail
# player_shot_data = shotchartdetail.ShotChartDetail(context_measure_simple = 'FGA', team_id=0, player_id=2544, season_nullable='2013-14', season_type_all_star='Regular Season')
# player_shot_df = player_shot_data.get_data_frames()[0]
# data_columns = ['SHOT_TYPE','SHOT_ZONE_AREA','SHOT_ZONE_RANGE','SHOT_DISTANCE','LOC_X','LOC_Y','SHOT_ATTEMPTED_FLAG','SHOT_MADE_FLAG']
# filtered_player_shot_df = player_shot_df[data_columns]
# print(filtered_player_shot_df)
# ======================================================================================================= #

def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id='tabs-group',
                value="Team",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Team-tab",
                        label="Team Statistics",
                        value="Team",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Player-tab",
                        label="Player Statistics",
                        value="Player",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )

def build_team_tab():
    return [
        html.Div([
        dcc.Dropdown(id='people-dropdown'),
    ]
    ),
    ]

def build_player_tab():
    return


# ======================================================================================================= #
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

group_options = ['Team', 'Player']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Welcome to NBA Stats', style={
        'textAlign':'center'
    }),

    html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),

    html.Div([
        dcc.Dropdown(id='people-dropdown'),
    ]
    ),

    html.Div(children='''
        NBA Stats : A web applications for viewing NBA Statistics
    ''', style={
        'textAlign':'center'
    }),

    html.Div(id='tabs-content')
])

#  Callback updates options for people-dropdown based on group selected
@app.callback(
    Output('people-dropdown', 'options'),
    [Input('tabs-group', 'value')])
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
    Output('tabs-content','children'),
    [Input('tabs-group','value'),
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
        data_columns = ['WINS','LOSSES','CONF_RANK','REB','AST','STL','TOV','BLK','PTS']
        filtered_team_yby_df = selected_year_data[data_columns]
        #  Pie chart for display record data
        record_pie_labels = ['WINS','LOSSES']
        record_pie_values = [filtered_team_yby_df.iloc[0]['WINS'], filtered_team_yby_df.iloc[0]['LOSSES']]
        record_pie = go.Figure(data=[go.Pie(labels=record_pie_labels, values=record_pie_values)])
        colors=['cyan','orange']
        record_pie.update_traces(marker=dict(colors=colors))
        #  Bar graph for displaying basic data 
        basic_bar_labels = ['REB','AST','STL','TOV','BLK','PTS']
        basic_bar_values = [filtered_team_yby_df.iloc[0]['REB'], filtered_team_yby_df.iloc[0]['AST'],
                             filtered_team_yby_df.iloc[0]['STL'], filtered_team_yby_df.iloc[0]['TOV'],
                             filtered_team_yby_df.iloc[0]['BLK'], filtered_team_yby_df.iloc[0]['PTS']]
        basic_bar = go.Figure(data=[go.Bar(x=basic_bar_labels, y=basic_bar_values)])
        return [
            html.Div([
                dcc.Graph(figure=record_pie),
            ]
            ),
            html.Div(children='''
                                Standard Team Data
                               ''',
                     style={
                         'textAlign': 'center'
                     }),
            dcc.Graph(figure=basic_bar)
        ]

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
        season = selected_year_data['SEASON_ID']
        filtered_player_df = selected_year_data[['REB','AST','STL','BLK','TOV','PTS','FG_PCT','FG3_PCT','FT_PCT']]
        #  Bar graph for displaying basic data 
        basic_stats_x = ['REB','AST','STL','BLK','TOV','PTS']
        basic_stats_y = [filtered_player_df.loc['REB'],filtered_player_df.loc['AST'],
             filtered_player_df.loc['STL'],filtered_player_df.loc['BLK'],
             filtered_player_df.loc['TOV'],filtered_player_df.loc['PTS']]
        basic_stats_bar = go.Figure(data=[go.Bar(x=basic_stats_x,y=basic_stats_y,name=player_team_selected)])
        #  Bar graph for displaying percentages
        perc_stats_x = ['FG_PCT','FG3_PCT','FT_PCT']
        perc_stats_y = np.multiply(100, [filtered_player_df.loc['FG_PCT'],filtered_player_df.loc['FG3_PCT'],
             filtered_player_df.loc['FT_PCT']])
        perc_stats_bar = go.Figure(data=[go.Bar(x=perc_stats_x,y=perc_stats_y,name=player_team_selected)])

        # Player shot chart detail
        player_shot_data = shotchartdetail.ShotChartDetail(context_measure_simple = 'FGA', team_id=0, player_id=player_id, season_nullable=season, season_type_all_star='Regular Season')
        player_shot_df = player_shot_data.get_data_frames()[0]
        data_columns = ['SHOT_TYPE','SHOT_ZONE_AREA','SHOT_ZONE_RANGE','SHOT_DISTANCE','LOC_X','LOC_Y','SHOT_ATTEMPTED_FLAG','SHOT_MADE_FLAG']
        filtered_player_shot_df = player_shot_df[data_columns]
        xlocs = filtered_player_shot_df['LOC_X'].tolist()
        ylocs = filtered_player_shot_df['LOC_Y'].tolist()
        player_shot_chart = go.Figure()
        player_shot_chart.add_trace(go.Scatter(
            x=xlocs, y=ylocs, mode='markers', name='markers',
            marker=dict(
                sizemode='area', sizemin=2.5,
                line=dict(width=1, color='#333333'), symbol='hexagon',
            ),
        ))
        return [
            html.Div([
                dcc.Graph(figure=basic_stats_bar),
            ]
            ),
            html.Div(children='''
                                Player Percentage Data
                               ''',
                     style={
                         'textAlign': 'center'
                     }),
            dcc.Graph(figure=perc_stats_bar),
            html.Div(children='''
                                Player Shot Chart Data
                               ''',
                     style={
                         'textAlign': 'center'
                     }),
            dcc.Graph(figure=player_shot_chart)      
        ]


#  Callback updates value for people-dropdown based on player/team selected
@app.callback(
    Output('people-dropdown', 'value'),
    [Input('people-dropdown', 'options')])
def set_people_value(available_options):
    return available_options[0]['value']

if __name__ == '__main__':
    app.run_server(debug=True)

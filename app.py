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
league_shot_data = shotchartdetail.ShotChartDetail(context_measure_simple = 'FGA', team_id=0, player_id=0, season_nullable='2013-14', season_type_all_star='Regular Season')
league_shot_df = league_shot_data.get_data_frames()[1]
print('2013-14 League Shooting Averages')
print(league_shot_df)
data_columns = ['SHOT_TYPE','SHOT_ZONE_AREA','SHOT_ZONE_RANGE','SHOT_DISTANCE','LOC_X','LOC_Y','SHOT_ATTEMPTED_FLAG','SHOT_MADE_FLAG']
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

def draw_plotly_court(fig, fig_width=600, margins=10):        
    # From: https://community.plot.ly/t/arc-shape-with-path/7205/5
    def ellipse_arc(x_center=0.0, y_center=0.0, a=10.5, b=10.5, start_angle=0.0, end_angle=2 * np.pi, N=200, closed=False):
        t = np.linspace(start_angle, end_angle, N)
        x = x_center + a * np.cos(t)
        y = y_center + b * np.sin(t)
        path = f'M {x[0]}, {y[0]}'
        for k in range(1, len(t)):
            path += f'L{x[k]}, {y[k]}'
        if closed:
            path += ' Z'
        return path

    fig_height = fig_width * (470 + 2 * margins) / (500 + 2 * margins)
    fig.update_layout(width=fig_width, height=fig_height)

    # Set axes ranges
    fig.update_xaxes(range=[-250 - margins, 250 + margins])
    fig.update_yaxes(range=[-52.5 - margins, 417.5 + margins])

    threept_break_y = 89.47765084
    three_line_col = "#777777"
    main_line_col = "#777777"

    fig.update_layout(
        # Line Horizontal
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        shapes=[
            dict(
                type="rect", x0=-250, y0=-52.5, x1=250, y1=417.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="rect", x0=-80, y0=-52.5, x1=80, y1=137.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="rect", x0=-60, y0=-52.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="circle", x0=-60, y0=77.5, x1=60, y1=197.5, xref="x", yref="y",
                line=dict(color=main_line_col, width=1),
                # fillcolor='#dddddd',
                layer='below'
            ),
            dict(
                type="line", x0=-60, y0=137.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=1),
                layer='below'
            ),

            dict(
                type="rect", x0=-2, y0=-7.25, x1=2, y1=-12.5,
                line=dict(color="#ec7607", width=1),
                fillcolor='#ec7607',
            ),
            dict(
                type="circle", x0=-7.5, y0=-7.5, x1=7.5, y1=7.5, xref="x", yref="y",
                line=dict(color="#ec7607", width=1),
            ),
            dict(
                type="line", x0=-30, y0=-12.5, x1=30, y1=-12.5,
                line=dict(color="#ec7607", width=1),
            ),

            dict(type="path",
                 path=ellipse_arc(a=40, b=40, start_angle=0, end_angle=np.pi),
                 line=dict(color=main_line_col, width=1), layer='below'),
            dict(type="path",
                 path=ellipse_arc(a=237.5, b=237.5, start_angle=0.386283101, end_angle=np.pi - 0.386283101),
                 line=dict(color=main_line_col, width=1), layer='below'),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=220, y0=-52.5, x1=220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),

            dict(
                type="line", x0=-250, y0=227.5, x1=-220, y1=227.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=250, y0=227.5, x1=220, y1=227.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=17.5, x1=-80, y1=17.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=27.5, x1=-80, y1=27.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=57.5, x1=-80, y1=57.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=87.5, x1=-80, y1=87.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=17.5, x1=80, y1=17.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=27.5, x1=80, y1=27.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=57.5, x1=80, y1=57.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=87.5, x1=80, y1=87.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),

            dict(type="path",
                 path=ellipse_arc(y_center=417.5, a=60, b=60, start_angle=-0, end_angle=-np.pi),
                 line=dict(color=main_line_col, width=1), layer='below'),

        ]
    )
    return True

def generate_player_shotchart_averages(player_shot_chart_df):
    # Goal : Generate player's shot chart averages for each zone
    # Input : Player shot chart dataframe from shotchartdetail API endpoint
    # Output : Dataframe containing players averages for each area for a given NBA Regular season
    # For each of the 20 shooting zones, calculate the following:
    # 1) FGA
    # 2) FGM
    # 3) FG_PCT
    # 4) Frequency

    # Columns needed to calculate the above data
    data_columns = ['SHOT_ZONE_BASIC','SHOT_ZONE_AREA','SHOT_ZONE_RANGE','SHOT_ATTEMPTED_FLAG','SHOT_MADE_FLAG']
    filtered_player_shot_df = player_shot_chart_df[data_columns]
    print('Rookie Season Shot Chart Data')
    print(filtered_player_shot_df)
    second_zone = filtered_player_shot_df.loc[(filtered_player_shot_df['SHOT_ZONE_BASIC'] == 'Above the Break 3') & (filtered_player_shot_df['SHOT_ZONE_AREA'] == 'Center(C)') & (filtered_player_shot_df['SHOT_ZONE_RANGE'] == '24+ ft.')]
    print('2nd shot zone')
    print(second_zone)
    second_zone_FGM = second_zone.SHOT_MADE_FLAG.sum()
    second_zone_FGA = second_zone.SHOT_ATTEMPTED_FLAG.sum()
    second_zone_AVG = 0
    if second_zone_FGA != 0:
        second_zone_AVG = second_zone_FGM/second_zone_FGA
    print("FGM = {}. FGA = {}. FG% = {}.".format(second_zone_FGM, second_zone_FGA, second_zone_AVG))

    return True



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
        #print(player_shot_df)
        generate_player_shotchart_averages(player_shot_df)
        data_columns = ['SHOT_TYPE','SHOT_ZONE_AREA','SHOT_ZONE_RANGE','SHOT_DISTANCE','LOC_X','LOC_Y','SHOT_ATTEMPTED_FLAG','SHOT_MADE_FLAG']
        filtered_player_shot_df = player_shot_df[data_columns]
        #print(filtered_player_shot_df)
        xlocs = filtered_player_shot_df['LOC_X'].tolist()
        ylocs = filtered_player_shot_df['LOC_Y'].tolist()
        player_shot_chart = go.Figure()
        draw_plotly_court(player_shot_chart)
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

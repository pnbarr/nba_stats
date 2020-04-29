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
import time

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
# league_shot_data = shotchartdetail.ShotChartDetail(context_measure_simple = 'FG_PCT', team_id=0, player_id=0, season_nullable='1997-98', season_type_all_star='Regular Season')
# league_shot_df = league_shot_data.get_data_frames()[1]
# print('2013-14 League Shooting Averages')
# print(league_shot_df)
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

def generate_player_shotchart_averages(player_id, season):
    # Goal : Generate player's shot chart averages for each zone
    # Input : Player shot chart dataframe from shotchartdetail API endpoint
    # Output : Dataframe containing players averages for each area for a given NBA Regular season

    # Columns of interest
    shot_zone_basic = 'SHOT_ZONE_BASIC'
    shot_zone_area = 'SHOT_ZONE_AREA'
    shot_zone_range = 'SHOT_ZONE_RANGE'
    shot_attempted_flag = 'SHOT_ATTEMPTED_FLAG'
    shot_made_flag = 'SHOT_MADE_FLAG'
    shot_distance = 'SHOT_DISTANCE'
    fgm = 'FGM'
    fga = 'FGA'
    rel_fgp = 'RELATIVE_FG_PCT'
    player_fgp = 'PLAYER_FG_PCT'
    league_fgp = 'LEAGUE_FG_PCT'
    fgf = 'FREQ'

    # Shot Zone Basic strings
    basic_above_the_break_3 = 'Above the Break 3'
    basic_backcourt = 'Backcourt'
    basic_non_RA = 'In The Paint (Non-RA)'
    basic_left_corner_3 = 'Left Corner 3'
    basic_mid_range = 'Mid-Range'
    basic_restricted_area = 'Restricted Area'
    basic_right_corner_3 ='Right Corner 3'
    
    # Shot Zone Area strings
    area_back_court = 'Back Court(BC)'
    area_center = 'Center(C)'
    area_left_side_center = 'Left Side Center(LC)'
    area_right_side_center = 'Right Side Center(RC)'
    area_left_side = 'Left Side(L)'
    area_right_side ='Right Side(R)'

    # Shot Zone Range strings
    range_back_court = 'Back Court Shot'
    range_24 = '24+ ft.'
    range_8_to_16 = '8-16 ft.'
    range_0_to_8 = 'Less Than 8 ft.'
    range_16_to_24 = '16-24 ft.'

    # Shot Zone Basic List : Basic shot zone data for each of the 20 shot zones
    shot_zone_basic_list = [basic_above_the_break_3, basic_above_the_break_3, basic_above_the_break_3,
                            basic_above_the_break_3, basic_backcourt, basic_non_RA, basic_non_RA,
                            basic_non_RA, basic_non_RA, basic_left_corner_3, basic_mid_range,
                            basic_mid_range, basic_mid_range, basic_mid_range, basic_mid_range,
                            basic_mid_range, basic_mid_range, basic_mid_range, basic_restricted_area,
                            basic_right_corner_3]
    # Shot Zone Area List : Area zone data for each of the 20 shot zones
    shot_zone_area_list = [area_back_court, area_center, area_left_side_center, area_right_side_center,
                           area_back_court, area_center, area_center, area_left_side, area_right_side,
                           area_left_side, area_center, area_center, area_left_side_center, area_left_side,
                           area_left_side, area_right_side_center, area_right_side, area_right_side,
                           area_center, area_right_side ]
    # Shot Zone Range List : Range zone data for each of the 20 shot zones
    shot_zone_range_list = [range_back_court, range_24, range_24, range_24, range_back_court, range_8_to_16,
                            range_0_to_8, range_8_to_16, range_8_to_16, range_24, range_8_to_16, range_16_to_24,
                            range_16_to_24, range_16_to_24, range_8_to_16, range_16_to_24, range_16_to_24,
                            range_8_to_16, range_0_to_8, range_24]

    # Player shot chart detail
    time.sleep(0.5)
    player_shot_data = shotchartdetail.ShotChartDetail(context_measure_simple = 'FGA', team_id=0, player_id=player_id, season_nullable=season, season_type_all_star='Regular Season')
    player_shot_chart_df = player_shot_data.get_data_frames()[0]
    
    # Columns needed to calculate the above data
    data_columns = [shot_zone_basic, shot_zone_area, shot_zone_range, shot_attempted_flag, shot_made_flag, shot_distance]
    filtered_player_shot_df = player_shot_chart_df[data_columns]
    print('Filtered pLayer shot')
    print(filtered_player_shot_df)
    total_FGA = len(filtered_player_shot_df.index)

    # League Average Data
    filtered_league_shot_df = player_shot_data.get_data_frames()[1]

    # ==============================    Generates Player Shot Chart Dataframe for all 20 shot zones   ==============================
    # Define columns for data frame
    shot_zone_averages_df = pd.DataFrame(columns=[shot_zone_basic, shot_zone_area, shot_zone_range, fga, fgm, rel_fgp, fgf, player_fgp, league_fgp])
    for shot_zone_number in range(0, 20):
        current_player_zone = filtered_player_shot_df.loc[(filtered_player_shot_df[shot_zone_basic] == shot_zone_basic_list[shot_zone_number])
                                                & (filtered_player_shot_df[shot_zone_area] == shot_zone_area_list[shot_zone_number])
                                                & (filtered_player_shot_df[shot_zone_range] == shot_zone_range_list[shot_zone_number])]
        current_player_zone_FGM = current_player_zone.SHOT_MADE_FLAG.sum()
        current_player_zone_FGA = current_player_zone.SHOT_ATTEMPTED_FLAG.sum()
        current_player_zone_AVG = 0
        current_player_zone_relative_AVG = 0
        current_player_zone_FREQ = 0
        current_league_zone = filtered_league_shot_df.loc[(filtered_league_shot_df[shot_zone_basic] == shot_zone_basic_list[shot_zone_number])
                                                & (filtered_league_shot_df[shot_zone_area] == shot_zone_area_list[shot_zone_number])
                                                & (filtered_league_shot_df[shot_zone_range] == shot_zone_range_list[shot_zone_number])]

        current_league_zone_AVG = current_league_zone.FG_PCT.tolist()
        if len(current_league_zone_AVG) > 0:
            current_league_zone_AVG = current_league_zone_AVG[0]

        # Don't want to divide by 0
        if total_FGA != 0:
            current_player_zone_FREQ = current_player_zone_FGA/total_FGA
        
        # Don't want to divide by 0
        if current_player_zone_FGA != 0:
            current_player_zone_AVG = (current_player_zone_FGM/current_player_zone_FGA)
            current_player_zone_relative_AVG = current_player_zone_AVG - current_league_zone_AVG
        current_player_zone_data = [shot_zone_basic_list[shot_zone_number], shot_zone_area_list[shot_zone_number],
                             shot_zone_range_list[shot_zone_number], current_player_zone_FGA, current_player_zone_FGM,
                             current_player_zone_relative_AVG,current_player_zone_FREQ, current_player_zone_AVG,
                             current_league_zone_AVG]
        shot_zone_averages_df.loc[shot_zone_number] = current_player_zone_data
    
    # Generate  DataFrame containing FG% data relative to distance away from rim
    distance_averages_df = pd.DataFrame(columns=[fgm, fga, shot_distance, player_fgp])
    for distance_from_rim in range(0, 31):
        current_player_distance = filtered_player_shot_df.loc[(filtered_player_shot_df[shot_distance] == distance_from_rim)]
        current_player_distance_FGM = current_player_distance.SHOT_MADE_FLAG.sum()
        current_player_distance_FGA = current_player_distance.SHOT_ATTEMPTED_FLAG.sum()
        current_player_distance_AVG = 0

        # Don't want to divide by 0
        if current_player_distance_FGA != 0:
            current_player_distance_AVG = (current_player_distance_FGM/current_player_distance_FGA)
        
        current_player_distance_data = [current_player_distance_FGM, current_player_distance_FGA,
                             distance_from_rim, current_player_distance_AVG]
        distance_averages_df.loc[distance_from_rim] = current_player_distance_data

    return shot_zone_averages_df, distance_averages_df

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

# Callback updates options for people-dropdown based on group selected
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

# Callback updates graph based on player/team selected
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
        # Pie chart for display record data
        record_pie_labels = ['WINS','LOSSES']
        record_pie_values = [filtered_team_yby_df.iloc[0]['WINS'], filtered_team_yby_df.iloc[0]['LOSSES']]
        record_pie = go.Figure(data=[go.Pie(labels=record_pie_labels, values=record_pie_values)])
        colors=['cyan','orange']
        record_pie.update_traces(marker=dict(colors=colors))
        # Bar graph for displaying basic data 
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
        # Bar graph for displaying basic data 
        basic_stats_x = ['REB','AST','STL','BLK','TOV','PTS']
        basic_stats_y = [filtered_player_df.loc['REB'],filtered_player_df.loc['AST'],
             filtered_player_df.loc['STL'],filtered_player_df.loc['BLK'],
             filtered_player_df.loc['TOV'],filtered_player_df.loc['PTS']]
        basic_stats_bar = go.Figure(data=[go.Bar(x=basic_stats_x,y=basic_stats_y,name=player_team_selected)])
        # Bar graph for displaying percentages
        perc_stats_x = ['FG_PCT','FG3_PCT','FT_PCT']
        perc_stats_y = np.multiply(100, [filtered_player_df.loc['FG_PCT'],filtered_player_df.loc['FG3_PCT'],
             filtered_player_df.loc['FT_PCT']])
        perc_stats_bar = go.Figure(data=[go.Bar(x=perc_stats_x,y=perc_stats_y,name=player_team_selected)])
        # Scatter plot for displaying shot chart data
        player_zone_averages_df, player_distance_averages_df = generate_player_shotchart_averages(player_id, season)
        print('Player Distance Averages')
        print(player_distance_averages_df)
        player_shot_data = shotchartdetail.ShotChartDetail(context_measure_simple = 'FGA', team_id=0, player_id=player_id, season_nullable=season, season_type_all_star='Regular Season')
        player_shot_df = player_shot_data.get_data_frames()[0]
        data_columns = ['SHOT_ZONE_BASIC','SHOT_ZONE_AREA','SHOT_ZONE_RANGE','SHOT_DISTANCE','LOC_X','LOC_Y']
        filtered_player_shot_df = player_shot_df[data_columns]
        merged_df = pd.merge(filtered_player_shot_df, player_zone_averages_df,how='inner', on=['SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA','SHOT_ZONE_RANGE'])
        # print('MERGED DATA FRAME')
        # print(merged_df)
        xlocs = merged_df['LOC_X'].tolist()
        ylocs = merged_df['LOC_Y'].tolist()
        shot_freq = merged_df['FREQ'].tolist()
        rel_shot_accur = merged_df['RELATIVE_FG_PCT'].tolist()
        league_shot_accur = merged_df['LEAGUE_FG_PCT'].tolist()
        player_shot_accur = merged_df['PLAYER_FG_PCT'].tolist()
        player_shot_chart = go.Figure()
        draw_plotly_court(player_shot_chart)
        colorscale = 'RdYlBu_r'
        marker_cmin = -0.05
        marker_cmax = 0.05
        ticktexts = ["Worse", "Average", "Better"]
        hexbin_text = [
            '<i>Relative Accuracy: </i>' + str(round(rel_shot_accur[i]*100, 1)) + '% (vs league avg)<BR>'
            '<i>Player Accuracy: </i>' + str(round(player_shot_accur[i]*100, 2)) + '% (player avg)<BR>'
            '<i>League Accuracy: </i>' + str(round(league_shot_accur[i]*100, 3)) + '% (league avg)<BR>'
            '<i>Frequency: </i>' + str(round(shot_freq [i]*100, 4)) + '%'
            for i in range(len(shot_freq))
            ]
        player_shot_chart.add_trace(go.Scatter(
            x=xlocs, y=ylocs, mode='markers', name='markers', text=hexbin_text,
            marker=dict(
                size=shot_freq, sizemode='area', sizeref=2. * max(shot_freq, default=0) / (11. ** 2), sizemin=2.5,
                line=dict(width=1, color='#333333'), symbol='hexagon',
                color = rel_shot_accur, colorscale = colorscale,
                colorbar=dict(
                    thickness=15,
                    x=0.84,
                    y=0.87,
                    yanchor='middle',
                    len=0.2,
                    title=dict(
                        text="<B>Accuracy</B>",
                        font=dict(
                            size=11,
                            color='#4d4d4d'
                        ),
                    ),
                    tickvals=[marker_cmin, (marker_cmin + marker_cmax) / 2, marker_cmax],
                    ticktext=ticktexts,
                    tickfont=dict(
                        size=11,
                        color='#4d4d4d'
                    )
                ),
                cmin=marker_cmin, cmax=marker_cmax,
            ),
            hoverinfo='text'
        ))
        return [
            html.Div(children='''
                                Player Shot Chart Data
                               ''',
                     style={
                         'textAlign': 'center'
                     }),

            html.Div([
                dcc.Graph(figure=player_shot_chart), 
            ]
            ),

            html.Div(children='''
                                Player Basic Bar Data
                               ''',
                     style={
                         'textAlign': 'center'
                     }),

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

            html.Div([
                dcc.Graph(figure=perc_stats_bar), 
            ]
            ),  
        ]


# Callback updates value for people-dropdown based on player/team selected
@app.callback(
    Output('people-dropdown', 'value'),
    [Input('people-dropdown', 'options')])
def set_people_value(available_options):
    return available_options[0]['value']

if __name__ == '__main__':
    app.run_server(debug=True)

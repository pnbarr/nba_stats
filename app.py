# -*- coding: utf-8 -*-
import dash
import matplotlib
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonallplayers, leaguegamefinder, commonplayerinfo, playercareerstats, teamyearbyyearstats, shotchartdetail
from nba_api.stats.endpoints import shotchartlineupdetail
from nba_api.stats.library.parameters import Season
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import time
from mongoengine import connect
from database import Player

# ==================================== SandBox Area ==================================================== #
# Create to Mongodb if database does not exist or connect to database if it exists
connect("nba-api-static-lists")

nba_teams = teams.get_teams()  # nba_teams is a list of dictionaries
# print('First NBA team data example.')
# print(nba_teams[0])
# KEYS
# 'id'
# 'full_name'
# 'abbreviation'
# 'nickname'
# 'city'
# 'state'
# 'year_founded'

players_nba = players.get_players()  # nba_players is a list of dictionaries
# print('Frist NBA player data example.')
# print(nba_players[0])
# KEYS
# 'id'
# 'full_name'
# 'first_name'
# 'last_name'
# 'is_active'

team_example = teamyearbyyearstats.TeamYearByYearStats(
    team_id=nba_teams[0]['id'])
team_example_df = team_example.get_data_frames()[0]
# team_example_year_df = team_example_df.loc[(team_example_df['YEAR'] == '2018-19')]
# print(team_example_year_df)

# Function should take a year season as an input and return list of players who played that year
# player_example = playercareerstats.PlayerCareerStats(player_id='2544')
# player_example = playercareerstats.PlayerCareerStats(player_id='76001')
# player_example_df = player_example.get_data_frames()[0]
# list_of_seasons = player_example_df['SEASON_ID'].values.tolist()
list_of_applicable_seasons = ['1996-97', '1997-98', '1998-99', '1999-00', '2000-01', '2001-02', '2002-03', '2003-04', '2004-05',
                              '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14',
                              '2014-15', '2015-16', '2016-17', '2017-18', '2018-19']

# Compile list of players who played anytime between the seasons 1996-97 - 2018-19
# nba_players = []

# for player in players_nba[:5]:
#     player_id = player['id']
#     time.sleep(1)
#     player_career_stats = playercareerstats.PlayerCareerStats(
#         player_id=player_id)
#     time.sleep(1)
#     player_career_stats_df = player_career_stats.get_data_frames()[0]
#     list_of_seasons = player_career_stats_df['SEASON_ID'].values.tolist()
#     player_in_relevant_time_frame = any(
#         item in list_of_seasons for item in list_of_applicable_seasons)
#     if player_in_relevant_time_frame == True:
#         nba_players.append(player)
#         print(player)
#         print(type(player))

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
    team_options = set_people_dropdown_options('Team')
    marks_year_slider = {0: '1996-97',
                         1: '1997-98',
                         2: '1998-99',
                         3: '1999-00',
                         4: '2000-01',
                         5: '2001-02',
                         6: '2002-03',
                         7: '2003-04',
                         8: '2004-05',
                         9: '2005-06',
                         10: '2006-07',
                         11: '2007-08',
                         12: '2008-09',
                         13: '2009-10',
                         14: '2010-11',
                         15: '2011-12',
                         16: '2012-13',
                         17: '2013-14',
                         18: '2014-15',
                         19: '2015-16',
                         20: '2016-17',
                         21: '2017-18',
                         22: '2018-19', }
    min_year_slider = 0
    max_year_slider = 22
    value_year_slider = 0
    team_value = team_options[0]['value']
    return [
        html.Div([
            dcc.Dropdown(id='team-dropdown',
                         options=team_options,
                         value=team_value),
            dcc.Slider(id='team-year-slider',
                       marks=marks_year_slider,
                       min=min_year_slider,
                       max=max_year_slider,
                       value=value_year_slider),
            html.Div(id='team-tab-content')
        ])
    ]

def build_player_tab():
    player_options = set_people_dropdown_options('Player')
    marks_year_slider = {0: '1996-97',
                         1: '1997-98',
                         2: '1998-99',
                         3: '1999-00',
                         4: '2000-01',
                         5: '2001-02',
                         6: '2002-03',
                         7: '2003-04',
                         8: '2004-05',
                         9: '2005-06',
                         10: '2006-07',
                         11: '2007-08',
                         12: '2008-09',
                         13: '2009-10',
                         14: '2010-11',
                         15: '2011-12',
                         16: '2012-13',
                         17: '2013-14',
                         18: '2014-15',
                         19: '2015-16',
                         20: '2016-17',
                         21: '2017-18',
                         22: '2018-19', }
    min_year_slider = 0
    max_year_slider = 22
    value_year_slider = 0
    player_value = player_options[0]['value']
    return [
        html.Div([
            dcc.Store(id='player-store', storage_type='session'),
            dcc.Dropdown(id='player-dropdown',
                         options=player_options,
                         value=player_value),
            dcc.Slider(id='player-year-slider',
                       marks=marks_year_slider,
                       min=min_year_slider,
                       max=max_year_slider,
                       value=value_year_slider),
            dcc.RadioItems(
                id='shotfilter-radio',
                options=[
                    {'label': 'Season', 'value': 'season'},
                    {'label': '1st Quarter', 'value': 'first'},
                    {'label': '2nd Quarter', 'value': 'second'},
                    {'label': '3rd Quarter', 'value': 'third'},
                    {'label': '4th Quarter', 'value': 'fourth'}
                ],
                value='season',
                labelStyle={'display': 'inline-block'},
                style={
                    'textAlign': 'center'
                }
            ),
            html.Div(id='player-tab-content')
        ])
    ]

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
                 path=ellipse_arc(
                     a=237.5, b=237.5, start_angle=0.386283101, end_angle=np.pi - 0.386283101),
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
                 path=ellipse_arc(y_center=417.5, a=60, b=60,
                                  start_angle=-0, end_angle=-np.pi),
                 line=dict(color=main_line_col, width=1), layer='below'),

        ]
    )
    return True

def generate_team_shotchart_averages(team_id, season):
    # Goal : Generate team's shot chart averages for each zone
    # Input : Team shot chart dataframe from shotchartdetail API endpoint
    # Output : Dataframe containing team's averages for each area for a given NBA Regular season

    # Columns of interest
    shot_zone_basic = 'SHOT_ZONE_BASIC'
    shot_zone_area = 'SHOT_ZONE_AREA'
    shot_zone_range = 'SHOT_ZONE_RANGE'
    shot_attempted_flag = 'SHOT_ATTEMPTED_FLAG'
    shot_made_flag = 'SHOT_MADE_FLAG'
    shot_distance = 'SHOT_DISTANCE'
    period = 'PERIOD'
    fgm = 'FGM'
    fga = 'FGA'
    rel_fgp = 'RELATIVE_FG_PCT'
    team_fgp = 'TEAM_FG_PCT'
    league_fgp = 'LEAGUE_FG_PCT'
    fgf = 'FREQ'

    # Shot Zone Basic strings
    basic_above_the_break_3 = 'Above the Break 3'
    basic_backcourt = 'Backcourt'
    basic_non_RA = 'In The Paint (Non-RA)'
    basic_left_corner_3 = 'Left Corner 3'
    basic_mid_range = 'Mid-Range'
    basic_restricted_area = 'Restricted Area'
    basic_right_corner_3 = 'Right Corner 3'

    # Shot Zone Area strings
    area_back_court = 'Back Court(BC)'
    area_center = 'Center(C)'
    area_left_side_center = 'Left Side Center(LC)'
    area_right_side_center = 'Right Side Center(RC)'
    area_left_side = 'Left Side(L)'
    area_right_side = 'Right Side(R)'

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
                           area_center, area_right_side]
    # Shot Zone Range List : Range zone data for each of the 20 shot zones
    shot_zone_range_list = [range_back_court, range_24, range_24, range_24, range_back_court, range_8_to_16,
                            range_0_to_8, range_8_to_16, range_8_to_16, range_24, range_8_to_16, range_16_to_24,
                            range_16_to_24, range_16_to_24, range_8_to_16, range_16_to_24, range_16_to_24,
                            range_8_to_16, range_0_to_8, range_24]

    # team shot chart detail
    time.sleep(0.5)
    team_shot_data = shotchartdetail.ShotChartDetail(
        context_measure_simple='FGA', team_id=team_id, player_id=0, season_nullable=season, season_type_all_star='Regular Season')
    team_shot_chart_df = team_shot_data.get_data_frames()[0]

    # Columns needed to calculate the above data
    data_columns = [shot_zone_basic, shot_zone_area, shot_zone_range,
                    shot_attempted_flag, shot_made_flag, shot_distance, period]
    filtered_team_shot_df = team_shot_chart_df[data_columns]
    total_FGA = len(filtered_team_shot_df.index)

    # League Average Data
    filtered_league_shot_df = team_shot_data.get_data_frames()[1]

    # ==============================    Generates team Shot Chart Dataframe for all 20 shot zones   ==============================
    # Define columns for data frame
    shot_zone_averages_df = pd.DataFrame(columns=[
                                         shot_zone_basic, shot_zone_area, shot_zone_range, fga, fgm, rel_fgp, fgf, team_fgp, league_fgp])
    for shot_zone_number in range(0, 20):
        current_team_zone = filtered_team_shot_df.loc[(filtered_team_shot_df[shot_zone_basic] == shot_zone_basic_list[shot_zone_number])
                                                      & (filtered_team_shot_df[shot_zone_area] == shot_zone_area_list[shot_zone_number])
                                                      & (filtered_team_shot_df[shot_zone_range] == shot_zone_range_list[shot_zone_number])]
        current_team_zone_FGM = current_team_zone.SHOT_MADE_FLAG.sum()
        current_team_zone_FGA = current_team_zone.SHOT_ATTEMPTED_FLAG.sum()
        current_team_zone_AVG = 0
        current_team_zone_relative_AVG = 0
        current_team_zone_FREQ = 0
        current_league_zone = filtered_league_shot_df.loc[(filtered_league_shot_df[shot_zone_basic] == shot_zone_basic_list[shot_zone_number])
                                                          & (filtered_league_shot_df[shot_zone_area] == shot_zone_area_list[shot_zone_number])
                                                          & (filtered_league_shot_df[shot_zone_range] == shot_zone_range_list[shot_zone_number])]

        current_league_zone_AVG = current_league_zone.FG_PCT.tolist()
        if len(current_league_zone_AVG) > 0:
            current_league_zone_AVG = current_league_zone_AVG[0]

        # Don't want to divide by 0
        if total_FGA != 0:
            current_team_zone_FREQ = current_team_zone_FGA/total_FGA

        # Don't want to divide by 0
        if current_team_zone_FGA != 0:
            current_team_zone_AVG = (
                current_team_zone_FGM/current_team_zone_FGA)
            current_team_zone_relative_AVG = current_team_zone_AVG - current_league_zone_AVG
        current_team_zone_data = [shot_zone_basic_list[shot_zone_number], shot_zone_area_list[shot_zone_number],
                                  shot_zone_range_list[shot_zone_number], current_team_zone_FGA, current_team_zone_FGM,
                                  current_team_zone_relative_AVG, current_team_zone_FREQ, current_team_zone_AVG,
                                  current_league_zone_AVG]
        shot_zone_averages_df.loc[shot_zone_number] = current_team_zone_data

    return shot_zone_averages_df


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
    period = 'PERIOD'
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
    basic_right_corner_3 = 'Right Corner 3'

    # Shot Zone Area strings
    area_back_court = 'Back Court(BC)'
    area_center = 'Center(C)'
    area_left_side_center = 'Left Side Center(LC)'
    area_right_side_center = 'Right Side Center(RC)'
    area_left_side = 'Left Side(L)'
    area_right_side = 'Right Side(R)'

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
                           area_center, area_right_side]
    # Shot Zone Range List : Range zone data for each of the 20 shot zones
    shot_zone_range_list = [range_back_court, range_24, range_24, range_24, range_back_court, range_8_to_16,
                            range_0_to_8, range_8_to_16, range_8_to_16, range_24, range_8_to_16, range_16_to_24,
                            range_16_to_24, range_16_to_24, range_8_to_16, range_16_to_24, range_16_to_24,
                            range_8_to_16, range_0_to_8, range_24]

    # Player shot chart detail
    time.sleep(0.5)
    player_shot_data = shotchartdetail.ShotChartDetail(
        context_measure_simple='FGA', team_id=0, player_id=player_id, season_nullable=season, season_type_all_star='Regular Season')
    player_shot_chart_df = player_shot_data.get_data_frames()[0]

    # Columns needed to calculate the above data
    data_columns = [shot_zone_basic, shot_zone_area, shot_zone_range,
                    shot_attempted_flag, shot_made_flag, shot_distance, period]
    filtered_player_shot_df = player_shot_chart_df[data_columns]
    total_FGA = len(filtered_player_shot_df.index)

    # League Average Data
    filtered_league_shot_df = player_shot_data.get_data_frames()[1]

    # ==============================    Generates Player Shot Chart Dataframe for all 20 shot zones   ==============================
    # Define columns for data frame
    shot_zone_averages_df = pd.DataFrame(columns=[
                                         shot_zone_basic, shot_zone_area, shot_zone_range, fga, fgm, rel_fgp, fgf, player_fgp, league_fgp])
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
            current_player_zone_AVG = (
                current_player_zone_FGM/current_player_zone_FGA)
            current_player_zone_relative_AVG = current_player_zone_AVG - current_league_zone_AVG
        current_player_zone_data = [shot_zone_basic_list[shot_zone_number], shot_zone_area_list[shot_zone_number],
                                    shot_zone_range_list[shot_zone_number], current_player_zone_FGA, current_player_zone_FGM,
                                    current_player_zone_relative_AVG, current_player_zone_FREQ, current_player_zone_AVG,
                                    current_league_zone_AVG]
        shot_zone_averages_df.loc[shot_zone_number] = current_player_zone_data

    # Generate  DataFrame containing FG% data relative to distance away from rim
    distance_averages_df = pd.DataFrame(
        columns=[fgm, fga, shot_distance, player_fgp])
    for distance_from_rim in range(0, 36):
        current_player_distance = filtered_player_shot_df.loc[(
            filtered_player_shot_df[shot_distance] == distance_from_rim)]
        current_player_distance_FGM = current_player_distance.SHOT_MADE_FLAG.sum()
        current_player_distance_FGA = current_player_distance.SHOT_ATTEMPTED_FLAG.sum()
        current_player_distance_AVG = 0

        # Don't want to divide by 0
        if current_player_distance_FGA != 0:
            current_player_distance_AVG = (
                current_player_distance_FGM/current_player_distance_FGA)

        current_player_distance_data = [current_player_distance_FGM, current_player_distance_FGA,
                                        distance_from_rim, current_player_distance_AVG]
        distance_averages_df.loc[distance_from_rim] = current_player_distance_data

    # Generate  DataFrame containing FG% data relative to period
    quarters_averages_df = pd.DataFrame(columns=[
                                        shot_zone_basic, shot_zone_area, shot_zone_range, fgm, fga, period, player_fgp, fgf])
    row_count = 0
    for quarter in range(1, 5):
        current_quarter_total_FGA = 0
        current_quarter_total_FGA = filtered_player_shot_df.loc[(
            filtered_player_shot_df[period] == quarter)].SHOT_ATTEMPTED_FLAG.sum()
        for shot_zone_number in range(0, 20):
            current_player_quarter = filtered_player_shot_df.loc[(filtered_player_shot_df[shot_zone_basic] == shot_zone_basic_list[shot_zone_number])
                                                                 & (filtered_player_shot_df[shot_zone_area] == shot_zone_area_list[shot_zone_number])
                                                                 & (filtered_player_shot_df[shot_zone_range] == shot_zone_range_list[shot_zone_number])
                                                                 & (filtered_player_shot_df[period] == quarter)]

            current_player_quarter_FGM = current_player_quarter.SHOT_MADE_FLAG.sum()
            current_player_quarter_FGA = current_player_quarter.SHOT_ATTEMPTED_FLAG.sum()
            current_player_quarter_FREQ = 0
            current_player_quarter_AVG = 0

            # Don't want to divide by 0
            if current_quarter_total_FGA != 0:
                current_player_quarter_FREQ = current_player_quarter_FGA/current_quarter_total_FGA

            # Don't want to divide by 0
            if current_player_quarter_FGA != 0:
                current_player_quarter_AVG = (
                    current_player_quarter_FGM/current_player_quarter_FGA)

            current_player_quarter_data = [shot_zone_basic_list[shot_zone_number], shot_zone_area_list[shot_zone_number],
                                           shot_zone_range_list[shot_zone_number], current_player_quarter_FGM, current_player_quarter_FGA,
                                           quarter, current_player_quarter_AVG, current_player_quarter_FREQ]
            quarters_averages_df.loc[row_count] = current_player_quarter_data
            row_count += 1

    return shot_zone_averages_df, distance_averages_df, quarters_averages_df

def set_people_dropdown_options(group):
    if group == 'Team':
        nba_team_list = []
        for team in nba_teams:
            nba_team_list.append(team['full_name'])
        return [{'label': i, 'value': i} for i in nba_team_list]
    else:
        nba_player_list_test = []
        nba_players_test = Player.objects
        for player_test in nba_players_test:
            nba_player_list_test.append(player_test.full_name)
        return [{'label': i, 'value': i} for i in nba_player_list_test]


# ======================================================================================================= #
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

group_options = ['Team', 'Player']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config["suppress_callback_exceptions"] = True

app.layout = html.Div(children=[
    html.H1(children='NBA Shooting Trends 1996-97 through 2018-19 Seasons', style={
        'textAlign': 'center'
    }),

    html.Div(
        id="app-container",
        children=[
            build_tabs(),
            # Main app
            html.Div(id="app-content"),
        ],
    ),
])

# Callback to update tabs
@app.callback(
    [Output('app-content', 'children')],
    [Input('tabs-group', 'value')],
)
def render_tab_content(tab_switch):
    if tab_switch == 'Player':
        return build_player_tab()
    if tab_switch == 'Team':
        return build_team_tab()

# Callback updates year-slider based on player seleced
@app.callback(
    [Output('player-year-slider', 'marks'),
     Output('player-year-slider', 'min'),
     Output('player-year-slider', 'max'),
     Output('player-year-slider', 'value'),
     Output('player-store', 'data')],
    [Input('player-dropdown', 'value'), ])
def set_player_year_marks(player_selected):
    player_info_test = ([player for player in Player.objects
                   if player.full_name == player_selected][0]).to_mongo().to_dict()
    player_id = player_info_test['player_id']
    player_career_data = playercareerstats.PlayerCareerStats(
        player_id=player_id)
    player_career_df = player_career_data.get_data_frames()[0]
    seasons_played = player_career_df['SEASON_ID'].values.tolist()
    players_applicable_seasons = sorted(
        set(seasons_played).intersection(list_of_applicable_seasons))
    marks = {}
    for i in range(0, len(players_applicable_seasons)):
        marks[i] = players_applicable_seasons[i]
    return marks, 0, len(players_applicable_seasons) - 1, 0, player_selected

# Callback updates tab content if team selected
@app.callback(
    Output('team-tab-content', 'children'),
    [Input('team-dropdown', 'value'),
     Input('team-year-slider', 'value'),
     Input('team-year-slider', 'marks')])
def update_team_tab(team_selected, year_selected_key, year_marks):
    year_selected_map = {0: '1996-97',
                         1: '1997-98',
                         2: '1998-99',
                         3: '1999-00',
                         4: '2000-01',
                         5: '2001-02',
                         6: '2002-03',
                         7: '2003-04',
                         8: '2004-05',
                         9: '2005-06',
                         10: '2006-07',
                         11: '2007-08',
                         12: '2008-09',
                         13: '2009-10',
                         14: '2010-11',
                         15: '2011-12',
                         16: '2012-13',
                         17: '2013-14',
                         18: '2014-15',
                         19: '2015-16',
                         20: '2016-17',
                         21: '2017-18',
                         22: '2018-19', }
    selected_year = year_selected_map[year_selected_key]
    team_info = [team for team in nba_teams
                 if team['full_name'] == team_selected][0]
    team_id = team_info['id']

    # Scatter plot data for team shot chart data
    team_zone_averages_df = generate_team_shotchart_averages(
        team_id, selected_year)
    team_shot_data = shotchartdetail.ShotChartDetail(
        context_measure_simple='FGA', team_id=team_id, player_id=0, season_nullable=selected_year, season_type_all_star='Regular Season')
    team_shot_df = team_shot_data.get_data_frames()[0]
    data_columns = ['SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE',
                    'SHOT_DISTANCE', 'LOC_X', 'LOC_Y', 'PERIOD', 'SHOT_MADE_FLAG']
    filtered_team_shot_df = team_shot_df[data_columns]
    season_merged_df = pd.merge(filtered_team_shot_df, team_zone_averages_df, how='inner', on=[
        'SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'])
    season_xlocs = season_merged_df['LOC_X'].tolist()
    season_ylocs = season_merged_df['LOC_Y'].tolist()
    season_shot_freq = season_merged_df['FREQ'].tolist()
    season_rel_shot_accur = season_merged_df['RELATIVE_FG_PCT'].tolist()
    season_league_shot_accur = season_merged_df['LEAGUE_FG_PCT'].tolist()
    season_team_shot_accur = season_merged_df['TEAM_FG_PCT'].tolist()
    season_team_shot_chart = go.Figure()
    draw_plotly_court(season_team_shot_chart)
    colorscale = 'RdYlBu_r'
    marker_cmin = -0.05
    marker_cmax = 0.05
    ticktexts = ["Below Average", "Average", "Above Average"]
    hexbin_text = [
        '<i>Relative Accuracy: </i>' +
        str(round(season_rel_shot_accur[i]
                  * 100, 1)) + '% (vs league avg)<BR>'
        '<i>Team Accuracy: </i>' +
        str(round(season_team_shot_accur[i]*100, 2)) + '% (team avg)<BR>'
        '<i>League Accuracy: </i>' +
        str(round(season_league_shot_accur[i]
                  * 100, 3)) + '% (league avg)<BR>'
        '<i>Frequency: </i>' + str(round(season_shot_freq[i]*100, 4)) + '%'
        for i in range(len(season_shot_freq))
    ]
    season_team_shot_chart.add_trace(go.Scatter(
        x=season_xlocs, y=season_ylocs, mode='markers', name='markers', text=hexbin_text,
        marker=dict(
            size=season_shot_freq, sizemode='area', sizeref=2. * max(season_shot_freq, default=0) / (11. ** 2), sizemin=2.5,
            line=dict(width=1, color='#333333'), symbol='hexagon',
            color=season_rel_shot_accur, colorscale=colorscale,
            colorbar=dict(
                thickness=15,
                x=0.75,
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
                tickvals=[marker_cmin,
                          (marker_cmin + marker_cmax) / 2, marker_cmax],
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

    team_example = teamyearbyyearstats.TeamYearByYearStats(team_id=team_id)
    team_example_df = team_example.get_data_frames()[0]
    team_example_year_df = team_example_df.loc[(
        team_example_df['YEAR'] == selected_year)]
    data_columns = ['FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM',
                    'FTA', 'FT_PCT', 'PTS', 'WINS', 'LOSSES', 'CONF_RANK', 'DIV_RANK', 'PTS_RANK']
    filtered_team_df = team_example_year_df[data_columns]
    # Point Totals Data
    total_points = filtered_team_df.iloc[0]['PTS']
    total_FG3_points = filtered_team_df.iloc[0]['FG3M'] * 3
    total_FT_points = filtered_team_df.iloc[0]['FTM']
    total_FG2_points = total_points - total_FG3_points - total_FT_points
    # Shooting Percentages Data
    fgm = filtered_team_df.iloc[0]['FGM']
    fga = filtered_team_df.iloc[0]['FGA']
    fg3m = filtered_team_df.iloc[0]['FG3M']
    fg3a = filtered_team_df.iloc[0]['FG3A']
    fg2a = fga - fg3a
    fta = filtered_team_df.iloc[0]['FTA']
    fg_perc = round(filtered_team_df.iloc[0]['FG_PCT'] * 100, 2)
    fg2_perc = round(((fgm-fg3m)/(fga-fg3a)) * 100, 2)
    fg3_perc = round(filtered_team_df.iloc[0]['FG3_PCT'] * 100, 2)
    ft_perc = round(filtered_team_df.iloc[0]['FT_PCT'] * 100, 2)
    # Team Performance Metrics
    wins = int(filtered_team_df.iloc[0]['WINS'])
    losses = int(filtered_team_df.iloc[0]['LOSSES'])
    record = str(wins) + '-' + str(losses)
    conf_rank = filtered_team_df.iloc[0]['CONF_RANK']
    div_rank = filtered_team_df.iloc[0]['DIV_RANK']
    pts_rank = filtered_team_df.iloc[0]['PTS_RANK']
    return [
        html.Div(children='''
                                Team Shot Chart Data
                               ''',
                 style={
                     'textAlign': 'center'
                 }),

        html.Div([
            html.Div([
                 dcc.Graph(figure=season_team_shot_chart)
                 ], className="six columns"),

            html.Div([
                html.Div(
                     [
                         html.Div(
                             [html.H6(id="win_pct", children=record),
                              html.P("Record")],
                             id="win_pct",
                             className="mini_container",
                         ),
                         html.Div(
                             [html.H6(id="conf_rank", children=conf_rank), html.P(
                                 "Conference Rank")],
                             id="conf_rank",
                             className="mini_container",
                         ),
                         html.Div(
                             [html.H6(id="div_rank", children=div_rank),
                              html.P("Division Rank")],
                             id="div_rank",
                             className="mini_container",
                         ),
                         html.Div(
                             [html.H6(id="pts_rank", children=pts_rank),
                              html.P("Points Rank")],
                             id="pts_rank",
                             className="mini_container",
                         ),
                     ],
                     id="info-container",
                     className="row container-display",
                     ),
                html.Div(
                    [
                        html.Div(
                            [html.H6(id="total_fga", children=fga),
                             html.P("Total FGA")],
                            id="total_fga",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.H6(id="total_FG2_fga", children=fg2a), html.P(
                                "Total 2PT FGA")],
                            id="total_FG2_fga",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.H6(id="total_FG3_fga", children=fg3a), html.P(
                                "Total 3PT FGA")],
                            id="total_FG3_fga",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.H6(id="total_FTA", children=fta),
                             html.P("Total FTA")],
                            id="total_FTA",
                            className="mini_container",
                        ),
                    ],
                    id="info-container",
                    className="row container-display",
                ),
                html.Div(
                    [
                        html.Div(
                            [html.H6(id="total_points", children=total_points), html.P(
                                "Total Points")],
                            id="total_points",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.H6(id="total_FG2_points", children=total_FG2_points), html.P(
                                "Total Points from 2PT FG")],
                            id="total_FG2_points",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.H6(id="total_FG3_points", children=total_FG3_points), html.P(
                                "Total Points from 3PT FG")],
                            id="total_FG3_points",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.H6(id="total_FT_points", children=total_FT_points), html.P(
                                "Total Points from FT")],
                            id="total_FT_points",
                            className="mini_container",
                        ),
                    ],
                    id="info-container",
                    className="row container-display",
                ),
                html.Div(
                    [
                        html.Div(
                            [html.H6(id="fg", children=fg_perc),
                             html.P("FG%")],
                            id="fg",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.H6(id="fg2", children=fg2_perc),
                             html.P("2-PT FG%")],
                            id="fg2",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.H6(id="fg3", children=fg3_perc),
                             html.P("3-PT FG%")],
                            id="fg3",
                            className="mini_container",
                        ),
                        html.Div(
                            [html.H6(id="ftp", children=ft_perc),
                             html.P("FT%")],
                            id="ftp",
                            className="mini_container",
                        ),
                    ],
                    id="info-container",
                    className="row container-display",
                ),
            ], className="six columns"),
        ], className="row")
    ]

# Callback updates player tab content based on player selected
@app.callback(
    Output('player-tab-content', 'children'),
    [Input('player-store', 'data'),
     Input('player-year-slider', 'value'),
     Input('player-year-slider', 'marks'),
     Input('shotfilter-radio', 'value')])
def update_statsgraph_figure(player_selected, year_selected_key, year_marks, shot_filter):
    selected_year = year_marks[str(year_selected_key)]
    player_info = ([player for player in Player.objects
                   if player.full_name == player_selected][0]).to_mongo().to_dict()
    player_id = player_info['player_id']
    player_career_data = playercareerstats.PlayerCareerStats(
        player_id=player_id)
    player_career_df = player_career_data.get_data_frames()[0]
    selected_year_data = player_career_df.loc[(
        player_career_df['SEASON_ID'] == selected_year)]
    # If player played for multiple teams in the same season, select total stats for that season
    if(len(selected_year_data.index) > 1):
        selected_year_data = selected_year_data.loc[(
            player_career_df['TEAM_ID'] == 0)]
    season = selected_year_data['SEASON_ID']

    # Scatter plot for displaying season shot chart data
    player_zone_averages_df, player_distance_averages_df, player_quarters_averages_df = generate_player_shotchart_averages(
        player_id, season)
    player_shot_data = shotchartdetail.ShotChartDetail(
        context_measure_simple='FGA', team_id=0, player_id=player_id, season_nullable=season, season_type_all_star='Regular Season')
    player_shot_df = player_shot_data.get_data_frames()[0]
    data_columns = ['SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA',
                    'SHOT_ZONE_RANGE', 'SHOT_DISTANCE', 'LOC_X', 'LOC_Y', 'PERIOD']
    filtered_player_shot_df = player_shot_df[data_columns]
    player_shot_chart = go.Figure()

    # Season Data
    if(shot_filter == 'season'):
        season_merged_df = pd.merge(filtered_player_shot_df, player_zone_averages_df, how='inner', on=[
                                    'SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'])
        season_xlocs = season_merged_df['LOC_X'].tolist()
        season_ylocs = season_merged_df['LOC_Y'].tolist()
        season_shot_freq = season_merged_df['FREQ'].tolist()
        season_rel_shot_accur = season_merged_df['RELATIVE_FG_PCT'].tolist()
        season_league_shot_accur = season_merged_df['LEAGUE_FG_PCT'].tolist()
        season_player_shot_accur = season_merged_df['PLAYER_FG_PCT'].tolist()
        draw_plotly_court(player_shot_chart)
        colorscale = 'RdYlBu_r'
        marker_cmin = -0.05
        marker_cmax = 0.05
        ticktexts = ["Below Average", "Average", "Above Average"]
        hexbin_text = [
            '<i>Relative Accuracy: </i>' +
            str(round(season_rel_shot_accur[i]
                      * 100, 1)) + '% (vs league avg)<BR>'
            '<i>Player Accuracy: </i>' +
            str(round(season_player_shot_accur[i]
                      * 100, 2)) + '% (player avg)<BR>'
            '<i>League Accuracy: </i>' +
            str(round(season_league_shot_accur[i]
                      * 100, 3)) + '% (league avg)<BR>'
            '<i>Frequency: </i>' + str(round(season_shot_freq[i]*100, 4)) + '%'
            for i in range(len(season_shot_freq))
        ]
        player_shot_chart.add_trace(go.Scatter(
            x=season_xlocs, y=season_ylocs, mode='markers', name='markers', text=hexbin_text,
            marker=dict(
                size=season_shot_freq, sizemode='area', sizeref=2. * max(season_shot_freq, default=0) / (11. ** 2), sizemin=2.5,
                line=dict(width=1, color='#333333'), symbol='hexagon',
                color=season_rel_shot_accur, colorscale=colorscale,
                colorbar=dict(
                    thickness=15,
                    x=0.75,
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
                    tickvals=[marker_cmin,
                              (marker_cmin + marker_cmax) / 2, marker_cmax],
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

    # Scatter plot for displaying season 1st quarter shot chart data
    if(shot_filter == 'first'):
        generate_quarter_shot_chart(1, filtered_player_shot_df, player_shot_chart, player_quarters_averages_df)

    # Scatter plot for displaying season 2nd quarter shot chart data
    if(shot_filter == 'second'):
        generate_quarter_shot_chart(2, filtered_player_shot_df, player_shot_chart, player_quarters_averages_df)

    # Scatter plot for displaying season 3rd quarter shot chart data
    if(shot_filter == 'third'):
        generate_quarter_shot_chart(3, filtered_player_shot_df, player_shot_chart, player_quarters_averages_df)

    # Scatter plot for displaying season 4th quarter shot chart data
    if(shot_filter == 'fourth'):
        generate_quarter_shot_chart(4, filtered_player_shot_df, player_shot_chart, player_quarters_averages_df)

    shot_distance_pct_fig = px.line(
        player_distance_averages_df, x="SHOT_DISTANCE", y="PLAYER_FG_PCT")

    return [
        html.Div(children='''
                                Player Shot Chart Data for the
                               '''
                 + season + ' Season',
                 style={
                     'textAlign': 'center'
                 }),

        html.Div([
            dcc.Graph(figure=player_shot_chart),
        ]
        ),

        html.Div(children='''
                                Player Shot Distance Data
                               ''',
                 style={
                     'textAlign': 'center'
                 }),

        html.Div([
            dcc.Graph(figure=shot_distance_pct_fig),
        ]
        ),
    ]


def generate_quarter_shot_chart(quarter_int, filtered_player_shot_df, player_shot_chart, player_quarters_averages_df):
    quarter_averages_df = player_quarters_averages_df.loc[(
        player_quarters_averages_df['PERIOD'] == quarter_int)]
    quarter_merged_df = pd.merge(filtered_player_shot_df, quarter_averages_df, how='inner', on=[
        'SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE', 'PERIOD'])
    quarter_xlocs = quarter_merged_df['LOC_X'].tolist()
    quarter_ylocs = quarter_merged_df['LOC_Y'].tolist()
    quarter_shot_FGM = quarter_merged_df['FGM'].tolist()
    quarter_shot_FGA = quarter_merged_df['FGA'].tolist()
    quarter_shot_freq = quarter_merged_df['FREQ'].tolist()
    quarter_shot = quarter_merged_df['PERIOD'].tolist()
    quarter_player_shot_accur = quarter_merged_df['PLAYER_FG_PCT'].tolist(
    )
    draw_plotly_court(player_shot_chart)
    colorscale = 'RdYlBu_r'
    marker_cmin = 0.2
    marker_cmax = 0.6
    ticktexts = ["Below 40%", "40%", "Above 40%"]
    hexbin_text = [
        '<i>Player Accuracy: </i>' +
        str(round(
            quarter_player_shot_accur[i]*100, 1)) + '% (player avg)<BR>'
        '<i>Period Taken: </i>' +
        str(round(quarter_shot[i], 2)) + ' (period taken)<BR>'
        '<i>Field Goals Made: </i>' +
        str(round(quarter_shot_FGM[i], 3)) + ' (FGM)<BR>'
        '<i>Field Goals Attempted: </i>' +
        str(round(quarter_shot_FGA[i], 4)) + ' (FGA)<BR>'
        '<i>Frequency: </i>' +
        str(round(quarter_shot_freq[i]
                  * 100, 5)) + '% (taken in quarter {})'.format(str(quarter_int))
        for i in range(len(quarter_xlocs))
    ]
    player_shot_chart.add_trace(go.Scatter(
        x=quarter_xlocs, y=quarter_ylocs, mode='markers', name='markers', text=hexbin_text,
        marker=dict(
            size=quarter_shot_freq, sizemode='area', sizeref=2. * max(quarter_shot_freq, default=0) / (11. ** 2), sizemin=2.5,
            line=dict(width=1, color='#333333'), symbol='hexagon',
            color=quarter_player_shot_accur, colorscale=colorscale,
            colorbar=dict(
                thickness=15,
                x=0.75,
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
                tickvals=[marker_cmin,
                          (marker_cmin + marker_cmax) / 2, marker_cmax],
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
    return player_shot_chart

if __name__ == '__main__':
    app.run_server(debug=True)

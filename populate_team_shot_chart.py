from database_schema import Teams, TeamShotDataSets
from nba_api.stats.endpoints import shotchartdetail
import pandas as pd
from mongoengine import connect
import time

# Connect to NBA Dashboard Database
print("Connecting to database . . .")
connect("nbaDashboardDB")
print("Connected to nbaDashboardDB database!")

# Dictionary of applicable years
year_selected_map = {0: "1996-97",
                     1: "1997-98",
                     2: "1998-99",
                     3: "1999-00",
                     4: "2000-01",
                     5: "2001-02",
                     6: "2002-03",
                     7: "2003-04",
                     8: "2004-05",
                     9: "2005-06",
                     10: "2006-07",
                     11: "2007-08",
                     12: "2008-09",
                     13: "2009-10",
                     14: "2010-11",
                     15: "2011-12",
                     16: "2012-13",
                     17: "2013-14",
                     18: "2014-15",
                     19: "2015-16",
                     20: "2016-17",
                     21: "2017-18",
                     22: "2018-19"}

# Relevant data columns
data_columns = ["SHOT_ZONE_BASIC", "SHOT_ZONE_AREA", "SHOT_ZONE_RANGE",
                "SHOT_DISTANCE", "LOC_X", "LOC_Y", "PERIOD", "SHOT_MADE_FLAG"]

def generate_team_shotchart_averages(team_id, season):
    # Goal : Generate team's shot chart averages for each zone
    # Input : team_id and season
    # Output : Dataframe containing team's averages for each area for a given NBA Regular season

    # Columns of interest
    shot_zone_basic = "SHOT_ZONE_BASIC"
    shot_zone_area = "SHOT_ZONE_AREA"
    shot_zone_range = "SHOT_ZONE_RANGE"
    shot_attempted_flag = "SHOT_ATTEMPTED_FLAG"
    shot_made_flag = "SHOT_MADE_FLAG"
    shot_distance = "SHOT_DISTANCE"
    period = "PERIOD"
    fgm = "FGM"
    fga = "FGA"
    rel_fgp = "RELATIVE_FG_PCT"
    team_fgp = "TEAM_FG_PCT"
    league_fgp = "LEAGUE_FG_PCT"
    fgf = "FREQ"

    # Shot Zone Basic strings
    basic_above_the_break_3 = "Above the Break 3"
    basic_backcourt = "Backcourt"
    basic_non_RA = "In The Paint (Non-RA)"
    basic_left_corner_3 = "Left Corner 3"
    basic_mid_range = "Mid-Range"
    basic_restricted_area = "Restricted Area"
    basic_right_corner_3 = "Right Corner 3"

    # Shot Zone Area strings
    area_back_court = "Back Court(BC)"
    area_center = "Center(C)"
    area_left_side_center = "Left Side Center(LC)"
    area_right_side_center = "Right Side Center(RC)"
    area_left_side = "Left Side(L)"
    area_right_side = "Right Side(R)"

    # Shot Zone Range strings
    range_back_court = "Back Court Shot"
    range_24 = "24+ ft."
    range_8_to_16 = "8-16 ft."
    range_0_to_8 = "Less Than 8 ft."
    range_16_to_24 = "16-24 ft."

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
        context_measure_simple="FGA", team_id=team_id, player_id=0, season_nullable=season, season_type_all_star="Regular Season")
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

    return shot_zone_averages_df, team_shot_chart_df

# Iterate through all teams in NBA
for team in Teams.objects:
    team_selected = team.full_name
    team_id = team.team_id
    # List of current team shot data objects by year
    team_shot_data_list = []
    print("Processing {0} data . . . ".format(team_selected))
    # Iterate through all applicable years for plotting shot chart data
    for year_index in range(0, 23):
        selected_year = year_selected_map[year_index]
        team_zone_averages_df, team_shot_df = generate_team_shotchart_averages(
            team_id, selected_year)
        filtered_team_shot_df = team_shot_df[data_columns]
        season_merged_df = pd.merge(filtered_team_shot_df, team_zone_averages_df, how="inner", on=[
            "SHOT_ZONE_BASIC", "SHOT_ZONE_AREA", "SHOT_ZONE_RANGE"])
        season_xlocs = season_merged_df["LOC_X"].tolist()
        season_ylocs = season_merged_df["LOC_Y"].tolist()
        season_shot_freq = season_merged_df["FREQ"].tolist()
        season_rel_shot_accur = season_merged_df["RELATIVE_FG_PCT"].tolist(
        )
        season_league_shot_accur = season_merged_df["LEAGUE_FG_PCT"].tolist(
        )
        season_team_shot_accur = season_merged_df["TEAM_FG_PCT"].tolist()
        current_team_shot_data_object = TeamShotDataSets(
            year=selected_year,
            xlocs=season_xlocs,
            ylocs=season_ylocs,
            shot_freq=season_shot_freq,
            rel_shot_accur=season_rel_shot_accur,
            league_shot_accur=season_league_shot_accur,
            team_shot_accur=season_team_shot_accur
        )
        team_shot_data_list.append(current_team_shot_data_object)
    team.shot_data = team_shot_data_list
    print("Saving {0} shot data to database . . .".format(team_selected))
    team.save()
    print("Finished saving {} shot data to database!".format(team_selected))
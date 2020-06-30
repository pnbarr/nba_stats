from mongoengine import connect
from database_schema import Teams, TeamShotDataSets
from nba_api.stats.endpoints import teamgamelogs
import pandas as pd
import time

# Data columns of interest
data_columns = ["FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT", "PTS"]

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
                         22: '2018-19'}

# Method to connect to NBA dashboard Database
def connect_to_database():
    print("Connecting to database . . .")
    connect("nbaDashboardDB")
    print("Connected to nbaDashboardDB database!")

# Method to get and process gamelog data from NBA stats site
def get_team_gamelog_data():
    # Iterate through all teams
    for team in Teams.objects:
        team_selected = team.full_name
        team_id = team.team_id
        print("Starting to process {} data . . .".format(team_selected))
        # Iterate through all years
        for key in year_selected_map:
            time.sleep(0.5)
            season = year_selected_map[key]
            print("Processing {} {} data . . .".format(season, team_selected))
            # Get data from NBA Stats API Endpoint
            team_gamelog_data = teamgamelogs.TeamGameLogs(
                team_id_nullable=team_id, season_nullable=season, season_type_nullable="Regular Season")
            team_gamelog_df = team_gamelog_data.get_data_frames()[0]
            filtered_team_gamelog_df = team_gamelog_df[data_columns]
            num_games_in_current_season = len(filtered_team_gamelog_df.index)

            # Initialize shooting data lists
            two_point_FGA_list = []
            two_point_FGM_list = []
            two_point_PCT_list = []
            two_point_points_total_list = []
            avg_pts_per_two_point_FGA_list = []
            three_point_FGA_list = []
            three_point_FGM_list = []
            three_point_PCT_list = []
            three_point_points_total_list = []
            avg_pts_per_three_point_FGA_list = []
            FTA_list = []
            FT_points_total_list = []
            avg_pts_per_FT_list = []
            ppg_list = []

            for game_index in range(0, num_games_in_current_season):
                row = filtered_team_gamelog_df.iloc[game_index]
                # Process 2-point data
                two_point_FGA = row.FGA - row.FG3A
                two_point_FGA_list.append(two_point_FGA)
                two_point_FGM = row.FGM - row.FG3M
                two_point_FGM_list.append(two_point_FGM)
                if(two_point_FGA != 0):
                    two_point_PCT = two_point_FGM/two_point_FGA
                else:
                    two_point_PCT = 0
                two_point_PCT_list.append(two_point_PCT)
                two_point_points_total = two_point_FGM * 2
                two_point_points_total_list.append(two_point_points_total)
                if(two_point_FGA != 0):
                    avg_pts_per_two_point_FGA = two_point_points_total / two_point_FGA
                else:
                    avg_pts_per_two_point_FGA = 0
                avg_pts_per_two_point_FGA_list.append(avg_pts_per_two_point_FGA)
                # Process 3-point data
                three_point_FGA_list.append(row.FG3A)
                three_point_FGM_list.append(row.FG3M)
                three_point_PCT_list.append(row.FG3_PCT)
                three_point_points_total = row.FG3M * 3
                three_point_points_total_list.append(three_point_points_total)
                if(row.FG3A != 0):
                    avg_pts_per_three_point_FGA = three_point_points_total / row.FG3A
                else:
                    avg_pts_per_three_point_FGA = 0
                avg_pts_per_three_point_FGA_list.append(avg_pts_per_three_point_FGA)
                # Process Free Throw data
                FTA_list.append(row.FTA)
                FT_points_total_list.append(row.FTM)
                avg_pts_per_FT_list.append(row.FT_PCT)
                # Process General Points data
                ppg_list.append(row.PTS)
            # Save to database collection
            current_team_object = Teams.objects(full_name=team_selected).first()
            current_team_object.shot_data[key].two_point_FGA_per_game = two_point_FGA_list
            current_team_object.shot_data[key].two_point_FGM_per_game = two_point_FGM_list
            current_team_object.shot_data[key].two_point_FG_PCT_per_game = two_point_PCT_list
            current_team_object.shot_data[key].two_point_points_total_per_game = two_point_points_total_list
            current_team_object.shot_data[key].avg_pts_per_two_point_FGA_per_game = avg_pts_per_two_point_FGA_list
            current_team_object.shot_data[key].three_point_FGA_per_game = three_point_FGA_list
            current_team_object.shot_data[key].three_point_FGM_per_game = three_point_FGM_list
            current_team_object.shot_data[key].three_point_FG_PCT_per_game = three_point_PCT_list
            current_team_object.shot_data[key].three_point_points_total_per_game = three_point_points_total_list
            current_team_object.shot_data[key].avg_pts_per_three_point_FGA_per_game = avg_pts_per_three_point_FGA_list
            current_team_object.shot_data[key].fta_per_game = FTA_list
            current_team_object.shot_data[key].ft_points_total_per_game = FT_points_total_list
            current_team_object.shot_data[key].avg_pts_per_ft_per_game = avg_pts_per_FT_list
            current_team_object.shot_data[key].points_per_game = ppg_list
            current_team_object.save()
            print("Done saving {} {} data.".format(season, team_selected))

def main():
    connect_to_database()
    get_team_gamelog_data()

if __name__ == "__main__":
    main()

from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from mongoengine import connect
from database_schema import Players
import time

list_of_applicable_seasons = ['1996-97', '1997-98', '1998-99', '1999-00', '2000-01', '2001-02', '2002-03', '2003-04', '2004-05',
                              '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12', '2012-13', '2013-14',
                              '2014-15', '2015-16', '2016-17', '2017-18', '2018-19']
players_nba = players.get_players()
# Create to Mongodb if database does not exist or connect to database if it exists
connect("nbaDashboardDB")
for player in players_nba[:10]:
    player_id = player['id']
    time.sleep(0.5)
    player_career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    player_career_stats_df = player_career_stats.get_data_frames()[0]
    list_of_seasons = player_career_stats_df['SEASON_ID'].values.tolist()
    player_in_relevant_time_frame = any(
        item in list_of_seasons for item in list_of_applicable_seasons)
    if player_in_relevant_time_frame == True:
        add_player_to_db = Players(
            player_id=player['id'],
            full_name=player['full_name'],
            first_name=player['first_name'],
            last_name=player['last_name'],
            is_active=player['is_active']
        ).save()
print('Done adding players to database collection.')
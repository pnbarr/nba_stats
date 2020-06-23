from nba_api.stats.static import teams
from mongoengine import connect
from database_schema import Teams

nba_teams = teams.get_teams()
# Create to Mongodb if database does not exist or connect to database if it exists
connect("nbaDashboardDB")
for team in nba_teams:
    team_id = team['id']
    add_team_to_db = Teams(
        team_id=team['id'],
        full_name=team['full_name'],
        abbreviation=team['abbreviation'],
        nickname=team['nickname'],
        city=team['city'],
        state=team['state'],
        year_founded=team['year_founded']
    ).save()
print('Done adding teamss to database collection.')
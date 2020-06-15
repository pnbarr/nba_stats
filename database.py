from mongoengine import connect
from mongoengine import Document
from mongoengine import IntField
from mongoengine import StringField
from mongoengine import BooleanField

# Create to Mongodb if database does not exist or connect to database if it exists
connect("nba-api-static-lists")

# Defining Documents

class Player(Document):
    player_id = IntField(required=True)
    full_name = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    is_active = BooleanField(required=True)

class Team(Document):
    team_id = IntField(required=True)
    full_name = StringField(required=True)
    abbreviation = StringField(required=True)
    nickname = StringField(required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    year_founded = IntField(required=True)
    
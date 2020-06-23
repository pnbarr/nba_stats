from mongoengine import connect
from mongoengine import Document
from mongoengine import IntField
from mongoengine import StringField
from mongoengine import BooleanField
from mongoengine import EmbeddedDocumentField
from mongoengine import ListField
from mongoengine import EmbeddedDocument
from mongoengine import FloatField
from mongoengine import EmbeddedDocumentListField
# Create to Mongodb if database does not exist or connect to database if it exists
# connect("nbaDashboardDB")

# Defining Documents

class TeamShotDataSets(EmbeddedDocument):
    year = StringField(required=True)
    xlocs = ListField(IntField())
    ylocs = ListField(IntField())
    shot_freq = ListField(FloatField())
    rel_shot_accur = ListField(FloatField())
    league_shot_accur = ListField(FloatField())
    team_shot_accur = ListField(FloatField())

class Players(Document):
    player_id = IntField(required=True)
    full_name = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    is_active = BooleanField(required=True)

class Teams(Document):
    team_id = IntField(required=True)
    full_name = StringField(required=True)
    abbreviation = StringField(required=True)
    nickname = StringField(required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    year_founded = IntField(required=True)
    shot_data = EmbeddedDocumentListField(TeamShotDataSets)
    

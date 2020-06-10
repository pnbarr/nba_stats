from mongoengine import connect
from mongoengine import Document
from mongoengine import IntField
from mongoengine import StringField
from mongoengine import BooleanField

# Create to Mongodb if database does not exist or connect to database if it exists
connect("nba-api-static-lists")

# Defining Documents

class Player(Document):
    player_id = IntField(unique=True, required=True)
    full_name = StringField(unique=True, required=True)
    first_name = StringField(unique=True, required=True)
    last_name = StringField(unique=True, required=True)
    is_active = BooleanField(unique=True, required=True)

# Save a document

player1 = Player(
    player_id=2544,
    full_name='LeBron James',
    first_name='LeBron',
    last_name='James',
    is_active=True
).save()

print('Done')
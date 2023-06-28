import sqlalchemy as db
from api import engine

random = "SELECT * FROM channel_data ORDER BY RAND() LIMIT 1"
url = ''

with engine.connect() as connection:
    # with engine.cursor() as cursor:
    url = connection.execute(db.text(random))

print(url.fetchall()[0])
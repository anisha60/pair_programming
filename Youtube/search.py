import sqlalchemy as db
from api import engine
from pyyoutube import Api
import webbrowser
import pprint

def underline(text):
    # print("\u0332".join(text))
    print('\x1B[4m' + text + '\x1B[0m')

random = "SELECT * FROM channel_data ORDER BY RAND() LIMIT 1"
url = ''

with engine.connect() as connection:
    # with engine.cursor() as cursor:
    url = connection.execute(db.text(random))

result = url.fetchall()[0]
# print(result)

channel_name = result[0]
channel_id = result[1]
channel_url = result[2]

apikey = "AIzaSyDDJhSQtGyf9IAlANGFVEyPh0AnbMghym4"
api = Api(api_key=apikey)
url = "https://www.googleapis.com/youtube/v3/videos?id=7lCDEYXw3mM&key={key} &fields=items(id,snippet(channelId,title,categoryId),statistics)&part=snippet,statistics"

channel_by_ids = api.get_channel_info(channel_id=channel_id)
channel_dict = channel_by_ids.items[0].to_dict()
# print(channel_dict)

description = channel_dict['snippet']['localized']['description']
country = channel_dict['snippet']['country']
custom_url = channel_dict['snippet']['customUrl']
views = channel_dict['statistics']['viewCount']
subscribers = channel_dict['statistics']['subscriberCount']
videos = channel_dict['statistics']['videoCount']


print('Random Channel Info')
print('--------------------')
print('Name: ' ,channel_name)
# print('id: ', channel_id)
print('Channel link: ', channel_url)
# print('')
print('Description: ', description)
print('Country: ', country)
print('Custom url: ', custom_url)
print('View count: ', views)
print('Subscriber count: ', subscribers)
print('Video count: ', videos)

webbrowser.open('http://www.' + channel_url)






from pyyoutube import Api
from selenium import webdriver
import json
import requests
import urllib.request
import string
import random
import pandas as pd
from getpass import getpass
from mysql.connector import connect, Error
import mysql


def getHTML(channels):
    driver = webdriver.Chrome()
    driver.implicitly_wait(0.5)
    channel_ids = []
    for channel in channels:
        try:
            channelUrl = 'https://www.youtube.com/@' + channel
            driver.get(channelUrl)
        except:
            continue
    # access HTML source code with page_source method
        s = driver.page_source
        # print(s)
        start_index = s.find('externalId')
        print(start_index)
        externalId =  s[start_index+13:start_index+37]
        print(externalId)
        channel_ids.append(externalId)
    return channel_ids
    

def getRandomIds(key):
    count = 50
    API_KEY = key
    randomID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

    urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(API_KEY,count,randomID)
    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    results = json.loads(data.decode(encoding))

    for data in results['items']:
        videoId = (data['id']['videoId'])
        print(videoId)
        #store your ids
    
    return results



apikey = "AIzaSyDDJhSQtGyf9IAlANGFVEyPh0AnbMghym4"
api = Api(api_key=apikey)
url = "https://www.googleapis.com/youtube/v3/videos?id=7lCDEYXw3mM&key={key} &fields=items(id,snippet(channelId,title,categoryId),statistics)&part=snippet,statistics"

# response = api.get_channel_info(channel_id="UCa-vrCLQHviTOVnEKDOdetQ")
channel_id = "https://www.youtube.com/@TifoIRL"

# response = api.get_channel_info(channel_id=channel_id)


# video_by_chart = api.get_videos_by_chart(chart="mostPopular", region_code="US", count=2)
# print(video_by_chart.items)

# channelId = getHTML(channel_id)

# channel = api.get_channel_info(channel_id=channelId)
# channel_dict = channel.items[0].to_dict()
# print(channel_dict)

# top_channels = pd.read_csv('Youtube/most_subscribed_youtube_channels.csv')
# print(top_channels)

# top_channels['Youtuber'] = top_channels['Youtuber'].str.replace(' ','')
# print(top_channels)

channel_ids_df = pd.read_csv('Youtube/output.csv')
print(channel_ids_df)

print(channel_ids_df.columns)
channel_ids_df['URL'] = channel_ids_df['ID'].apply(lambda x: 'youtube.com/channel/' + x)
channel_ids_df.rename(columns = {'ID':'ChannelID'}, inplace = True)
print(channel_ids_df)

# try:
#     with connect(
#         host="localhost",
#         user="sqluser",
#         password="password",
#     ) as connection:
#         create_db_query = "IF NOT EXISTS CREATE DATABASE channels"
#         # create_table = "CREATE TABLE channel_info"
#         with connection.cursor() as cursor:
#             cursor.execute(create_db_query)
#             # cursor.execute(create_table)
# except Error as e:
#     print(e)

mydb = mysql.connector.connect(
        host='localhost',
        user='sqluser',
        password='password',
        port = '3306',
        database='channels'
    )

cursor = mydb.cursor()

# df_to_mysql('channel_info',  mydb)


channel_ids_df.to_sql('channel_info', mydb, if_exists='replace', index = False)

# def df_to_mysql(df, db_tbl_name, conn, index=False):
#     df.to_sql(con = conn, name = db_tbl_name, if_exists='replace', index = False)








# random_ids = getRandomIds(apikey)

# for data in random_ids['items']:
#     videoId = (data['id']['videoId'])
#     video_by_id = api.get_video_by_id(video_id=videoId)
#     print(video_by_id.items)

    



# if channel_by_username.items:  # Check if the response contains items
#     # Access the channel information
#     channel_info = channel_by_username.items[0]
#     print(channel_info)

#     id = channel_info.id
#     print(id)
#     channel_by_id = api.get_channel_info(channel_id=id)
#     channel_dict = channel_by_id.items[0].to_dict()
#     print(channel_dict)
# else:
#     print("No channel information found.")


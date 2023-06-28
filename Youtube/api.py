# from oauthlib.uri_validate import userinfo
from pyyoutube import Api
from selenium import webdriver
import json
import requests
import urllib.request
import string
import random
# import pandas as pd
import mysql.connector

apikey = "AIzaSyDDJhSQtGyf9IAlANGFVEyPh0AnbMghym4"
api = Api(api_key=apikey)


def getHTML(channels):
    driver = webdriver.Chrome()
    driver.implicitly_wait(0.5)
    channel_ids = []
    for channel in channels:
        try:
            channelUrl = 'https://www.youtube.com/' + channel
            driver.get(channelUrl)
        except:
            continue
        # access HTML source code with page_source method
        s = driver.page_source
        # print(s)
        start_index = s.find('externalId')
        print(start_index)
        externalId = s[start_index + 13:start_index + 37]
        print(externalId)
        channel_ids.append(externalId)
    return channel_ids


def get_channel_name(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={apikey}"
    response = requests.get(url)
    data = json.loads(response.text)
    channel_name = data["items"][0]["snippet"]["channelTitle"]
    return channel_name


def check_link_working(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    response = requests.head(url)
    return response.status_code == 200


def insert_channel_id(channel_id, channel_name=None):
    # Establish a connection to the database
    mydb = mysql.connector.connect(
        host='localhost',
        user='notladi',
        password='xeno6',
        port='3308',
        database='channel_id'
    )

    # Create a cursor object
    mycursor = mydb.cursor()

    # Define the SQL query
    sql = "INSERT INTO channels (id_channel, channel_name) VALUES (%s, %s)"

    # Execute the query with the provided values
    val = (channel_id, channel_name)
    mycursor.execute(sql, val)

    # Commit the changes to the database
    mydb.commit()

    # Close the cursor and database connection
    mycursor.close()
    mydb.close()


def getRandomIds(key):
    count = 50
    API_KEY = key
    randomID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

    urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(
        API_KEY, count, randomID)
    webURL = urllib.request.urlopen(urlData)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    results = json.loads(data.decode(encoding))

    for data in results['items']:
        videoId = data['id']['videoId']
        print(videoId)

        # Assuming you have a function to check if the link is working, modify the condition below
        if check_link_working(videoId):
            # Assuming you have a function to get the channel name from the videoId
            channel_name = get_channel_name(videoId)
            insert_channel_id(videoId, channel_name)

    return results


def check_database_updates():
    # Establish a connection to the database
    mydb = mysql.connector.connect(
        host='localhost',
        user='notladi',
        password='xeno6',
        port='3308',
        database='channel_id'
    )

    # Create a cursor object
    mycursor = mydb.cursor()

    # Define the SQL query to retrieve the data you expect to be updated
    sql = "SELECT id_channel, channel_name FROM channels"

    # Execute the query
    mycursor.execute(sql)

    # Fetch all the rows returned by the query
    rows = mycursor.fetchall()

    # Check if any rows are returned
    if rows:
        print("Database has been updated.")
        # You can iterate over the rows and print or process the data as needed
        for row in rows:
            id_channel = row[0]
            channel_name = row[1]
            print(f"ID: {id_channel}, Channel Name: {channel_name}")
    else:
        print("Database has not been updated.")

    # Close the cursor and database connection
    mycursor.close()
    mydb.close()

# url = "https://www.googleapis.com/youtube/v3/videos?id=7lCDEYXw3mM&key={key} &fields=items(id,snippet(channelId,title,categoryId),statistics)&part=snippet,statistics"


# channel_id = "https://www.youtube.com/@TifoIRL"


# top_channels = pd.read_csv('most_subscribed_youtube_channels.csv')
# print(top_channels)

# top_channels['Youtuber'] = top_channels['Youtuber'].str.replace(' ','')
# print(top_channels)

# channels = top_channels['Youtuber'].to_list()

# for channel in channels:
#   channel_by_username = api.get_channel_info(for_username=channel)
#

# channel_ids = getHTML(channels)


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

from pyyoutube import Api
import json
import requests


key = "AIzaSyDDJhSQtGyf9IAlANGFVEyPh0AnbMghym4"
api = Api(api_key=key)
url = "https://www.googleapis.com/youtube/v3/videos?id=7lCDEYXw3mM&key={key} &fields=items(id,snippet(channelId,title,categoryId),statistics)&part=snippet,statistics"

# response = api.get_channel_info(channel_id="UCa-vrCLQHviTOVnEKDOdetQ")
channel_id = "https://www.youtube.com/@TifoIRL"

# response = api.get_channel_info(channel_id=channel_id)
channel_by_username = api.get_channel_info(for_username="MrBeast")

# video_by_chart = api.get_videos_by_chart(chart="mostPopular", region_code="US", count=2)
# print(video_by_chart.items)

if channel_by_username.items:  # Check if the response contains items
    # Access the channel information
    channel_info = channel_by_username.items[0]
    print(channel_info)

    id = channel_info.id
    print(id)
    channel_by_id = api.get_channel_info(channel_id=id)
    channel_dict = channel_by_id.items[0].to_dict()
    print(channel_dict)
else:
    print("No channel information found.")

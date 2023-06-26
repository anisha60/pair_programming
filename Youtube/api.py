 
from pyyoutube import Api
import json
import requests


api_key = "AIzaSyDDJhSQtGyf9IAlANGFVEyPh0AnbMghym4"
api = Api(api_key=api_key)

# response = api.get_channel_info(channel_id="UCa-vrCLQHviTOVnEKDOdetQ")
channel_id = "https://www.youtube.com/@TifoIRL"

response = api.get_channel_info(channel_id=channel_id)

if response.items:  # Check if the response contains items
    channel_info = response.items[0]
    # Access the channel information
    print(channel_info)
else:
    print("No channel information found.")
import json
import urllib.request
import string
import random
from pyyoutube import Api


count = 50
API_KEY = "AIzaSyBUSjOBc8GUMPh31WmsBvyVzW0WUMI5p6o"
random = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

urlData = "https://www.googleapis.com/youtube/v3/search?key={}&maxResults={}&part=snippet&type=video&q={}".format(
    API_KEY, count, random)
webURL = urllib.request.urlopen(urlData)
data = webURL.read()
encoding = webURL.info().get_content_charset('utf-8')
results = json.loads(data.decode(encoding))

for data in results['items']:
    videoId = (data['id']['videoId'])
    print(videoId)
    # store your ids

print(resp)
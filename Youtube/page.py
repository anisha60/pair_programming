import csv
import urllib.request
import json
import mysql.connector
import urllib.error


def check_link_working(video_id):
    url = f"https://www.youtube.com/channel/{video_id}"
    try:
        response = urllib.request.urlopen(url)
        return response.status == 200
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False


def get_channel_name(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key=YOUR_API_KEY"
    webURL = urllib.request.urlopen(url)
    data = webURL.read()
    encoding = webURL.info().get_content_charset('utf-8')
    results = json.loads(data.decode(encoding))
    channel_name = results["items"][0]["snippet"]["channelTitle"]
    return channel_name


def add_to_database(file_path, api_key):
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

    with open(file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            link = row[0]  # Assuming link is in the first column of the CSV
            video_id = link.split('=')[-1]  # Extract the video ID from the link

            if check_link_working(video_id):
                channel_name = get_channel_name(video_id)

                # Define the SQL query
                sql = "INSERT INTO channels (id_channel, channel_name) VALUES (%s, %s)"

                # Execute the query with the provided values
                val = (video_id, channel_name)
                mycursor.execute(sql, val)

                # Commit the changes to the database
                mydb.commit()

    # Close the cursor and database connection
    mycursor.close()
    mydb.close()


api_key = 'AIzaSyDDJhSQtGyf9IAlANGFVEyPh0AnbMghym4'
file_path = 'most_subscribed_youtube_channels.csv'
add_to_database(file_path, api_key)


def check_database():
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

    # Execute a query to fetch all records from the 'channels' table
    mycursor.execute("SELECT * FROM channels")

    # Fetch all the records returned by the query
    records = mycursor.fetchall()

    if len(records) > 0:
        print("Database contains the following records:")
        for record in records:
            print(record)
    else:
        print("Database is empty.")

    # Close the cursor and database connection
    mycursor.close()
    mydb.close()


# Usage example
check_database()

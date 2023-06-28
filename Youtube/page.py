import csv
import requests
import mysql.connector


def check_and_add_channel_ids(file_path):
    mydb = mysql.connector.connect(
        host='localhost',
        user='notladi',
        password='xeno6',
        port='3308',
        database='channel_id'
    )
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print("start")
            csv_reader = csv.reader(file)

            for i, row in enumerate(csv_reader):
                print("step1")
                if i >= 50:
                    print("step2")
                    break  # Stop after checking the first 20 entries

                channel_id = row[0]  # Assuming channel ID is in the first column

                try:
                    if is_channel_id_working(channel_id):
                        print("step3")
                        add_channel_to_database(channel_id, mydb)
                except Exception as e:
                    print(f"An error occurred while checking channel ID {channel_id}: {e}")
                    continue
    finally:
        print("step4")
        print("yes")


def is_channel_id_working(channel_id):
    url = f'https://www.youtube.com/channel/{channel_id}'

    response = requests.get(url)
    return response.status_code == 200


def add_channel_to_database(channel_id, mydb):
    cursor = mydb.cursor()
    query = "INSERT INTO `channel_id`.`channels` (`id_channel`) VALUES (%s)"

    try:
        cursor.execute(query, (channel_id,))
        mydb.commit()
        print(f"Added channel ID {channel_id} to the database.")
    except mysql.connector.Error as error:
        print(f"Failed to add channel ID {channel_id} to the database: {error}")

    cursor.close()


# Usag
api_key = 'AIzaSyDDJhSQtGyf9IAlANGFVEyPh0AnbMghym4'
file_path = 'most_subscribed_youtube_channels.csv'
check_and_add_channel_ids(file_path)

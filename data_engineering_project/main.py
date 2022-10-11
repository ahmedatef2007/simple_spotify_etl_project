import datetime
import sqlite3

import pandas as pd
import requests
import sqlalchemy

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
# the user id from your account
USER_ID = "31e7aw4sgllmkk45qpy4yv4us4wm"
# Spotify access token https://developer.spotify.com/console/get-recently-played/
TOKEN = "BQCwz16IKXQqDOrpLexx40ZrY7a7iJlG4z3A3gyxJHgTZB68bmiVoZaRCC7I1bQ8azvaaVNhbdvkOvVwYyXpDz2HWMpXYMQoFf-PttyJHqYDO_FJeM7GM_7ky15w-31LLVvM8mes9bWkKLpPyDNKnc1aZJff_befWJQYJr4erggSU4F_TiOiEVyhGcshKA4hrkJyzURH"


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False

        # Primary Key Check
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")


if __name__ == "__main__":

    # Extract part of the ETL process

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }
    # Convert time to Unix timestamp in miliseconds
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
    # Download all songs you've listened to "after yesterday", which means in the last 24 hours
    r = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp),
        headers=headers)

    data = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Extracting only the relevant bits of data from the json object
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    # Prepare a dictionary in order to turn it into a pandas dataframe below
    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])
    # print(song_df)

    # Validate
    if check_if_valid_data(song_df):
        print("Data valid, proceed to Load stage")
    # print(song_dict)

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")

    conn.close()
    print("Close database successfully")
    print(song_df)

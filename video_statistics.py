import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"
maxResult = 50


def get_playlistid ():
    try :
        youtube_url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        response = requests.get(youtube_url, verify= False)
        response.raise_for_status()
        data = response.json()
        channel_items = data['items'][0]
        channel_playlist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']
        #print(channel_playlist_id)
        return channel_playlist_id

    except requests.exceptions.RequestException as e:
        raise e
    
def get_video_id(playlist_id):

    video_ids = []

    page_token = None

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResult}&playlistId={playlist_id}&key={API_KEY}"

    try:
        while True:

            url = base_url

            if page_token:
                url += f"&page_token={page_token}"

            response = requests.get(url, verify= False)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

            page_token = data.get('nextPageToken')

            if not page_token:
                break

        return video_ids
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    playlist_id = get_playlistid()
    get_video_id(playlist_id)


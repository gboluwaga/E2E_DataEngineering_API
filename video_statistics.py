import requests
from datetime import date
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

def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_id_list, batch_size):
        for video in range(0, len(video_id_list), batch_size):
            yield video_id_list[video: video + batch_size]

    try:
        for batch in batch_list(video_ids, maxResult):
            video_ids_str = ",".join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=statistics&part=snippet&id={video_ids_str}&key={API_KEY}"

            response = requests.get(url, verify= False)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                content = item['contentDetails']
                statistics = item['statistics']

                video_data = {
                    "video_id":video_id,
                    "title":snippet['title'],
                    "published_date":snippet['publishedAt'],
                    "duration":content['duration'],
                    "viewcount":statistics.get('viewCount',None),
                    "likecount":statistics.get('likeCount',None),
                    "commentcount":statistics.get('commentCount',None),
                }

                extracted_data.append(video_data)

        return extracted_data
    
    except requests.exceptions.RequestException as e:
        raise e

def save_as_json_to_file_path(extracted_data):
    file_path = f"./data/youtube_data_{date.today()}.json"

    with open(file_path,"w", encoding="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    playlist_id = get_playlistid()
    video_ids = get_video_id(playlist_id)
    video_data = extract_video_data(video_ids)
    save_as_json_to_file_path(video_data)


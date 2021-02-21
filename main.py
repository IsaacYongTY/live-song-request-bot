# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os
import googleapiclient.discovery
import google_auth_oauthlib
import googleapiclient.errors
import threading
import csv

scopes = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtube"]


def authorize():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets_file.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)

    credentials = flow.run_console()

    return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)


def get_livechatid(token, url):
    youtube = token

    request = youtube.liveBroadcasts().list(
        part='snippet',
        id=url.split('/')[-1]
    )

    broadcast_response = request.execute()

    live_chat_id = broadcast_response['items'][0]['snippet']['liveChatId']
    print(live_chat_id)

    return live_chat_id

previous_page_token = ''
next_page_token = ''
bot_activate_interval = 20


class SongRequest:
    def __init__(self, author_id, song_title):
        self.author_id = author_id
        self.song_title = song_title
        self.name = None


def get_latest_message(live_chat_id):

    global next_page_token
    youtube = token

    request = youtube.liveChatMessages().list(
        liveChatId=live_chat_id,
        part="snippet",
        pageToken=next_page_token
    )

    live_chat_response = request.execute()

    messages_list = live_chat_response['items']
    channel_id_list = []
    song_request_list = []

    print(next_page_token)

    print(messages_list)
    for message in messages_list:

        word_list = message['snippet']['textMessageDetails']['messageText'].split(' ', 1)
        command = word_list[0]

        if command == '!request' and len(word_list) > 1:
            song_title = word_list[1]

            song_request = SongRequest(message['snippet']['authorChannelId'], song_title)
            song_request_list.append(song_request)

    for song_request in song_request_list:
        channel_id_list.append(song_request.author_id)

    if len(song_request_list) > 0:
        request = youtube.channels().list(
            part='snippet',
            id=','.join(channel_id_list)
        )

        channels_response = request.execute()

        for song_request in song_request_list:
            for item in channels_response['items']:
                if item['id'] == song_request.author_id:
                    song_request.name = item['snippet']['title']

        if len(word_list) > 1:
            for song_request in song_request_list:
                print(f'{song_request.song_title} is requested')

            write_to_csv(song_request_list)

    else:

        print('working but empty')

    next_page_token = live_chat_response['nextPageToken']


def set_interval(func, sec):
    def func_wrapper(live_chat_id):
        set_interval(func,sec)
        func(live_chat_id)

    t = threading.Timer(sec, func_wrapper, args=[live_chat_id])
    t.start()
    return t


def write_to_csv(song_request_list):
    with open('./song_request.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')

        for song_request in song_request_list:
            writer.writerow([song_request.song_title, song_request.name, 1])


if __name__ == '__main__':

    token = authorize()
    url = 'https://youtu.be/I_Yv5DCivw0'
    live_chat_id = get_livechatid(token, url)

    set_interval(get_latest_message, bot_activate_interval)

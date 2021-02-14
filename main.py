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


next_page_token = ''


def get_latest_message(live_chat_id, page_token):

    youtube = token

    request = youtube.liveChatMessages().list(
        liveChatId=live_chat_id,
        part="snippet",
        pageToken=page_token
    )

    response = request.execute()

    # latest_message = response['items'][-1]
    # latest_message_word_list = latest_message['snippet']['textMessageDetails']['messageText'].split(' ', 1)

    messages_list = response['items']
    channel_id_list = []
    song_title_list = []
    author_name_list = []
    global next_page_token
    next_page_token = response['items']['nextPageToken']

    for message in messages_list:

        word_list = message['snippet']['textMessageDetails']['messageText'].split(' ', 1)
        command = word_list[0]

        if command == '!request' && len(word_list) > 1:
            song_title = word_list[1]
            print('this is a command')

            channel_id_list.append(response['items']['snippet']['authorChannelId'])
            song_title_list.append(song_title)

    request = youtube.channels().list(
        part='snippet',
        id=','.join(channel_id_list)
    )

    response = request.execute()

    for item in response['items']:
        author_name_list.append(item['snippet']['title'])

    if len(word_list) > 1:
        print(f'{song_title} is requested')

        write_to_csv(song_title_list, author_name_list)


def set_interval(func, sec):
    def func_wrapper(live_chat_id,next_page_token):
        set_interval(func,sec)
        func(live_chat_id, next_page_token)

    t = threading.Timer(sec, func_wrapper, args=[live_chat_id, next_page_token])
    t.start()
    return t


def write_to_csv(song_title_list, author_name_list):
    with open('./song_request.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')

        for song_title,author in zip(song_title_list,author_name_list):
            writer.writerow(song_title, author, 1)

if __name__ == '__main__':

    token = authorize()
    url = 'https://youtu.be/I_Yv5DCivw0'
    live_chat_id = get_livechatid(token, url)

    set_interval(get_latest_message,30)

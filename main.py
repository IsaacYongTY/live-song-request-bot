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
        # broadcastStatus='upcoming',
        id=url.split('/')[-1]
    )

    broadcast_response = request.execute()

    live_chat_id = broadcast_response['items'][0]['snippet']['liveChatId']
    print(live_chat_id)

    return live_chat_id


previous_message_published_at = ''


def get_latest_message(live_chat_id):

    youtube = token

    request = youtube.liveChatMessages().list(
        liveChatId=live_chat_id,
        part="snippet"
    )

    response = request.execute()

    latest_message = response['items'][-1]
    latest_message_word_list = latest_message['snippet']['textMessageDetails']['messageText'].split(' ', 1)

    current_message_published_at = latest_message['id']

    global previous_message_published_at

    if latest_message_word_list[0][0] == '!' and previous_message_published_at != current_message_published_at:
        print('this is a command')

        if len(latest_message_word_list) > 1:
            print(f'{latest_message_word_list[1]} is requested')

            write_to_csv(latest_message_word_list[1])
            previous_message_published_at = latest_message['id']
            print(previous_message_published_at)



def test():
    print('Testing')


def set_interval(func, sec):
    def func_wrapper(live_chat_id):
        set_interval(func,sec)
        func(live_chat_id)

    t = threading.Timer(sec, func_wrapper, args=[live_chat_id])
    t.start()
    return t

def write_to_csv(song_title):
    with open('./song_request.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow([song_title, 1])

if __name__ == '__main__':

    isOn = True
    token = authorize()
    # url = input("Paste the url: ")
    url = 'https://youtu.be/0nQiXuexkK8'
    live_chat_id = get_livechatid(token, url)

    # while isOn:

    set_interval(get_latest_message,5)


        # user_choice = input("Continue? Y/N: ")

        # if user_choice == 'y':
        #     isOn = True
        # elif user_choice == 'n':
        #     isOn = False

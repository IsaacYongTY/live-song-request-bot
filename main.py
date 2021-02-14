# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os
import googleapiclient.discovery
import google_auth_oauthlib
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtube"]

def get_youtube_data():

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets_file.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)

    credentials = flow.run_console()

    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    request = youtube.liveBroadcasts().list(
        part='snippet',
        broadcastStatus='all'
    )

    broadcast_response = request.execute()

    print(broadcast_response['items'][0])


    live_chat_id = broadcast_response['items'][0]['snippet']['liveChatId']
    print(live_chat_id)

    request = youtube.liveChatMessages().list(
        liveChatId=live_chat_id,
        part="snippet"
    )

    response = request.execute()
    print(response)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_youtube_data()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

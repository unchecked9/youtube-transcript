import scrapy
import json
from ..items import TranscriptItem

import io
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaIoBaseDownload

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


class PlaylistSpider(scrapy.Spider):

    name = 'playlist'

    def __init__(self, url=None, *args, **kwargs):

        super(PlaylistSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        flow = google_auth_oauthlib.flow.InstalledAppFlow\
            .from_client_secrets_file(
                client_secrets_file,
                scopes
            )
        credentials = flow.run_console()

        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

    def parse(self, response):
        start = self.start_urls[0].find('list=') + 5
        stop = self.start_urls[0].find('&index')
        playlist_id = self.start_urls[0][start:stop]

        res = self.youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id
        ).execute()
        self.parse_video(response=res)

    def parse_video(self, response):
        data = json.loads(response.body)
        videos = data['items']
        for video in videos:
            video_id = video['contentDetails']['videoId']
            res = self.youtube.captions().list(
                part='id',
                videoId=video_id
            ).execute()
            self.parse_id(response=res)

    def parse_id(self, response):
        item = TranscriptItem()
        data = json.loads(response.body)
        for key in data['items']:
            transcript_id = key['id']
            print(transcript_id)

            request = self.youtube.captions().download(
                id=transcript_id
            )

            fh = io.FileIO('caption.txt', 'wb')
            download = MediaIoBaseDownload(fh, request)

            with open('caption.txt') as f:
                item['value'].append(f.readlines)

            complete = False
            while not complete:
                status, complete = download.next_chunk()
        yield item

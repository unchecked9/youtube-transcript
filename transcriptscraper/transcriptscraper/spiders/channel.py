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


class ChannelSpider(scrapy.Spider):

    name = 'channel'

    def __init__(self, url=None, *args, **kwargs):

        super(ChannelSpider, self).__init__(*args, **kwargs)
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
            api_service_name,
            api_version,
            credentials=credentials
        )

    def parse(self, response):

        raw_data = response.css('script::text').getall()[19]
        start = raw_data.find('items":[{"g') + 7
        stop = raw_data.find('continuations') - 2
        video_render = json.loads(raw_data[start:stop].replace('\\', ''))

        for video in video_render:
            video_id = video['gridVideoRenderer']['videoId']
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

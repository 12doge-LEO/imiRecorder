import requests, struct
import time
from typing import List, Dict
from datetime import datetime

import matplotlib

import matplotlib.pyplot as plt
import numpy as np


class RecordDownloader:
    def __init__(self):
        self.url = 'https://api.live.bilibili.com/xlive/web-room/v1/record/getLiveRecordUrl?'
        self.record_list = []
        self.platform = 'html5'
        self.reference = {
            'Referrer Policy': 'strict-origin-when-cross-origin'
        }
        self.headers = {
            'User-Agent': 'Mozilla / 5.0(WindowsNT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 87.0.4280.141 Safari / 537.36'
        }

        self.TIME_STEP = 60

    def get_recent_record_id(self):
        live_room_url = 'https://api.live.bilibili.com/xlive/web-room/v1/record/getList?room_id=22605466&page=1&page_size=20'

        response = requests.get(live_room_url, headers=self.headers, params=self.reference)

        self.record_list = response.json()['data']['list']

    def get_live_record_by_id(self, record_id):
        record_request_url = self.url + 'rid={}'.format(record_id) + '&platform=' + self.platform
        response = requests.get(record_request_url, params=self.reference)

        record_video_urls = [item['url'] for item in response.json()['data']['list']]

        for item in self.record_list:
            if item['rid'] == record_id:
                record_video_name = item['title']
        self.download_files(record_video_urls, record_video_name)

    def download_files(self, record_video_urls, record_video_name):
        for url in record_video_urls:
            file_name = './' + url.split('?')[0].split('/')[-1].replace(':', '-')
            file_name = '-'.join(file_name.split('-')[1:])
            record_video_name = record_video_name.replace(' ', '')
            record_video_name = record_video_name.replace('|', '')
            file_name = record_video_name + '-' + file_name

            response = requests.get(url, headers=self.headers, params=self.reference)
            with open(file_name, 'wb') as f:
                f.write(response.content)

    def get_dm_pool(self, rid):
        dm_data = []
        dm_url = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/getDMMsgByPlayBackID'
        index = str(0)
        for i in range(10000):
            params = {
                'rid': rid,
                'index': str(i)
            }
            try:
                response = requests.get(dm_url, headers=self.headers, params=params)
                assert response.status_code == 200
                dm_data.extend(response.json()['data']['dm']['dm_info'])
            except:
                break
        return dm_data

    def analyze_dm_by_timestamp(self, dm_data):
        def get_dm_content_and_time(_dm_data):
            _dm_content = []  # type: List[Dict]

            for temp_dm in _dm_data:
                _dm_content.append(
                    {'time': int(temp_dm['check_info']['ts'] / 1000), 'text': temp_dm['text']})
            return _dm_content

        time_dm_matrix = []
        dm_content = get_dm_content_and_time(dm_data)
        print(len(dm_content))

        max_timestamps = 0
        for item in dm_content:
            if item['time'] > max_timestamps:
                max_timestamps = item['time']

        for i in range(0, int((max_timestamps - dm_content[0]['time']) / self.TIME_STEP) + 1):
            time_dm_matrix.append(0)
        for item in dm_content:
            time_dm_matrix[int((item['time'] - dm_content[0]['time']) / self.TIME_STEP)] += 1
        return time_dm_matrix

    def draw_dm_time_map(self, data):

        x_data = [i for i in range(0, len(data))]
        y_data = data

        plt.plot(x_data, y_data, label='count', linewidth=3, color='b', marker='o',
                 markerfacecolor='blue', markersize=5)

        # 横坐标描述
        plt.xlabel('time')

        # 纵坐标描述
        plt.ylabel('count')

        # 设置数字标签
        for a, b in zip(x_data, y_data):
            plt.text(a, b, b, ha='center', va='bottom', fontsize=15)

        plt.show()


if __name__ == '__main__':
    record_downloader = RecordDownloader()
    record_downloader.get_recent_record_id()
    dm_data = record_downloader.get_dm_pool(record_downloader.record_list[0]['rid'])

    print(record_downloader.record_list[0])
    time_dm_matrix = record_downloader.analyze_dm_by_timestamp(dm_data)
    print(time_dm_matrix)
    record_downloader.draw_dm_time_map(time_dm_matrix)

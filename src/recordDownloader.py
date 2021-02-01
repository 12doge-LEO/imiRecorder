import requests
from typing import List, Dict

import matplotlib.pyplot as plt


class Record:
    def __init__(self, name='', rid='', date='', urls=[], cover_url='', start_timestamp=0, end_timestamp=0):
        self.name = name
        self.date = date
        self.rid = rid

        self.urls = urls  # type: List[str]
        self.cover_url = cover_url

        self.raw_dm = []
        self.analyzed_dm = []

        self.reference = {
            'Referrer Policy': 'strict-origin-when-cross-origin'
        }
        self.headers = {
            'User-Agent': 'Mozilla / 5.0(WindowsNT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                          '87.0.4280.141 Safari / 537.36 '
        }

        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp

    def download(self):
        for url in self.urls:
            file_name = './' + url.split('?')[0].split('/')[-1].replace(':', '-')
            file_name = '-'.join(file_name.split('-')[1:])
            record_video_name = self.name.replace(' ', '')
            record_video_name = record_video_name.replace('|', '')
            file_name = record_video_name + '-' + file_name

            response = requests.get(url, headers=self.headers, params=self.reference)
            with open(file_name, 'wb') as f:
                f.write(response.content)

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


class RecordDownloader:
    def __init__(self):
        self.url = 'https://api.live.bilibili.com/xlive/web-room/v1/record/getLiveRecordUrl?'

        self.live_room_url = 'https://api.live.bilibili.com/xlive/web-room/v1/record/getList?room_id=22605466&page=1' \
                             '&page_size=20 '
        self.record_list = []
        self.platform = 'html5'
        self.reference = {
            'Referrer Policy': 'strict-origin-when-cross-origin'
        }
        self.headers = {
            'User-Agent': 'Mozilla / 5.0(WindowsNT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / '
                          '87.0.4280.141 Safari / 537.36 '
        }

        self.TIME_STEP = 300

    def get_recent_record_id(self):
        self.live_room_url = 'https://api.live.bilibili.com/xlive/web-room/v1/record/getList?room_id=22605466&page=1' \
                             '&page_size=5 '

        response = requests.get(self.live_room_url, headers=self.headers, params=self.reference)

        self.record_list = response.json()['data']['list']

    def get_live_record_by_id(self, record_id):
        record_request_url = self.url + 'rid={}'.format(record_id) + '&platform=' + self.platform
        response = requests.get(record_request_url, params=self.reference)

        record_video_urls = [item['url'] for item in response.json()['data']['list']]

        return record_video_urls
        # self.download_files(record_video_urls, record_video_name)

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

    def get_dm_pool(self, rid, total_time):
        dm_data = []
        dm_url = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/getDMMsgByPlayBackID'
        for i in range(0, int(total_time / 3)):
            if i % 10 == 0 or i == int(total_time / 3) - 1:
                print('Getting DM index : {}/{}'.format(i, int(total_time / 3)))
            params = {
                'rid': rid,
                'index': str(i)
            }
            response = requests.get(dm_url, headers=self.headers, params=params)
            assert response.status_code == 200
            try:
                dm_data.extend(response.json()['data']['dm']['dm_info'])
            except:
                print('Error: dm get failed')
                continue
        return dm_data

    def create_record_instance(self, max_count=3):
        temp_record_list = []
        count = 0
        for record in self.record_list:
            temp_record = Record(rid=record['rid'], urls=self.get_live_record_by_id(record['rid']),
                                 name=record['title'], cover_url=record['cover'],
                                 start_timestamp=record['start_timestamp'], end_timestamp=record['end_timestamp'])
            print('Creating record instance: ' + str(temp_record.name))
            temp_record.raw_dm = self.get_dm_pool(temp_record.rid,
                                                  (temp_record.end_timestamp - temp_record.start_timestamp) / 60)
            print('Begin DM analysis...')
            temp_record.analyzed_dm = self.analyze_dm_by_timestamp(temp_record.raw_dm)
            print('DM instance created')
            temp_record_list.append(temp_record)
            count += 1
            if count >= max_count:
                break
        return temp_record_list

    def analyze_dm_by_timestamp(self, dm_data):
        def get_dm_content_and_time(_dm_data):
            _dm_content = []  # type: List[Dict]

            for temp_dm in _dm_data:
                _dm_content.append(
                    {'time': int(temp_dm['check_info']['ts'] / 1000), 'text': temp_dm['text']})
            return _dm_content

        time_dm_matrix = []
        dm_content = get_dm_content_and_time(dm_data)

        max_timestamps = 0
        for item in dm_content:
            if item['time'] > max_timestamps:
                max_timestamps = item['time']
        try:

            for i in range(0, int((max_timestamps - dm_content[0]['time']) / self.TIME_STEP) + 1):
                time_dm_matrix.append(0)
            for item in dm_content:
                time_dm_matrix[int((item['time'] - dm_content[0]['time']) / self.TIME_STEP)] += 1
        except:
            print('Dm data error, please check raw dm data')
        return time_dm_matrix

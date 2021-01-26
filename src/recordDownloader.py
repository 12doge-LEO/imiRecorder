import requests, struct
from typing import List


class RecordDownloader:
    def __init__(self):
        self.url = 'https://api.live.bilibili.com/xlive/web-room/v1/record/getLiveRecordUrl?'
        self.record_id = 'R1gx411w7EX'
        self.platform = 'html5'
        self.reference = {
            'Referrer Policy': 'strict-origin-when-cross-origin'
        }

        self.record_video_urls = []  # type: List[str]

    def get_live_record_url(self):
        record_request_url = self.url + 'rid={}'.format(self.record_id) + '&platform=' + self.platform
        print(record_request_url)
        response = requests.get(record_request_url, params=self.reference)

        self.record_video_urls = [item['url'] for item in response.json()['data']['list']]

    def download_files(self):
        for url in self.record_video_urls:
            headers = {
                'User-Agent': 'Mozilla / 5.0(WindowsNT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 87.0.4280.141 Safari / 537.36'
            }
            file_name = './'+url.split('?')[0].split('/')[-1].replace(':','-')
            response = requests.get(url, headers=headers, params=self.reference)


            with open(file_name, 'wb') as f:
                f.write(response.content)



if __name__ == '__main__':
    record_downloader = RecordDownloader()
    record_downloader.get_live_record_url()
    record_downloader.download_files()

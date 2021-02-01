from src.recordDownloader import Record, RecordDownloader
from src.email_sender import EmailSender


from datetime import datetime
import time

from typing import List

if __name__ == '__main__':
    record_list = []  # type: List[Record]
    record_downloader = RecordDownloader()

    record_downloader.get_recent_record_id()
    record_list.extend(record_downloader.create_record_instance())

    email_sender = EmailSender()
    for record in record_list:
        print('Begin to send email, title: '+ str(record.name)
              )
        email_sender.data_builder(subject=record.name,date=str(datetime.fromtimestamp(record.start_timestamp)))
        email_sender.send_mail()
        print('Send successfully')



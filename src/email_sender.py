import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import email
from email import encoders
import base64


class EmailSender:
    def __init__(self):
        self.smtp_server = 'smtp.163.com'
        self.username = 'doge12bot@163.com'
        self.password = 'OQSKSEISPZVTHEMK'

        self.sender = 'doge12bot@163.com'

        self.receiver = 'doge12bot@163.com'

        self.msg = MIMEMultipart('mixed')

    def data_builder(self, subject='', date='', files=''):
        self.msg = MIMEMultipart('mixed')
        self.msg['Subject'] = subject
        self.msg['From'] = 'doge12bot@163.com <dobe12bot@163.com>'
        self.msg['To'] = 'liusiruigood@gmail.com'
        self.msg['Date'] = date
        for file_path in files:
            with open(file_path, 'rb') as fp:
                attach = MIMEBase('application', 'octet-stream')
                attach.set_payload(fp.read())
                attach.add_header('Content-Disposition', 'attachment', filename=str(file_path))
                encoders.encode_base64(attach)
                self.msg.attach(attach)

    def send_mail(self):
        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com')

        smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, self.receiver, self.msg.as_string())
        smtp.quit()

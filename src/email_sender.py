import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class EmailSender:
    def __init__(self):
        self.smtp_server = 'smtp.163.com'
        self.username = 'doge12bot@163.com'
        self.password = 'OQSKSEISPZVTHEMK'

        self.sender = 'doge12bot@163.com'

        self.receiver = 'doge12bot@163.com'

        self.msg = MIMEMultipart('mixed')

    def data_builder(self,subject='',date=''):
        self.msg = MIMEMultipart('mixed')
        self.msg['Subject'] = subject
        self.msg['From'] = 'doge12bot@163.com <dobe12bot@163.com>'
        self.msg['To'] = 'liusiruigood@gmail.com'
        self.msg['Date'] = date

    def send_mail(self):
        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com')
        # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
        # smtp.set_debuglevel(1)
        smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, self.receiver, self.msg.as_string())
        smtp.quit()

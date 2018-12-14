# -*- coding:utf-8 -*-
import os
import smtplib
from config import setting
from lib.public import logger
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendMail(object):

    def __init__(self, filename, receiver=None, mode='rb'):
        self.filename = os.fspath(filename)
        self.baseFilename = os.path.abspath(filename)
        # The recipient, list type, can be reassigned,
        # and if the recipient list is empty, the default sender is the receiver.
        if receiver is None:
            if isinstance(parameters.EMAILS['default']['receivers'], list):
                if len(parameters.EMAILS['default']['receivers']) < 1:
                    self.receiver = parameters.EMAILS['default']['sender_name']
                else:
                    self.receiver = parameters.EMAILS['default']['receivers']
        else:
            self.receiver = receiver
        self.mode = mode
        self.msg = MIMEMultipart()

    @property
    def get_report(self) -> str:
        try:
            dirs = os.listdir(self.filename)
            if dirs is not None:
                dirs.sort()
                new_report = dirs[-1]
                print('Latest test generated reports {0}'.format(new_report))
                return new_report
            else:
                print('This directory {0} is empty'.format(dirs))
        except Exception:
            print('The directory was not found。')
            raise

    # 邮件附件与内容
    def take_content(self):
        new_report = os.path.join(self.filename, self.get_report)
        self.msg['Subject'] = Header('SEM AUTO TEST REPORT', 'utf-8')
        with open(new_report, self.mode) as file:
            mail_body = file.read()
        self.msg.attach(MIMEText(mail_body, _subtype='html', _charset='utf-8'))
        att = MIMEText(mail_body, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="report.html"'
        self.msg.attach(att)

    # Flag为True 邮件发送
    def send_mail(self, flag: 'default Boolean False'=False):
        if flag:
            self.take_content()
            self.msg['From'] = parameters.EMAILS['default']['sender_name']
            self.msg['To'] = ','.join(self.receiver)
            server = smtplib.SMTP_SSL('smtp.qq.com', 465)
            try:
                server.login(parameters.EMAILS['default']['sender_name'], parameters.EMAILS['default']['sender_psw'])
                server.sendmail(parameters.EMAILS['default']['sender_name'], self.receiver, self.msg.as_string())
                print('{0} Please check if the email has been sent successfully.'
                      .format(parameters.EMAILS['default']['receivers']))
            except Exception:
                print('Mailbox sending failed, please check the parameters of each setting.')
                raise
            finally:
                server.quit()


if __name__ == '__main__':

    print(parameters.EMAILS['default']['filename'])
    send = SendMail(parameters.EMAILS['default']['filename'])
    print(send.get_report)
    send = SendMail(parameters.EMAILS['default']['filename'])
    send.send_mail(flag=True)

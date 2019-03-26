# -*- coding:utf-8 -*-
"""
@Author: Null
@File: excel_handler.py
@description: 发送Eamil邮件
"""
import smtplib
from lib.utils import fp
from config import setting
from lib.public import logger
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendMail(object):

    def __init__(self, receiver=None, mode='rb'):
        # The recipient, list type, can be reassigned,
        # and if the recipient list is empty, the default sender is the
        # receiver.
        if receiver is None:
            if isinstance(setting.EMAIL_CONF['receivers'], list):
                if len(setting.EMAIL_CONF['receivers']) < 1:
                    self.receiver = setting.EMAIL_CONF['sendaddr_name']
                else:
                    self.receiver = setting.EMAIL_CONF['receivers']
        else:
            self.receiver = receiver
        self.mode = mode
        self.msg = MIMEMultipart()

    @property
    def get_html_report(self) -> str:
        """
        获取测试报告路径

        :Usage:
            get_html_report()
        """
        try:
            return setting.REPORT_PATH + 'HighTalkReport.html'
        except FileNotFoundError:
            pass

    def email_content(self) -> None:
        """
        定义发送邮件的内容

        :Usage:
            email_content()
        """
        self.msg['Subject'] = Header('SEM AUTO TEST REPORT', 'utf-8')
        with open(setting.EMAIL_TEMPLATE_PATH, self.mode) as file:
            mail_body = file.read()
        self.msg.attach(MIMEText(mail_body, _subtype='html', _charset='utf-8'))
        att1 = MIMEText(open(self.get_html_report, self.mode).read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="report.html"'
        self.msg.attach(att1)
        att2 = MIMEText(open(fp.iter_files(setting.LOG_PATH)[-1], self.mode).read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = 'attachment; filename="mar.log"'
        self.msg.attach(att2)

    def send_mail(self):
        self.email_content()
        self.msg['From'] = setting.EMAIL_CONF['sendaddr_name']
        self.msg['To'] = ','.join(self.receiver)
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        try:
            server.login(
                setting.EMAIL_CONF['sendaddr_name'],
                setting.EMAIL_CONF['sendaddr_pswd'])
            server.sendmail(
                setting.EMAIL_CONF['sendaddr_name'],
                self.receiver,
                self.msg.as_string())
            logger.log_debug(
                'Please check if the email has been sent successfully.')
        except smtplib.SMTPException:
            pass
        finally:
            server.quit()


if __name__ == '__main__':
    pass

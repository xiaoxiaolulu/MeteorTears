# -*- coding:utf-8 -*-
import smtplib
from lib.utils import fp
from config import setting
from lib.public import logger
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from lib.utils import resvalues


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
        self.cons = open(setting.EMAIL, encoding='utf-8')
        self.con = self.cons.read()

    def make_email_template(self):
        r"""将各测试数据写入测试邮件模板
        """
        content, cases_table = resvalues.get_report_values(), resvalues.write_cases_result()
        with open(setting.REPORT + 'email', 'w', encoding='utf-8') as file:
            file.write(self.con.format(content[0], content[1],  content[2], content[3], cases_table))

    @property
    def get_html_report(self) -> str:
        r"""获取测试报告路径

        :Usage:
            get_html_report()
        """
        try:
            return setting.REPORT + 'Report.html'
        except FileNotFoundError:
            pass

    def email_content(self) -> None:
        r"""定义发送邮件的内容

        :Usage:
            email_content()
        """
        self.msg['Subject'] = Header('SEM AUTO TEST REPORT', 'utf-8')
        self.make_email_template()
        with open(setting.REPORT + 'email', self.mode) as file:
            mail_body = file.read()
        self.msg.attach(MIMEText(mail_body, _subtype='html', _charset='utf-8'))
        att1 = MIMEText(open(self.get_html_report, self.mode).read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="report.html"'
        self.msg.attach(att1)
        att2 = MIMEText(open(fp.iter_files(setting.LOG)[-1], self.mode).read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = 'attachment; filename="MyApiTest.log"'
        self.msg.attach(att2)

    def send_mail(self):
        r"""发送测试报告邮件
        """
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
        except smtplib.SMTPException as error:
            logger.log_warn(error)
        finally:
            server.quit()

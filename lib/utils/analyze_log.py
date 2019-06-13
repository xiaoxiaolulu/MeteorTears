# -*- coding:utf-8 -*-
import yaml
import json
import re
import os
import requests
from lib.public import logger
from config import setting


class WeChatAlarm(object):

    WeChat = {}
    with open(setting.WECHAT, 'r', encoding='utf-8') as file:
        WeChat.update(yaml.safe_load(file)['wechat'])

    @property
    def log_file(self) -> str:
        r"""获取最新的日志文件

        :Usage:
            log_file()
        """
        log_list = os.listdir(setting.LOG)
        log_list.sort()
        return log_list[-1]

    def analyze_files(self) -> list:
        r"""分析日志信息，提取存在错误的信息

        :Usage:
            analyze_files()
        """
        error_message = []
        with open(setting.LOG + self.log_file, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                er, wr = re.compile(r'ERROR.*'), re.compile(r'WARN.*')
                if er.findall(line) or wr.findall(line):
                    error_message.append(line)
        return error_message

    def error_log_message(self) -> str:
        r"""拼接错误信息

        :Usage:
            error_log_message()
        """
        msg = '' + '\n'
        for value in self.analyze_files():
            msg += value
        return msg

    @classmethod
    def get_token(cls) -> str:
        r"""获取微信公众号token信息

        :Usage:
            get_token()
        """
        token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s' \
                    % (cls.WeChat['corp'], cls.WeChat['secret'])
        response = requests.get(token_url, verify=True).text
        response_dict = json.loads(response)
        token = response_dict['access_token']
        return token

    @classmethod
    def send_message(cls, message: str) -> None:
        r"""发送错误的日志信息给企业微信

        :Args:
         - message: 错误的日志信息, str object.
        """
        send_url = (' https://qyapi.weixin.qq.com/cgi-bin/message/send?'
                    'access_token={}'.format(cls.get_token()))
        post_data = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": 1000002,
            "text": {
                "content": message
            },
            "safe": 0
        }
        res = requests.post(send_url, data=json.dumps(post_data), verify=True)
        logger.log_info("The Push WeChat message result is {}".format(
            json.dumps(res.json(), indent=4, ensure_ascii=False))
        )


if __name__ == '__main__':
    pass

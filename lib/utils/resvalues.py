import re
import os
from requests_html import HTMLSession
from requests_file import FileAdapter
from config import setting


def get_report_values():
    """
    获取测试报告中的数据值，用于传参与email中的数据统计
    :return:
    """
    session = HTMLSession()
    session.mount('file://', FileAdapter())
    filepath = (os.path.join(setting.BASE_DIR, setting.REPORT, 'Report.html')).replace("\\", "/")
    html_obj = session.get(f'file:///{filepath}')
    test_pass_pattern = re.findall('"testPass": \d+,', html_obj.html.text)[0].split(':')[1].replace(',', '')
    test_all_pattern = re.findall('"testAll": \d+,', html_obj.html.text)[0].split(':')[1].replace(',', '')
    test_fail_pattern = re.findall('"testFail": \d+,', html_obj.html.text)[0].split(':')[1].replace(',', '')
    test_skip_pattern = re.findall('"testSkip": \d+,', html_obj.html.text)[0].split(':')[1].replace(',', '')
    return test_all_pattern, test_pass_pattern, test_fail_pattern, test_skip_pattern

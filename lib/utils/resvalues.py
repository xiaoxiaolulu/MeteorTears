import re
import os
import types
from requests_html import HTMLSession
from requests_file import FileAdapter
from lib.public.load_cases import LoadCase
from lib.public.Recursion import GetJsonParams
from config import setting


def get_report_values() -> tuple:
    r"""获取测试报告中的数据值，用于传参与email中的数据统计
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


def case_values() -> types.GeneratorType:
    r"""获取测试用例中的基准数据，用于数据统计
    """
    LD = LoadCase(setting.CASES)
    tags = LD.load_files()
    for items in tags:
        for class_name, body in items.items():
            for key, value in body.items():
                func_name = key
                description = GetJsonParams.get_value(value, 'description')
                method = GetJsonParams.get_value(value, 'method')
                url = GetJsonParams.get_value(value, 'url')
                yield {
                    'class_name': class_name,
                    'func_name': func_name,
                    'description': description,
                    'url': url,
                    'method': method
                }


def get_cases_content_list() -> list:
    r"""返回测试用例数据，以list的形式返回
    :rtype: list object.
    """
    cases_content_list = []
    for case_content in iter(case_values()):
        cases_content_list.append(case_content)
    return cases_content_list


HTML_BASE_TEMPLATE = """
    <tr>
        <td>
            <table align="center" border="1" cellpadding="0" cellspacing="0" width="700" style="border-bottom: 1px solid #ddd;border-left: 1px solid #ddd;border-right: 1px solid #ddd;padding: 20px;background-color: #fff;color: #555;font-size: 10px;line-height: 1.7;">
                <tr>
                    <th>Id</th>
                    <th>TestSuite</th>
                    <th>TestCase</th>
                    <th>Description</th>
                    <th>Url</th>
                    <th>Method</th>
                </tr>
                {}
            </table>
        </td>
    </tr>
"""


HTML_TABLE_TEMPLATE = """
                <tr>
                    <th>{}</th>
                    <th>{}</th>
                    <th>{}</th>
                    <th>{}</th>
                    <th>{}</th>
                    <th>{}</th>
                </tr>
"""


def write_cases_result() -> str:
    r"""将测试用例中基准数据生成表格HTML
    """

    cases_result_template = ''
    for index, value in enumerate(get_cases_content_list()):
        class_name = value['class_name']
        func_name = value['func_name']
        description = value['description']
        url = value['url'].split('$')[-1]
        method = value['method']
        cases_result_template += HTML_TABLE_TEMPLATE.format(
            (index + 1), class_name, func_name, description, url, method
        )
    return HTML_BASE_TEMPLATE.format(cases_result_template)

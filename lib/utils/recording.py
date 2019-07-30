# -*- coding:utf-8 -*-
import yaml
import json
import click
from os import path
from urllib.parse import unquote


def loads_recording_file_content(filepath: str):
    r"""加载抓包工具保存的文件并获取request数据

    :Args:
     - filepath: 录制文件路径地址, str object.
    """
    if path.exists(filepath):
        with open(filepath, "r+", encoding="utf-8") as f:
            try:
                content_json = json.loads(f.read())
                return content_json["log"]["entries"]
            except (KeyError, TypeError):
                pass


RECORDING_CONTENT = lambda path: loads_recording_file_content(path)


def _method(filepath: str) -> str:
    r"""抓包保存的录制文件中的request-method元素
    
    :Args:
     - filepath: 录制文件路径地址, str object.
    """
    return RECORDING_CONTENT(filepath)[0]['request']['method']


def _url(filepath: str) -> str:
    r"""抓包保存的录制文件中的request-url元素
    
    :Args:
     - filepath: 录制文件路径地址, str object.
    """
    return RECORDING_CONTENT(filepath)[0]['request']['url']


def _params(filepath: str) -> dict:
    r"""抓包保存的录制文件中的request-params元素
    
    :Args:
     - filepath: 录制文件路径地址, str object.
    """
    request_data = RECORDING_CONTENT(filepath)[0]['request'].get("postData", {})
    if _method(filepath) in ['POST']:
        return {
            'json': json.loads(request_data.get("text"))
        }
    else:
        if _url(filepath).find('?'):
            return {}
        else:
            params = RECORDING_CONTENT(filepath)[0]['request'].get('queryString', [])
            post_data = {
                item["name"]: item.get("value")
                for item in params
            }
            if isinstance(post_data, dict):
                converted = []
                for key, value in post_data.items():
                    converted.append('{}={}'.format(key, value))
                return {
                    'params': '&'.join(converted)
                }


def _headers(filepath: str) -> dict:
    r"""抓包保存的录制文件中的request-headers元素

    :Args:
     - filepath: 录制文件路径地址, str object.
    """
    origin_list = RECORDING_CONTENT(filepath)[0]['request']['headers']
    return {
        item["name"]: item.get("value")
        for item in origin_list
    }


def _status_code(filepath: str) -> int:
    r"""抓包保存的录制文件中的response-status_code元素

    :Args:
     - filepath: 录制文件路径地址, str object.
    """
    return RECORDING_CONTENT(filepath)[0]['response']['status']


def generate_case_data(filepath: str, func_name: str, func_path: str) -> None:
    r"""生成.yaml的测试用例.

    :Args:
     - filepath: 录制文件路径地址, str object.
     - func_name: 用例名称&用例描述, str object.
     - func_path: 用例保存路径, str object.
    """
    request_body = dict(
        {
            'relevant_parameter': [],
            'relevant_sql': [],
            'skip': False,
            'description': func_name,
            'method': _method(filepath),
            'url': _url(filepath),
            'timeout': 8,
            'headers': _headers(filepath),
            'res_index': [],
            'assert': {
                'status_code': _status_code(filepath)
            }
        },
        **_params(filepath)
    )
    func_body = {
        func_name: request_body
    }
    with open(path.join(func_path, func_name + '.yaml'), 'w', encoding='utf-8') as file:
        yaml.dump(func_body, file, allow_unicode=True, default_flow_style=False, indent=4)
        print('录制的接口文件生成用例成功 -> {}'.format(path.join(func_path, func_name + '.yaml')))


@click.command()
@click.option('--r', default=None, help="recording file path")
@click.option('--n', default=None, help="test case func name")
@click.option(
    '--p',
    default=None,
    help="generate test case in path")
def main(r: str, n: str, p: str) -> None:
    r"""接口录制模块命令行运行主入口

    :Arg:
     - r:  抓包工具保存下来的接口录制源文件, str object.
     - n:  生成用例的名称以及用例描述, str object.
     - p:  生成接口用例存放路径, str object.
    """
    generate_case_data(r, n, p)


if __name__ == '__main__':
    main()

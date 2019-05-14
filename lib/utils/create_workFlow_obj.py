# -*- coding:utf-8 -*-
import json
from config import setting
from lib.utils.load_fiddler_files import LoadFiddlerFiles

LD = LoadFiddlerFiles(setting.Recording)


class CreateJsonCaseObj(object):

    def __init__(self, path: str = None):
        self.path = path

    @staticmethod
    def make_json_case_object() -> None:
        """
        将录制用例转化为JSON格式的用例对象

        :Usage:
            make_json_create_object()
        """
        for dic in iter(LD.loads_fiddler_request()):
            filename = dic['class_name'].lower()
            case_obj = {
                'test.json' + '_' + filename: {
                    "url": dic['request_url'],
                    "method": dic['request_type'],
                    "data": dic['request_body'],
                    "headers": dict({'Authorization': dic['authorization']}, **{'Content-Type': dic['content_type']}),
                    "description": filename,
                    "assert": {
                        "code": 0
                    }
                }
            }
            try:
                with open(setting.WORK_FLOW + filename + '.json', 'w', encoding='utf-8') as file:
                    file.write(json.dumps(case_obj, indent=4, ensure_ascii=False))
            except OSError:
                continue


if __name__ == '__main__':
    pass

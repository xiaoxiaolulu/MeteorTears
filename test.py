"""测试代码"""
import yaml
from lib.public.Recursion import GetJsonParams
_custom_fail = {}
with open('test.yaml', 'r', encoding='utf-8') as file:
    _custom_fail.update(yaml.load(file))
# _relevance = {}
# with open(r'F:\MeteorTears\res\Access-Token.yaml', 'r', encoding='utf-8') as file:
#     _relevance.update(yaml.load(file))
from lib.utils import relevance
# temp = ('Access-Token', )
# _custom_fail = GetJsonParams.for_keys_to_dict(*temp, my_dict=_custom_fail)
# print(_custom_fail['Access-Token'])
# _custom_fail = "${Access-Token}$"
_relevance = {"Access-Token": "C5FC812291A42ED477D1FBAC27E199F6DDF5F440C352E623CFB303EE027B4A9E"}
print(relevance.custom_manage(str(_custom_fail), _relevance))
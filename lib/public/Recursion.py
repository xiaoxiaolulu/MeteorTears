# -*- coding:utf-8 -*-


class GetJsonParams(object):

    @classmethod
    def get_value(cls, my_dict: dict, key: str) -> str:
        r"""解析一个嵌套字典，并获取指定key的值

        :Args:
         - my_dict: 解析的字典,  dict object.
         - key: 指定解析的键,  str object.

        :Usage:
            get_value({'hello': 'world'}, 'hello')
        """

        if isinstance(my_dict, dict):
            if my_dict.get(key) or my_dict.get(key) == 0 or my_dict.get(key) == '' \
                    and my_dict.get(key) is False or my_dict.get(key) == []:
                return my_dict.get(key)

            for my_dict_key in my_dict:
                if cls.get_value(my_dict.get(my_dict_key), key) or \
                        cls.get_value(my_dict.get(my_dict_key), key) is False:
                    return cls.get_value(my_dict.get(my_dict_key), key)

        if isinstance(my_dict, list):
            for my_dict_arr in my_dict:
                if cls.get_value(my_dict_arr, key) \
                        or cls.get_value(my_dict_arr, key) is False:
                    return cls.get_value(my_dict_arr, key)

    @classmethod
    def get_same_content(cls, my_dict: dict, list_key: str, list_index: int, same_key: str) -> str:
        r"""解析一个嵌套字典中存在相同key的情况

        :Arg:
         - my_dict: 需要解析的字典, dict object.
         - list_key: 相同key存在的数组, str object.
         - list_index: 取数组中第几个个字典, int object.
         - same_key: 需要取值的KEY值, str object.

        :Usage:
            get_same_content(my_dict=my_dict, list_key='datalist', list_index=0, same_key='botName')
        """
        return dict(cls.get_value(my_dict=my_dict, key=list_key)[list_index])[same_key]

    @classmethod
    def for_keys_to_dict(cls, *args: tuple, my_dict: dict) -> dict:
        r"""指定多个key，并获取一个字典的多个对应的key，组成一个新的字典

        :Arg:
         - args: 指定的key值, tuple object.
         - my_dict: 解析的字典, dict object.

        :Usage:
            for_keys_to_do_dict('hello', {'hello': 'hello'})
        """
        result = {}
        if len(args) > 0:
            for key in args:
                result.update({key: cls.get_value(my_dict, str(key))})
        return result

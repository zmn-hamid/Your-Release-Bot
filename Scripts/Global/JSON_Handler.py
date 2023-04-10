'''
    # handle any job with JSON/JSON-serilizable objects
'''

import json
from typing import *


class CJson:
    '''
        ## Automate some works with JSON files / JSON-serializable objects
    '''

    @staticmethod
    def jsonize_filename(filename: str):
        '''## check if object is json serializable'''
        return filename if filename.endswith('.json') else filename+'.json'

    @staticmethod
    def loads(filename: str):
        '''
            ## loads the data from a JSON file
            - applies `.json` in the end
        '''
        with open(CJson.jsonize_filename(filename), encoding='utf-8') as f:
            return json.loads(foo if (foo := f.read().strip()) != '' else '{}')

    @staticmethod
    def dumps(data, filename: str) -> str:
        '''
            ## dump the data into a JSON file
            - applies `.json` in the end
        '''
        with open(CJson.jsonize_filename(filename), 'w', encoding='utf-8') as f:
            f.write(CJson.get_text(data))
        return filename

    @staticmethod
    def get_text(data) -> str:
        '''
            ## converts JSON-serializable objects to string
            - it returns a formatted JSON object
        '''
        return json.dumps(data, indent=4, ensure_ascii=False).encode('utf8').decode()

    @staticmethod
    def print(data):
        '''## print the output of `CJson.get_text`'''
        print(CJson.get_text(data))

    @staticmethod
    def _copy_list(list_obj: list, new_list: list):
        '''
            ### copies a list
            - <b>DO NOT</b> use directly. use `CJson.copy_list` instead
        '''
        for item in list_obj:
            match type(item).__name__:
                case list.__name__ | tuple.__name__:
                    item = CJson._copy_list(list_obj=item, new_list=[])
                case dict.__name__:
                    item = CJson._copy_dict(dict_obj=item, new_dict={})
            new_list.append(item)
        return new_list

    def copy_list(list_obj: list):
        '''
            ## copies a list fully
        '''
        return CJson._copy_list(list_obj=list_obj, new_list=[])

    @staticmethod
    def _copy_dict(dict_obj: dict, new_dict: dict):
        '''
            ### copies a dict
            - <b>DO NOT</b> use directly. use `CJson.copy_dict` instead
        '''
        for key, value in dict_obj.items():
            match type(value).__name__:
                case list.__name__ | tuple.__name__:
                    value = CJson._copy_list(list_obj=value, new_list=[])
                case dict.__name__:
                    value = CJson._copy_dict(dict_obj=value, new_dict={})
            new_dict[key] = value
        return new_dict

    @staticmethod
    def copy_dict(dict_obj: list):
        '''
            ## copies a dict
        '''
        return CJson._copy_dict(dict_obj=dict_obj, new_dict={})

    @staticmethod
    def copy_obj(obj: list):
        '''
            ## copies a obj
            - determines the type itself
        '''
        match type(obj).__name__:
            case list.__name__ | tuple.__name__:
                return CJson.copy_list(list_obj=obj)
            case dict.__name__:
                return CJson.copy_dict(dict_obj=obj)
        return obj

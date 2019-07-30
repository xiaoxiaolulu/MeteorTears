# -*- coding:utf-8 -*-


class JsonLoadingError(Exception):
    pass


class TestApiMethodError(Exception):
    pass


class CaseYamlFileNotFound(FileNotFoundError, FileExistsError):
    pass


class SubInheritCaseParamsKwargs(TypeError, KeyError):
    pass

# -*- coding:utf-8 -*-
import base64


def encrypt(key: bytes)-> bytes:
    """
    加密

    :Arg:
     - key: 加密的字符串, STR TYPE.

    :Usage:
        encrypt(b'hello')
    """
    if isinstance(key, (bytearray, bytes)):
        return base64.b64encode(key)
    else:
        try:
            bytes_obj = bytes(key, encoding='utf-8')
            return base64.b64encode(bytes_obj)
        except TypeError:
            raise TypeError("argument should be a bytes-like object"
                            "not %r" % key.__class__.__name__) from None


def decryption(key: bytes) -> str:
    """
    解密

    :Args:
     - key: 解密的字符串, STR TYPE.

    :Usage:
        decryption(b'NTQ2NDY0MjY4QHFxLmNvbQ==')
    """
    if isinstance(key, (bytearray, bytes)):
        return str(base64.b64decode(key), encoding='utf-8')
    else:
        try:
            bytes_obj = bytes(key, encoding='utf-8')
            return str(base64.b64decode(bytes_obj), encoding='utf-8')
        except TypeError:
            raise TypeError("argument should be a bytes-like object"
                            "not %r" % key.__class__.__name__) from None

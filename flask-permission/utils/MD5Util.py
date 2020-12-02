import hashlib


# 用于 MD5 加密
def md5vale(key):
    input_name = hashlib.md5()
    input_name.update(key.encode("utf-8"))
    return input_name.hexdigest()

# 统一返回格式、自定义异常
import fastapi.responses


# 统一返回格式
def resp_ok(data=None, msg="成功"):
    return {
        "code": 200,
        "msg": msg,
        "data": data
    }


def resp_fail(code=400, msg="失败"):
    return {
        "code": code,
        "msg": msg,
        "data": None
    }

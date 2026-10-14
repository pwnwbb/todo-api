# Pydantic模型
from pydantic import BaseModel


class TodoCreat(BaseModel):  # 创造一个DotoCreat类，接收前端传过来的数据
    content: str  # 校验字符串
    is_done: bool  # 布尔值，默认 `False`


class TodoOut(TodoCreat):   # 返回
    id: int

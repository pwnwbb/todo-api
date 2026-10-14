# 入口，路由注册
import redis
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from models import TodoDB
from database import engine, Base, get_db
from schemas import TodoOut, TodoCreat
from redis_client import redis_client
from utils import resp_ok, resp_fail
import json

# 自动在mysql创建表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo缓存Demo项目")


@app.get("/")
async def root():
    return resp_ok(msg="项目启动成功！访问 /docs 看接口文档")


# 新增todo
@app.post("/todos", response_model=TodoOut)
async def creat_todo(todo: TodoCreat, db: Session = Depends(get_db)):
    # 构建ORM对象
    db_todo = TodoDB(content=todo.content, is_done=todo.is_done)
    # sqlalchemy增操作
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)  # 刷新，拿到数据库自增id

    # global next_id
    # new_todo = {
    #     "id": next_id,
    #     "content": todo.content,
    #     "is_done": todo.is_done
    # }
    # todo.append(new_todo)
    # next_id += 1

    # 新增之后，清空缓存，让下次查询重新缓存最新5条
    redis_client.delete("latest_5_todo")
    return resp_ok(data=db_todo, msg="任务创建成功")

    # 获取最近5条todo，走Redis缓存
    # @app.get("/todos/latest5")
    # async def get_latest5(cache_data=None, todo_db=None):
    #     cache = redis_client.get("latest_5_todo")
    #     if cache_data:  # 命中缓存，直接返回
    #         return resp_ok(data=json.loads(cache_data), msg="读取缓存成功")


@app.get("/todos/latest5")
async def get_latest5(db: Session = Depends(get_db)):
    cache = redis_client.get("latest_5_todo")
    if cache:
        return resp_ok(data=json.loads(cache), msg="命中Redis缓存")

    # 没命中，从模拟db拿最后5条,三元表达式必须写同一行
    # latest = todo_db[-5:] if len(todo_db) >= 5 else todo_db
    # if len(todo_db) >= 5:
    #     latest = todo_db[-5:]
    # else:
    #     latest = todo_db
    # SQLAlchemy查询：倒序，取5条
    todo_list = db.query(TodoDB).order_by(TodoDB.id.desc()).limit(5).all()
    # ORM对象转字典列表，存入redis
    data = [TodoOut.model_validate(item).model_dump() for item in todo_list]
    redis_client.setex("latest_5_todo", 60, json.dumps(data))
    return resp_ok(data=data, msg="查询MySQL，写入缓存")


# 写入redis，设置过期时间60秒
# redis_client.setex("latest_5_todo", 60, json.dumps(latest))
# return resp_ok(data=latest, msg="数据库查询，已写入缓存")


# 根据id查询单个todo，找不到抛异常（练习异常处理）
# @app.post("/todos/{todo_id}")
# async def get_one(todo_id: int, todo_db=None):
#     item = next((t for t in todo_db if t["id"] == todo_id), None)
#     if not item:
#         raise HTTPException(status_code=404, detail="任务不存在")
#     return resp_ok(data=item)
# 根据id查询单条任务
@app.get("/todos/{todo_id}", response_model=TodoOut)
async def get_one(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="任务不存在")
    return resp_ok(data=todo)

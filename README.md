# todo-api
基于 FastAPI 的待办任务后端接口 Demo

## 技术栈
- Python 3.11
- FastAPI
- SQLAlchemy（ORM）
- Redis（缓存最近5条任务）
- SQLite

## 功能
- 创建待办任务 POST /todos
- 获取单条任务 GET /todos/{todo_id}
- 获取最近5条任务（Redis缓存） GET /todos/latest5
- 自动生成Swagger接口文档 /docs

## 启动方式
1. 安装依赖
```bash
pip install fastapi
uvicorn
 sqlalchemy
 redis

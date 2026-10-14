# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库连接地址，我的数据库账号密码
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@127.0.0.1:3306/fastapi_todo"
# 换成sqlite
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
# 引擎和数据库建立连接的核心


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # 可选，输出SQL日志
    echo=True,  # 设置连接池活跃的连接数
    max_overflow=20  # 允许额外的连接数
)

# 会话工厂：创建数据库会话，session操作表
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM基类：所有数据库模型类都要继承
Base = declarative_base()


# 依赖函数：接口里拿到数据库session(FastAPI依赖注入，重点知识点)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

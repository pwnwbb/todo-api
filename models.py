from sqlalchemy import Column, Integer, String, Boolean
from database import Base


# 数据库表实体，SQLAIchemy ORM模型
class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(100), index=True, nullable=False)
    is_done = Column(Boolean, nullable=False)

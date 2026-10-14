# redis连接
import redis  # 导入库

REDIS_HOST = "localhost"
REDIS_POST = 6379
REDIS_DB = 0

# 创建Redis的连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,  # 服务器主机地址
    port=REDIS_POST,  # 端口号
    db=REDIS_DB,  # 数据库编号
    decode_responses=True  # 是否将字节数据解码为字符串
)

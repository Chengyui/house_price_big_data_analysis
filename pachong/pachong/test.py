# pymongo 库中导入 MongoClient
from pymongo import MongoClient

# 连接 MongoDB 数据库，通过 URL 的形式访问
client = MongoClient('mongodb://localhost:27017/')

# 检测客户端连接，可以通过查询文档数据是否能正常查询
for i in client.newdb.lightmap.find({}):
    print(i)

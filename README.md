# MyQuery

## 简介
基于 mysql-connector-python 的一个封装，提供了更简易的操作接口

基于 mysql-connector-python 文档：[文档](https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html)

## 安装
```bash
pip install myquery
```

## 使用示例

### 1、数据库建表
```sql

CREATE TABLE `person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `age` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
)

```

### 2、Database类

2.1 配置

```python

bd_url = "mysql://root:123456@127.0.0.1:3306/data?charset=utf8&autocommit=true"

# Deprecated
# db = DataBase(db_url=bd_url)

db = DataBase.from_url(bd_url)
# 或者

config = {
    "host": "127.0.0.1",
    "port": 3306,
    "username": "root",
    "password": "123456",
    "database": "data",
    "charset": "utf8",
    "autocommit": True
}
db = DataBase(**config)

```

2.2 打开关闭数据库

```python
# -*- coding: utf-8 -*-

from myquery.database import DataBase

db_url = "mysql://root:123456@127.0.0.1:3306/data?autocommit=true"
db = DataBase(db_url=db_url)

db.close()
```

2.3 插入数据
```python
# insert_one 返回插入数据的自增id

 # 命名占位符
user1 = {"name": "Tom", "age": 23}

sql = "insert into person (name, age) values (%(name)s, %(age)s)"
ret = db.insert_one(sql, user1)
print(ret) # 1


sql = "insert into person (name, age) values (:name, :age)"
ret = db.insert_one(sql, user1)
print(ret) # 2


# 占位符
user2 = ["Tom", 23]
sql = "insert into person (name, age) values (%s, %s)"
ret = db.insert_one(sql, user2)
print(ret) # 3

sql = "insert into person (name, age) values (?, ?)"
ret = db.insert_one(sql, user2)
print(ret) # 4


# 批量插入数据， insert返回插入数据的条数
user1 = {"name": "Tom", "age": 23}
user2 = {"name": "Jack", "age": 24}
sql = "insert into person (name, age) values (:name, :age)"
ret = db.insert(sql, [user1, user2])
print(ret) # 2
```

2.4 更新数据
```python
# update 返回影响行数
user1 = {"name": "Tom", "age": 23}
sql = "update person set name = :name, age = :age"
ret = db.update(sql, user1)
print(ret)
```

2.5 删除数据
```python
# delete 返回影响行数
sql = "delete from person where id = :id"
ret = db.delete(sql, {'id': 32})
print(ret)
```

2.6 查询数据
```python
# select_one 返回字典数据，select返回列表数据
sql = "select * from person where id = :id"
ret = db.select_one(sql, {'id': 1})
print(ret)
# {'id': 1, 'age': 23, 'name': 'Tom'}

sql = "select * from person where id > :id"
ret = db.select(sql, {'id': 1})
print(ret)
# [{'id': 3, 'age': 23, 'name': 'Tom'}]
```

2.7 获取Table类
```python
user1 = {"name": "Tom", "age": 23}
table = db.table("person")
ret = table.insert_one(user1)
print(ret)
```

2.8 事务
```python
sql1 = "update person set name = 'xxx' where id = 1"
sql2 = "update person set name = 'yyy' where id = 2"

db.transaction()

ret1 = db.update(sql1)
ret2 = db.update(sql2)
print(ret1)
print(ret2)

db.rollback()
```

## 3、Table类

Table类提供了常用的数据操作

```python
from myquery.table import Table


class PersonTable(Table):
    table_name = "person"
    database = db


# 插入一条数据
user1 = {"name": "Tom", "age": 23}
ret = PersonTable.insert_one(user1)
# INSERT INTO person (`name`, `age`) VALUES ('Tom', 23)
print(ret)

# 批量插入数据
user1 = {"name": "Tom", "age": 23}
user2 = {"name": "Tom", "age": 23}
ret = PersonTable.insert([user1, user2])
# INSERT INTO person (`name`, `age`) VALUES ('Tom', 23),('Tom', 23)
print(ret)

# 获取数据
ret = PersonTable.select_by_id(1)
# SELECT * FROM person WHERE `id` = 1
print(ret)
    
        

# 更新数据
user1 = {"name": "Tom", "age": 24, "id": 1}
ret = PersonTable.update_by_id(user1)
#  UPDATE person SET `name` = 'Tom', `age` = 24 WHERE `id` = 1
print(ret)

# 删除数据
ret = PersonTable.delete_by_id(2)
# DELETE FROM person WHERE `id` = 2
print(ret)

# 表中数据条数
ret = PersonTable.count()
# SELECT count(*) FROM person
print(ret)
```

## 4、ReconnectionDataBase

如果需要使用长链接的场景下，可以使用：
```python
db = ReconnectionDataBase(db_url=url)
```
会在*每次*发送sql语句到mysql之前，先执行ping测试连接情况

## 更新记录

- 2020-11-30 新增方法`DataBase.from_url(bd_url)`
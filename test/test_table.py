# -*- coding: utf-8 -*-

import unittest

######################
# 配置
######################
from myquery.database import DataBase
from myquery.table import Table

bd_url = "mysql://root:123456@127.0.0.1:3306/data?charset=utf8&autocommit=true"

config = {
    "host": "127.0.0.1",
    "port": 3306,
    "username": "root",
    "password": "123456",
    "database": "data",
    "charset": "utf8",
    "autocommit": True
}

######################
# 连接数据库
######################

# db = DataBase(db_url=bd_url)
db = DataBase(**config)



######################
# 定义Table
######################

class PersonTable(Table):
    table_name = "person"
    database = db


class DbTest(unittest.TestCase):
    def test_insert_one(self):
        user1 = {"name": "Tom", "age": 23}
        ret = PersonTable.insert_one(user1)
        # INSERT INTO person (`name`, `age`) VALUES ('Tom', 23)
        print(ret)

    def test_insert(self):
        user1 = {"name": "Tom", "age": 23}
        user2 = {"name": "Tom", "age": 23}
        ret = PersonTable.insert([user1, user2])
        # INSERT INTO person (`name`, `age`) VALUES ('Tom', 23),('Tom', 23)
        print(ret)

    def test_select_by_id(self):
        ret = PersonTable.select_by_id(1, 'name, age')
        ret = PersonTable.select_by_id(1, ['name', 'age'])
        # SELECT * FROM person WHERE `id` = 1
        print(ret)

    def test_update_by_id(self):
        user1 = {"name": "Tom", "age": 24, "id": 1}
        ret = PersonTable.update_by_id(user1)
        #  UPDATE person SET `name` = 'Tom', `age` = 24 WHERE `id` = 1
        print(ret)

    def test_delete_by_id(self):
        ret = PersonTable.delete_by_id(2)
        # DELETE FROM person WHERE `id` = 2
        print(ret)

    def test_count(self):
        ret = PersonTable.count()
        # SELECT count(*) FROM person
        print(ret)


if __name__ == '__main__':
    unittest.main()

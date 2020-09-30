# -*- coding: utf-8 -*-


import unittest
import logging
from myquery.database import DataBase, ReconnectionDataBase

logging.getLogger("myquery").setLevel(logging.DEBUG)

"""
CREATE TABLE `person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `age` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
)
"""


######################
# 定义测试 db
######################
class DbTest(unittest.TestCase):
    db = None
    db_url = "mysql://root:123456@127.0.0.1:3306/data?autocommit=true"

    @classmethod
    def setUpClass(cls):
        cls.db = ReconnectionDataBase(db_url=cls.db_url)
        # cls.db = DataBase(db_url=cls.db_url)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_insert_one(self):
        # 命名占位符
        user1 = {"name": "Tom", "age": 23}

        sql = "insert into person (name, age) values (%(name)s, %(age)s)"
        ret = self.db.insert_one(sql, user1)
        print(ret)

        sql = "insert into person (name, age) values (:name, :age)"
        ret = self.db.insert_one(sql, user1)
        print(ret)

        # 占位符
        user2 = ["Tom", 23]
        sql = "insert into person (name, age) values (%s, %s)"
        ret = self.db.insert_one(sql, user2)
        print(ret)

        sql = "insert into person (name, age) values (?, ?)"
        ret = self.db.insert_one(sql, user2)
        print(ret)

    def test_insert(self):
        user1 = {"name": "Tom", "age": 23}
        user2 = {"name": "Jack", "age": 24}
        sql = "insert into person (name, age) values (:name, :age)"
        ret = self.db.insert(sql, [user1, user2])
        print(ret)

    def test_update(self):
        user1 = {"name": "Tom", "age": 23}
        sql = "update person set name = :name, age = :age"
        ret = self.db.update(sql, user1)
        print(ret)

    def test_delete(self):
        sql = "delete from person where id = :id"
        ret = self.db.delete(sql, {'id': 32})
        print(ret)

    def test_select_one(self):
        sql = "select * from person where id = :id"
        ret = self.db.select_one(sql, {'id': 1})
        print(ret)

    def test_select(self):
        sql = "select * from person where id > :id"
        ret = self.db.select(sql, {'id': 1})
        print(ret)

    def test_table(self):
        user1 = {"name": "Tom", "age": 23}
        table = self.db.table("person")
        ret = table.insert_one(user1)
        print(ret)

    def test_transaction(self):
        sql1 = "update person set name = 'xxx' where id = 1"
        sql2 = "update person set name = 'yyy' where id = 2"

        self.db.transaction()

        ret1 = self.db.update(sql1)
        ret2 = self.db.update(sql2)
        print(ret1)
        print(ret2)

        self.db.rollback()


if __name__ == '__main__':
    unittest.main()

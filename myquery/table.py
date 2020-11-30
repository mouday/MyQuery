# -*- coding: utf-8 -*-
from myquery.util.database_util import DatabaseUtil
from myquery.sql_builder import SQLBuilder
from myquery.util.sql_builder_util import SQLBuilderUtil
from abc import ABC


class Table(ABC):
    """Table的基类，提供了部分简易操作"""
    # 真实的表名，可以为空
    table_name = None

    # 数据库实例
    database = None

    # 主键字段
    primary_key = "id"

    # select查询字段
    fields = "*"

    @classmethod
    def get_table_name(cls):
        """
        如果没有指定 table_name 属性，自动从类名中转换
        tip:
            类名尾部的继承标志会被去掉
            eg: Table
        :return: str
        """
        if cls.table_name is None:
            cls.table_name = DatabaseUtil.get_table_name(cls.__name__)

        if not cls.table_name:
            raise Exception("table name don't empty")

        return cls.table_name

    @classmethod
    def insert(cls, data):
        """插入列表数据"""
        table_name = cls.get_table_name()

        keys = SQLBuilderUtil.get_list_keys(data)
        keys_str = SQLBuilderUtil.get_key_str(keys)
        values_str = SQLBuilderUtil.get_value_str(keys)

        builder = SQLBuilder()
        # insert into table (name, age) values (?, ?)
        sql = builder.insert_into(table_name).append(f"({keys_str})").values(f"({values_str})").build()

        return cls.database.insert(sql, data)

    @classmethod
    def insert_one(cls, data):
        """插入字典数据"""
        table_name = cls.get_table_name()

        keys_str = SQLBuilderUtil.get_key_str(data.keys())
        values_str = SQLBuilderUtil.get_value_str(data.keys())

        # insert into table (name, age) values (?, ?)
        builder = SQLBuilder()
        sql = builder.insert_into(table_name).append(f"({keys_str})").values(f"({values_str})").build()
        return cls.database.insert_one(sql, data)

    @classmethod
    def delete_by_id(cls, uid):
        """删除数据"""
        table_name = cls.get_table_name()

        key_value_str = SQLBuilderUtil.get_key_value_str([cls.primary_key])

        # delete from table where id = ?
        builder = SQLBuilder()
        sql = builder.delete_from(table_name).where(key_value_str).build()

        return cls.database.delete(sql, {cls.primary_key: uid})

    @classmethod
    def update_by_id(cls, data):
        """更新数据 primary_key must in data"""
        table_name = cls.get_table_name()

        uid = data.pop(cls.primary_key)

        set_key_value_str = SQLBuilderUtil.get_key_value_str(data.keys())
        key_value_str = SQLBuilderUtil.get_key_value_str([cls.primary_key])

        # update table set name = ? where id = ?
        builder = SQLBuilder()
        sql = builder.update(table_name).set(set_key_value_str).where(key_value_str).build()

        data[cls.primary_key] = uid

        return cls.database.update(sql, data)

    @classmethod
    def select_by_id(cls, uid, fields=None):
        """获取数据
            fields: list/str
        """
        table_name = cls.get_table_name()

        if not fields:
            fields = cls.fields

        if isinstance(fields, list):
            fields = SQLBuilderUtil.get_key_str(fields)

        key_value_str = SQLBuilderUtil.get_key_value_str([cls.primary_key])

        # select * from table where id = ?
        builder = SQLBuilder()
        sql = builder.select(fields).from_(table_name).where(key_value_str).build()

        return cls.database.select_one(sql, {cls.primary_key: uid})

    @classmethod
    def count(cls):
        """统计数据"""
        table_name = cls.get_table_name()

        builder = SQLBuilder()

        # select count(*) from table
        sql = builder.select("count(*) as count").from_(table_name).build()
        ret = cls.database.select_one(sql)
        return ret['count']


Model = Table

# -*- coding: utf-8 -*-

import mysql.connector

from myquery.logger import logger
from myquery.table import Table
from myquery.util.database_util import DatabaseUtil
from myquery.util.sql_builder_util import SQLBuilderUtil


class DataBase(object):
    """对数据库访问进行封装
    参数参考：
    https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
    """

    def __init__(self, **kwargs):
        kwargs = DatabaseUtil.prepare_config(**kwargs)

        self.connect = mysql.connector.Connect(**kwargs)
        self.cursor = self.connect.cursor(dictionary=True)

        logger.debug("DataBase open")

    def close(self):
        """关闭游标和连接"""
        self.cursor.close()
        self.connect.close()

        logger.debug("DataBase close")

    def ping(self, reconnect=False, attempts=1, delay=0):
        self.connect.ping(reconnect, attempts, delay)

    def reconnect(self, attempts=1, delay=0):
        self.connect.reconnect(attempts, delay)

    def is_connected(self):
        return self.connect.is_connected()

    def _before_execute(self, operation, params):
        # 如果有:占位符再进行预处理
        if ":" in operation:
            operation = SQLBuilderUtil.compile_sql(operation)

        if "?" in operation:
            operation = SQLBuilderUtil.replace_sql(operation)

        logger.debug(f"before: {operation}")

        return operation

    def _after_execute(self):
        logger.info(f"after: {self.cursor.statement}")

    def execute_many(self, operation, seq_params):
        operation = self._before_execute(operation, seq_params)
        self.cursor.executemany(operation, seq_params)
        self._after_execute()

    def execute(self, operation, params):
        """
        :param operation: str 包含占位符的sql语句，支持4种占位符：%(key)s、:key、%s、?
        :param params: list/dict
        """
        operation = self._before_execute(operation, params)

        self.cursor.execute(operation, params)

        self._after_execute()

    def commit(self):
        self.connect.commit()

    def transaction(self, consistent_snapshot=False,
                    isolation_level=None, readonly=None):
        self.connect.start_transaction(
            consistent_snapshot, isolation_level, readonly)

    def rollback(self):
        self.connect.rollback()

    def select(self, operation, params=()):
        self.execute(operation, params)
        return self.cursor.fetchall()

    def select_one(self, operation, params=()):
        self.execute(operation, params)
        return self.cursor.fetchone()

    def update(self, operation, params=()):
        self.execute(operation, params)
        return self.cursor.rowcount

    def delete(self, operation, params=()):
        self.execute(operation, params)
        return self.cursor.rowcount

    def insert_one(self, operation, params=()):
        self.execute(operation, params)
        return self.cursor.lastrowid

    def insert(self, operation, seq_params):
        self.execute_many(operation, seq_params)
        return self.cursor.rowcount

    def table(self, table_name):
        return type(table_name, (Table,), {"table_name": table_name, "database": self})


if __name__ == '__main__':
    url = "mysql://root:123456@127.0.0.1:3306/data?charset=utf8"
    db = DataBase(db_url=url)
    print(db.is_connected())
    db.close()
    print(db.is_connected())

# -*- coding: utf-8 -*-
import re
from pprint import pprint
from urllib.parse import urlparse


class DatabaseUtil(object):
    @staticmethod
    def prepare_config(**kwargs):
        """数据库链接参数预处理"""

        db_url = kwargs.pop("db_url", None)

        if db_url:
            parse_config = DatabaseUtil.parse_db_url(db_url)
            if parse_config.pop('scheme') != "mysql":
                raise Exception("only support mysql scheme")
            kwargs.update(parse_config)

        return kwargs

    @staticmethod
    def parse_db_url(db_url):
        """
        解析bd_url
        :param db_url: str
        :return: dict
        """
        parse_result = urlparse(db_url)
        result = re.match(
            "(?P<username>.*):(?P<password>.*)@(?P<host>.*):(?P<port>\d+)", parse_result.netloc)

        group_dict = result.groupdict()

        db_config = {
            "scheme": parse_result.scheme,
            "database": parse_result.path.strip("/"),

            "username": group_dict.get("username"),
            "password": group_dict.get("password"),
            "host": group_dict.get("host"),
            "port": group_dict.get("port")
        }

        # 查询参数
        if parse_result.query:
            for query in parse_result.query.split("&"):
                key, value = query.split("=")

                # 注意bool值的转换
                if value == 'true':
                    value = True
                elif value == 'false':
                    value = False

                db_config[key] = value

        return db_config

    @classmethod
    def get_lower_class_name(cls, class_name):
        lst = []
        for index, char in enumerate(class_name):
            if char.isupper() and index != 0:
                lst.append("_")
            lst.append(char)

        return "".join(lst).lower()

    @classmethod
    def get_table_name(cls, table_name):
        if table_name.endswith('Table') or table_name.endswith('Model'):
            table_name = table_name[:-5]

        return DatabaseUtil.get_lower_class_name(table_name)


if __name__ == '__main__':
    url = "mysql://root:12345@6@127.0.0.1:3306/data?charset=utf8&autocommit=false"
    url = "mysql://root:12345@6@127.0.0.1:3306/data"
    pprint(DatabaseUtil.parse_db_url(url))

# -*- coding: utf-8 -*-
from pprint import pprint

from myquery.util.db_url import parse_url_to_dict


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
        return parse_url_to_dict(db_url)

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

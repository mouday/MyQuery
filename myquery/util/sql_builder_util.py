# -*- coding: utf-8 -*-
import re


class SQLBuilderUtil(object):
    @staticmethod
    def get_key_str(keys):
        """
        获取 键 的字符串拼接
        fields list

        eg:
        >>> SQLBuilderUtil.get_key_str(["name", "age"])
        '`name`, `age`'
        """
        return ", ".join(["`{}`".format(key) for key in keys])

    @staticmethod
    def get_value_str(keys):
        """
        获取 值 的字符串拼接
        :param keys: list
        :return: str

        eg:
        >>> SQLBuilderUtil.get_value_str(["name", "age"])
        '%(name)s, %(age)s'

        """
        return ", ".join(["%({})s".format(key) for key in keys])

    @staticmethod
    def get_key_value_str(keys):
        """
        获取 键-值 的字符串拼接
        :param keys: list
        :return: str

        eg:
        >>> SQLBuilderUtil.get_key_value_str(["name", "age"])
        '`name` = %(name)s, `age` = %(age)s'

        """
        return ", ".join(["`{0}` = %({0})s".format(key) for key in keys])

    @classmethod
    def get_list_keys(cls, data):
        """
        列表中字典key值校验
        :param data: list(dict)
        :return: list(key)

        eg:
        >>> user1 = {"name": "Tom"}
        >>> user2 = {"name": "Jack"}
        >>> user3 = {"name": "Jack", "age": 24}

        >>> data = [user1, user2]
        >>> SQLBuilderUtil.get_list_keys(data)
        ['name']

        >>> data = [user1, user2, user3]
        >>> SQLBuilderUtil.get_list_keys(data)
        Traceback (most recent call last):
            ...
        Exception: data key not equal!

        """

        keys = data[0].keys()
        for item in data:
            if item.keys() != keys:
                raise Exception("data key not equal!")

        return [key for key in keys]

    @classmethod
    def compile_sql(cls, sql):
        """转换sql中变量占位符 :key -> %(key)s"""
        return re.sub(r":(?P<key>\w+)", r"%(\g<key>)s", sql)

    @classmethod
    def replace_sql(cls, sql):
        """占位符替换 ? -> %s """
        return sql.replace("?", "%s")


def main():
    sql = "update person set name = :name , age = :age, id = ?"
    print(SQLBuilderUtil.compile_sql(sql))
    print(SQLBuilderUtil.replace_sql(sql))


if __name__ == '__main__':
    # import doctest
    #
    # doctest.testmod()

    main()

# -*- coding: utf-8 -*-

# @Date    : 2019-06-27
# @Author  : Peng Shiyu


from functools import partial


class SQLBuilder(object):
    """
    SQL拼接

    eg:
    >>> sql_builder = SQLBuilder()
    >>> sql_builder.select("name, age").from_("student").where("id=1").build()
    'SELECT name, age FROM student WHERE id=1'

    """

    def __init__(self):
        self._sqls = []

    def __getattr__(self, item):
        return partial(self.append, item)

    def append(self, key, value=None):
        if value:
            key = key.upper().strip("_").replace("_", " ")
            self._sqls.append("{} {}".format(key, value))
        else:
            self._sqls.append(key)
        return self

    def build(self):
        return " ".join(self._sqls)

    def __str__(self):
        return self.build()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

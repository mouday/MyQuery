# -*- coding: utf-8 -*-
from urllib.parse import urlparse, parse_qsl


# code reference : playhouse.db_url.parse
def parse_query(query):
    qs_args = parse_qsl(query, keep_blank_values=True)

    query_dict = {}

    for key, value in qs_args:
        if value.lower() == 'false':
            value = False
        elif value.lower() == 'true':
            value = True
        elif value.isdigit():
            value = int(value)
        elif '.' in value and all(p.isdigit() for p in value.split('.', 1)):
            try:
                value = float(value)
            except ValueError:
                pass
        elif value.lower() in ('null', 'none'):
            value = None

        query_dict[key] = value

    return query_dict


def parse_url_to_dict(db_url):
    parsed = urlparse(db_url)

    kwargs = {
        'database': parsed.path[1:],
        'username': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port,
        'scheme': parsed.scheme
    }

    query_kwargs = parse_query(parsed.query)
    kwargs.update(query_kwargs)
    return kwargs


if __name__ == '__main__':
    url1 = 'mysql://root:123456@127.0.0.1:3306/data?autocommit=true'
    url2 = 'mysql://127.0.0.1:3306/data?autocommit=true'
    url3 = 'mysql://127.0.0.1:3306/data'

    print(parse_url_to_dict(url1))
    print(parse_url_to_dict(url2))
    print(parse_url_to_dict(url3))

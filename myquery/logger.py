# -*- coding: utf-8 -*-

import logging

# 设置日志
logger = logging.getLogger("myquery")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("myquery: %(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)

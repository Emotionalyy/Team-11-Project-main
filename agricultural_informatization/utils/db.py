from typing import Any
import pymysql

from .hooks import EXIT_HOOK_FUNCS
from .config import (
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DATABASE
)


agri_conn = pymysql.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
"""Mysql 数据库连接对象"""

def execute_sql(sql: str) -> tuple[tuple[Any, ...], ...]:
    """
    运行所给的SQL语句，并返回结果。
    """
    agri_conn.ping(True)
    cursor = agri_conn.cursor()
    cursor.execute(sql)
    agri_conn.commit()
    res = cursor.fetchall()
    return res


EXIT_HOOK_FUNCS.append(agri_conn.close)


__all__ = [
    "agri_conn",
    "execute_sql"
]
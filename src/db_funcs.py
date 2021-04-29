import psycopg2
from typing import Union

_conn = None


def _generate_sql_tuple(values: Union[list, tuple]) -> str:
    query = "("
    for elem in values:
        if type(elem) != str or elem.upper() == 'DEFAULT':
            query += str(elem)
            query += ", "
        else:
            query += f"'{elem}'"
            query += ", "
    query = query.rstrip(" ,")
    query += ");"
    return query


def _generate_sql_where_from_dict(data: dict) -> str:
    sql = ""
    for key in data:
        if type(data[key]) == str:
            sql += f"{key} = '{data[key]}' and "
        elif data[key] is None:
            sql += f"{key} is NULL and "
        else:
            sql += f"{key} = {data[key]} and "
    return sql


# Установить подключение с базой данных
def set_connection(uri: str, autocommit: bool = False) -> psycopg2._psycopg.connection:
    global _conn
    if _conn is None:
        _conn = psycopg2.connect(uri)
        _conn.autocommit = autocommit
        return _conn


# Получить курсор
def get_cursor() -> psycopg2._psycopg.cursor:
    global _conn
    if _conn is not None:
        return _conn.cursor()


# Отправить запрос в СУБД
def execute_query(query: str) -> psycopg2._psycopg.cursor:
    cursor = get_cursor()
    cursor.execute(query)
    return cursor


# Коммит последних запросов
def commit():
    global _conn
    if _conn is not None:
        return _conn.commit()


# Получение данных из таблицы
def db_read_table(table: str, limit: int = 0, sql_condition: str = '', order_by: tuple = ('', '')) -> tuple:
    cursor = get_cursor()
    query = f'SELECT * FROM {table}'
    if sql_condition != '':
        query += f" where {sql_condition}"
    if order_by != ('', ''):
        query += f" order by {order_by[0]} {order_by[1]}"
    if limit != 0:
        query += f" limit {limit}"
    query += ';'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.cursor.commit()
    return data

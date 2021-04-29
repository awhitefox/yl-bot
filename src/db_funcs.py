from typing import Union, Dict, Tuple, List, Any

import psycopg2

_conn = None


def _generate_sql_tuple(values: Union[List[Any], Tuple[Any]]) -> str:
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


def _generate_sql_where_from_dict(data: Dict[str, Any]) -> str:
    sql = ""
    for key in data:
        if type(data[key]) == str:
            sql += f"{key} = '{data[key]}' AND "
        elif data[key] is None:
            sql += f"{key} IS NULL AND "
        else:
            sql += f"{key} = {data[key]} AND "
    return sql


def set_connection(uri: str, autocommit: bool = False) -> psycopg2._psycopg.connection:
    """Установить подключение с базой данных"""
    global _conn
    if _conn is None:
        _conn = psycopg2.connect(uri)
        _conn.autocommit = autocommit
        return _conn


def get_cursor() -> psycopg2._psycopg.cursor:
    """Получить курсор"""
    global _conn
    if _conn is not None:
        return _conn.cursor()


def execute_query(query: str) -> psycopg2._psycopg.cursor:
    """Отправить запрос в СУБД"""
    cursor = get_cursor()
    cursor.execute(query)
    return cursor


def commit() -> None:
    """Коммит последних изменений"""
    global _conn
    if _conn is not None:
        return _conn.commit()


def db_read_table(table: str, limit: int = 0, sql_condition: str = '', order_by: Tuple[str, str] = ('', '')) \
        -> List[Tuple[Any]]:
    """Получение данных из таблицы"""
    cursor = get_cursor()
    query = f'SELECT * FROM {table}'
    if sql_condition != '':
        query += f" WHERE {sql_condition}"
    if order_by != ('', ''):
        query += f" ORDER BY {order_by[0]} {order_by[1]}"
    if limit != 0:
        query += f" LIMIT {limit}"
    query += ';'
    cursor.execute(query)
    data = cursor.fetchall()
    return data

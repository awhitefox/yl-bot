import psycopg2

_conn = None


def set_connection(uri: str, autocommit=False) -> psycopg2._psycopg.connection:
    global _conn
    if _conn is None:
        _conn = psycopg2.connect(uri)
        _conn.autocommit = autocommit
        return _conn


def get_cursor() -> psycopg2._psycopg.cursor:
    global _conn
    if _conn is not None:
        return _conn.cursor()


def execute_query(query: str) -> psycopg2._psycopg.cursor:
    cursor = get_cursor()
    cursor.execute(query)
    return cursor


def commit():
    global _conn
    if _conn is not None:
        return _conn.commit()


def db_read_table(table, limit=0, sql_condition='', order_by=('', '')) -> tuple:
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

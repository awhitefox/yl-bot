import psycopg2

_conn = None


def set_connection(uri: str, autocommit=False):
    global _conn
    if _conn is None:
        _conn = psycopg2.connect(uri)
        _conn.autocommit = autocommit
        return _conn


def execute_query(query: str):
    global _conn
    if _conn is not None:
        cursor = _conn.cursor()
        cursor.execute(query)
    return True


def create_table(table_name, **kwargs):
    global _conn
    query = f"CREATE TABLE {table_name}("
    for key in kwargs:
        pass


from typing import Union, Dict, List, Tuple, Optional, Any
from .db_funcs import execute_query, _generate_sql_where_from_dict, _generate_sql_tuple


class CreatedTable:
    """Класс для работы с таблицей в БД"""

    def __init__(self, table_name: str):
        self.table = table_name
        self.cursor = execute_query(f'SELECT * FROM {table_name} LIMIT 0')
        self.columns = [desc[0] for desc in self.cursor.description]
        self.selected_data = []

    def get_data(self, limit: Optional[int] = None) -> List[Tuple[Any]]:
        """Получение данных из таблицы в виде списка кортежей"""
        query = f"SELECT {', '.join(self.columns)} FROM {self.table} "
        if limit is not None:
            query += f"LIMIT {limit}"
        return execute_query(query).fetchall()

    def find(self, index: int, name_id_field: str = 'id'):
        """Поиск элемента по значению столбца 'id'(можно указать другой)"""
        self.selected_data.extend(execute_query(
            f"SELECT {', '.join(self.columns)} FROM {self.table} WHERE {name_id_field}={index}").fetchall())
        return self

    def where(self, where_cond: str):
        """Поиск элемента через sql where условие"""
        self.selected_data.extend(execute_query(
            f"SELECT {', '.join(self.columns)} FROM {self.table} WHERE {where_cond}").fetchall())
        return self

    def get_selected_data(self) -> List[Dict[str, Any]]:
        """Получение выбранных(методы where и find) элементов"""
        return self.__make_dict_data(self.selected_data)

    def clear_selected_data(self):
        """Очистка массива с выбранными элементами"""
        self.selected_data = []
        return self

    def get_form_data(self, limit: int = 0, where_cond: Optional[str] = None) -> List[Dict[str, Any]]:
        """Получение данных из таблицы в виде массива словарей
        (ключ - имя столбца, значение - значение элемента в таблице)"""
        query = f"SELECT {', '.join(self.columns)} FROM {self.table} "
        if where_cond:
            query += f"WHERE {where_cond} "
        if limit:
            query += f"LIMIT {limit} "

        data = execute_query(query).fetchall()
        return self.__make_dict_data(data)

    def __make_dict_data(self, data: Union[List[Any], Tuple[Any]]) -> List[Dict[str, Any]]:
        new_data = []
        for elem in data:
            tmp = {}
            keys = list(self.columns)
            for i in range(len(elem)):
                tmp[keys[i]] = elem[i]
            new_data.append(tmp)
        return new_data

    def try_delete(self) -> None:
        """Удаление элементов которые прошли выборку(методы where и find)"""
        data = self.get_selected_data()
        for elem in data:
            sql = f"DELETE FROM {self.table} WHERE "
            sql += _generate_sql_where_from_dict(elem)
            sql = sql.rstrip("and ")
            sql += ";"
            execute_query(sql)
        self.clear_selected_data()
        return

    def update(self, **kwargs: Any) -> None:
        """Изменение выбранных элементов.
        Данные передаются через именнованные необязательные параметры
        (ключ - имя столбца, значение - новое значение элемента)"""
        data = self.get_selected_data()
        for elem in data:
            sql = f"UPDATE {self.table} SET "
            for value in kwargs:
                if type(kwargs[value]) == str:
                    sql += f"{value} = '{kwargs[value]}'"
                else:
                    sql += f"{value} = {kwargs[value]}"
                sql += ', '
            sql = sql.rstrip(', ')
            sql += " WHERE "
            sql += _generate_sql_where_from_dict(elem)
            sql = sql.rstrip("and ")
            sql += ";"
            execute_query(sql)
        self.clear_selected_data()
        return

    def insert(self, *args: Union[List[Any], Dict[str, Any], Tuple[Any]], **kwargs: Any) -> None:
        """Вставка данных. Можно передать кортеж/список:  .insert(["value1", 2, True])
        или словарь: .insert({'col1': 'value1', 'col2': 2, 'col3': True})
        или через именнованные необязательные параметры .insert(col1='value1', col2=2, col3=True)"""
        if len(args) > 0:
            if type(*args) == dict:
                execute_query(self._query_dict_insert(*args))
                return
            else:
                execute_query(self._query_list_insert(*args))
                return
        elif len(kwargs) > 0:
            execute_query(self._query_dict_insert(**kwargs))
            return
        else:
            execute_query(f'INSERT INTO {self.table} VALUES ()')
            return

    def _query_list_insert(self, collection: Union[List[Any], Tuple[Any]]) -> str:
        query = f"INSERT INTO {self.table} VALUES "
        query += _generate_sql_tuple(collection)
        return query

    def _query_dict_insert(self, data: Dict[str, Any]) -> str:
        keys = tuple(data)
        values = tuple(data.values())
        query = f"INSERT INTO {self.table}("
        for elem in keys:
            query += f"{elem}"
            query += ", "
        query = query.rstrip(" ,")
        query += ") VALUES "
        query += _generate_sql_tuple(values)

        return query

    def drop(self) -> None:
        """Удалить таблицу"""
        execute_query(f"DROP TABLE {self.table}")
        return

from .db_funcs import commit, execute_query, _generate_sql_where_from_dict, _generate_sql_tuple
from typing import Union


class CreatedTable:
    def __init__(self, table_name: str):
        self.table = table_name
        self.cursor = execute_query(f'Select * FROM {table_name} LIMIT 0')
        self.columns = [desc[0] for desc in self.cursor.description]
        commit()
        self.selected_data = []

    # Получение данных из таблицы в виде списка кортежей
    def get_data(self, limit: int = None) -> list:
        query = f"SELECT {', '.join(self.columns)} FROM {self.table} "
        if limit is not None:
            query += f"LIMIT {limit}"
        return execute_query(query).fetchall()

    # Поиск элемента по значению столбца 'id'(можно указать другой)
    def find(self, index: int, name_id_field: str = 'id'):
        self.selected_data.extend(execute_query(
            f"select {', '.join(self.columns)} from {self.table} where {name_id_field}={index}").fetchall())
        return self

    # Поиск элемента по через sql where условие
    def where(self, where_cond: str):
        self.selected_data.extend(execute_query(
            f"select {', '.join(self.columns)} from {self.table} where {where_cond}").fetchall())
        return self

    # Получение выбранных(методы where и find) элементов
    def get_selected_data(self) -> list:
        return self.__make_dict_data(self.selected_data)

    # Очистка массива с выбранными элементами
    def clear_selected_data(self):
        self.selected_data = []
        return self

    # Получение данных из таблицы в виде массива словарей(ключ - имя столбца, значение - значение элемента в таблице)
    def get_form_data(self, limit: int = 0, where_cond: str = None) -> list:
        query = f"SELECT {', '.join(self.columns)} FROM {self.table} "
        if where_cond:
            query += f"WHERE {where_cond} "
        if limit:
            query += f"LIMIT {limit} "

        data = execute_query(query).fetchall()
        return self.__make_dict_data(data)

    def __make_dict_data(self, data: Union[list, tuple]) -> list:
        new_data = []
        for elem in data:
            tmp = {}
            keys = list(self.columns)
            for i in range(len(elem)):
                tmp[keys[i]] = elem[i]
            new_data.append(tmp)
        return new_data

    # Удаление элементов которые прошли выборку(методы where и find)
    def delete(self) -> bool:
        data = self.get_selected_data()
        for elem in data:
            sql = f"DELETE FROM {self.table} WHERE "
            sql += _generate_sql_where_from_dict(elem)
            sql = sql.rstrip("and ")
            sql += ";"
            execute_query(sql)
        self.clear_selected_data()
        return True

    # Изменение выбранных элементов. В метод передаются кварги(ключ - имя столбца, значение - новое значение элемента)
    def update(self, **kwargs: Union[str, int]) -> bool:
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
        return True

    # Вставка данных. Можно передать кортеж/список:  .insert(["value1", 2, True]
    # или словарь: .insert({'col1': 'value1', 'col2': 2, 'col3': True})
    # или через кварги .insert(col1='value1', col2=2, col3=True)
    def insert(self, *args: Union[list, dict, tuple], **kwargs: Union[str, int, bool]) -> bool:
        if len(args) > 0:
            if type(*args) == dict:
                execute_query(self._query_dict_insert(*args))
                return True
            else:
                execute_query(self._query_list_insert(*args))
                return True
        elif len(kwargs) > 0:
            execute_query(self._query_dict_insert(**kwargs))
            return True
        else:
            execute_query(f'INSERT INTO {self.table} VALUES ()')
            return True

    def _query_list_insert(self, collection: Union[list, tuple]) -> str:
        query = f"INSERT INTO {self.table} VALUES "
        query += _generate_sql_tuple(collection)
        return query

    def _query_dict_insert(self, data: dict) -> str:
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

    # Удалить таблицу
    def drop(self) -> bool:
        execute_query(f"DROP TABLE {self.table}")
        return True

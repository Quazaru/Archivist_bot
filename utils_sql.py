import config
import queries_sql
import text
import psycopg2

class DBHandler:
    _connection = None
    _cursor = None
    _queryHelper = queries_sql.QueryHelper()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                connection = psycopg2.connect(
                    host=config.PSQL_HOST,
                    user=config.PSQL_USER,
                    password=config.PSQL_PASSWORD,
                    database=config.PSQL_DB_NAME,
                )
                cls._connection = connection
                cls._cursor = connection.cursor() # Получаем необходимые обработчики
                
                print("[INFO] DBHandler connected successfully")
            except psycopg2.Error as error:
                print("[ERROR] Error constructing DBHandler", error)
                cls.__del__()
        return cls._instance

    def __init__(self) -> None:
        pass

    def __del__(self):
        if self._connection:
                self._connection.close()
        print("[INFO] DBHandler closed")

    def database_init(self) -> None:
        try:
            self._cursor.execute(queries_sql.query_database_version)
            print(f"[INFO] Server version: {self._cursor.fetchone()}")
            self._cursor.execute(queries_sql.query_database_init)
            self._connection.commit()
            print(text.info_database_created)
        except Exception as _ex:
            print(text.info_database_error.format(error=_ex) + " \n_____ from DBHandler")


    def table_insert(self, table_name, insert_dict) -> None:
        query = self._queryHelper.generate_query_insert(tableName=table_name, insert_dict=insert_dict)
        self._cursor.execute(query)
        self._connection.commit()
    def table_select(self, table_name, condition_tuple) -> list[dict]:
        query = self._queryHelper.generate_query_select(table_name, condition_tuple)
        self._cursor.execute(query)
        rows = self._cursor.fetchall()

        # Получаем описание столбцов из курсора
        column_names = [desc[0] for desc in self._cursor.description]

        # Преобразуем полученные строки в список словарей
        results = []
        for row in rows:
            result_dict = {}
            for i, value in enumerate(row):
                column_name = column_names[i]
                # Если значение числовое, преобразуем его в число, иначе оставляем строку
                result_dict[column_name] = value if isinstance(value, (int, float)) else str(value)
            results.append(result_dict)
        return results
    def table_select_new(self, table_name, condition_tuple, orderByField, isDESC):
        pass
    def table_select_all(self, table_name) -> list[dict]:
        self._cursor.execute(f"SELECT * FROM {table_name}")
        rows = self._cursor.fetchall()
        column_names = [desc[0] for desc in self._cursor.description]
        results = []
        for row in rows:
            result_dict = {}
            for i, value in enumerate(row):
                column_name = column_names[i]
                result_dict[column_name] = value if isinstance(value, (int, float)) else str(value)
            results.append(result_dict)
        return results
    def table_update(self, table_name, update_dict, condition_tuple) -> None:
        query = self._queryHelper.generate_query_update(table_name, update_dict, condition_tuple)
        self._cursor.execute(query)
        self._connection.commit()
    def table_delete(self, table_name, condition_tuple) -> None:
        query = self._queryHelper.generate_query_delete(table_name, condition_tuple)
        self._cursor.execute(query)
        self._connection.commit()   

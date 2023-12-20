## DATABASE ##
query_database_init = """
                CREATE TABLE IF NOT EXISTS Users (
                    "UserID" BIGINT PRIMARY KEY,
                    "SelectedCollectionID" INTEGER NOT NULL
                );           

                CREATE TABLE IF NOT EXISTS Collections (
                    "CollectionID" SERIAL PRIMARY KEY,
                    "Name" VARCHAR(50) NOT NULL,
                    "CreationTimestamp" FLOAT NOT NULL,
                    "UserID" BIGINT NOT NULL,
                    CONSTRAINT collection_user_fk
                    FOREIGN KEY ("UserID") REFERENCES Users ("UserID")
                );

                CREATE TABLE IF NOT EXISTS Notes (
                    "NoteID" SERIAL PRIMARY KEY,
                    "Name" VARCHAR(50) NOT NULL,
                    "CreationTimestamp" FLOAT NOT NULL,
                    "NoteText" TEXT,
                    "CollectionID" INTEGER NOT NULL,
                    CONSTRAINT note_collection_fk
                    FOREIGN KEY ("CollectionID") REFERENCES Collections ("CollectionID")
                );
                           
                CREATE TABLE IF NOT EXISTS Files (
                    "FileID" SERIAL PRIMARY KEY,
                    "FileType" VARCHAR(20) NOT NULL,
                    "tg_FileID" VARCHAR(50) NOT NULL,
                    "NoteID" INTEGER NOT NULL,
                    CONSTRAINT files_notes_fk
                    FOREIGN KEY ("NoteID") REFERENCES Notes ("NoteID")       
                );      
            """
query_database_version = """
                SELECT version();
            """

## COLLECTIONS ##
query_collections_insert = """
            INSERT INTO Collections (Name, CreationTime, UserID)
            VALUES 
                ('{Name}', '{CreationTime}', '{tg_UserID}');
            """
query_collections_select_ByUserID = """
                SELECT * FROM Collections WHERE UserID = {UserID}
            """
query_collections_select_ByName = """
                SELECT * FROM Collections WHERE Name = {CollectionName}
            """

## NOTES ##
query_notes_insert = """
                INSERT INTO Notes (CollectionID, CreationTime, NoteText, Name)
                SELECT 
                    COALESCE((SELECT CollectionID FROM Collections WHERE Name = {CollectionName} LIMIT 1), 1) AS CollectionID,
                    '{CreationTime}' AS CreationTime,
                    '{NoteText}' AS NoteText,
                    '{NoteName}' AS NAME
                ON CONFLICT DO NOTHING;
            """
query_notes_select_ByCollectionID = """
                SELECT * FROM Notes WHERE CollectionID = {CollectionID}
            """

## abstract
class QueryHelper:
    query_insert = """
            INSERT INTO {0} ({1})
            VALUES ({2});
            """
    query_select = """
            SELECT * FROM {0} WHERE {1};
            """
    query_select_template = """ SELECT * FROM {0} """
    query_select_sorted = """
            SELECT * FROM {0} ORDER BY {1} {2};
            """
    query_update = """
            UPDATE {0} SET {1} WHERE {2};
            """
    query_delete = """
            DELETE {0} WHERE {1};
            """
    
    
    def generate_query_insert(self, tableName, insert_dict):
        """
        Создает строку запроса INSERT для вставки данных в указанную таблицу.

        Аргументы:
        - tableName (str): Имя таблицы, в которую будет производиться вставка данных.
        - insert_dict (dict): Словарь, содержащий пары ключ-значение для вставки в таблицу.

        Возвращает:
        - str: Строка запроса INSERT, вставляющая данные из указанного словаря в указанную таблицу.

        Пример использования:
        >>> query_helper = QueryHelper()
        >>> data_to_insert = {'Name': 'John', 'Age': 30, 'City': 'New York'}
        >>> table_name = 'Users'
        >>> query = query_helper.generate_query_insert(table_name, data_to_insert)
        """
        columnNames = ', '.join(f'"{key}"' for key in insert_dict.keys())
        
        columnValues = ', '.join(f"'{value}'" if isinstance(value, str) else str(value) for value in insert_dict.values())
        query_insert = self.query_insert.format(tableName, columnNames, columnValues)
        return query_insert

    ###    
    def generate_query_select(self, tableName, condition_tuple=(), orderByField="", isDESC=False):
        """
        Функция для генерации SQL-запроса SELECT с дополнительными параметрами
        Принимает аргументы:
          - tableName: имя таблицы для запроса
          - condition_tuple: кортеж условий вида ("fieldName", "operator", fieldValue) | (по умолчанию пустой)
          - orderByField: поле для сортировки (по умолчанию пустая строка)
          - isDESC: флаг сортировки в порядке убывания (по умолчанию False)
          """
        query = self.query_select_template.format(tableName)
        if(condition_tuple):
            query += "WHERE " + self.getConditionStr(condition_tuple=condition_tuple)
        if(orderByField):
            DESC = "DESC" if isDESC else ""
            query+= f"\nORDER BY {orderByField} {DESC}"
        return query+";"
    ###
    def generate_query_update(self, tableName, update_dict, conditionTuple):
        """
        Создает строку запроса UPDATE для обновления данных в указанной таблице с заданными условиями.

        Аргументы:
        - tableName (str): Имя таблицы, которую необходимо обновить.
        - update_dict (dict): Словарь, содержащий пары ключ-значение для обновления данных.
        - conditionTuple (tuple): Кортеж с условиями для фильтрации обновляемых данных в формате
                                  (поле, оператор, значение) для каждого условия.

        Возвращает:
        - str: Строка запроса UPDATE, обновляющая указанные поля таблицы с заданными значениями
               при соблюдении указанных условий.

        Пример использования:
        >>> query_helper = QueryHelper()
        >>> updates = {'Name': 'John', 'Age': 30}
        >>> condition = (('Age', '>', 25), ('City', '=', 'New York'))
        >>> table_name = 'Users'
        >>> query = query_helper.generate_query_update(table_name, updates, condition)
        """
        updateSetterStr = self.updateSetterStr(update_dict)
        conditionStr = self.getConditionStr(conditionTuple)

        query_update = f"""
            UPDATE {tableName} SET {updateSetterStr} WHERE {conditionStr};
        """
        return query_update
    def generate_query_delete(self, tableName, condition_tuple):
        """
        Создает строку запроса DELETE для удаления данных из указанной таблицы с заданными условиями.

        Аргументы:
        - tableName (str): Имя таблицы, из которой будут удаляться данные.
        - condition_tuple (tuple): Кортеж с условиями для удаления данных в формате
                                   (поле, оператор, значение) для каждого условия.

        Возвращает:
        - str: Строка запроса DELETE, удаляющая данные из указанной таблицы с указанными условиями.

        Пример использования:
        >>> query_helper = QueryHelper()
        >>> table_name = 'Users'
        >>> conditions = (('Age', '>', 30), ('City', '=', 'New York'))
        >>> query = query_helper.generate_query_delete(table_name, conditions)
        """
        conditionStr = self.getConditionStr(condition_tuple)
        query_delete = self.query_delete.format(tableName, conditionStr)
        return query_delete
    def getConditionStr(self, condition_tuple):
        """
        Создает строковое представление условий на основе кортежа.

        Аргументы:
        - condition_tuple (tuple): Кортеж, содержащий условия в формате
                                (поле, оператор, значение) для каждого условия.

        Возвращает:
        - str: Строка, представляющая условия, объединенные 'AND'. Если есть только
            одно условие, возвращает его как строку. Если условий нет, возвращает
            пустую строку.
        """
        conditions = []
        # Проверка если передан один элемент для условия
        if len(condition_tuple) == 3 and all(isinstance(elem, (str, int, float)) for elem in condition_tuple):
            field, operator, value = condition_tuple
            if isinstance(value, int) or isinstance(value, float):
                condition = f"\"{field}\" {operator} {value}"
            else:
                condition = f"\"{field}\" {operator} '{value}'"
            return condition

        for idx, (field, operator, value) in enumerate(condition_tuple):
            if isinstance(value, int) or isinstance(value, float):
                condition = f"\"{field}\" {operator} {value}"
            else:
                condition = f"\"{field}\" {operator} '{value}'"
            conditions.append(condition)

        if len(conditions) > 1:
            return ' AND '.join(conditions)
        elif len(conditions) == 1:
            
            return conditions[0]
        else:
            return ''
    def updateSetterStr(self, update_dict):
        """
        Создает строковое представление для обновления значений на основе словаря.

        Аргументы:
        - update_dict (dict): Словарь, содержащий пары ключ-значение для обновления.

        Возвращает:
        - str: Строка, представляющая обновления в формате 'ключ = 'значение'', разделенные запятыми.
        """
        if len(update_dict) == 1:
            field, value = next(iter(update_dict.items()))
            if isinstance(value, int) or isinstance(value, float):
                return f"\"{field}\" = {value}"
            else:
                return f"\"{field}\" = '{value}'"
        else:
            setters = []
            for field, value in update_dict.items():
                if isinstance(value, int) or isinstance(value, float):
                    setters.append(f"\"{field}\" = {value}")
                else:
                    setters.append(f"\"{field}\" = '{value}'")
            return ', '.join(setters)


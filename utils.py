import config
import psycopg2

def add_note(collection_id, user_id, note_text):
    """
    Функция для добавления заметки в таблицу Notes.

    Параметры:
    - collection_id: ID коллекции, к которой привязана заметка.
    - user_id: ID пользователя, создавшего заметку.
    - note_text: Текст заметки.

    Добавляет новую заметку в таблицу Notes с указанными данными.
    """
    try:
        # Соединение с базой данных
        connection = psycopg2.connect(
            host=config.PSQL_HOST,
            user=config.PSQL_USER,
            password=config.PSQL_PASSWORD,
            database=config.PSQL_DB_NAME,
        )

        # Вставка заметки
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Notes (CollectionID, UserID, NoteText, CreationDate, LastModifiedDate)
                VALUES (%s, %s, %s, CURRENT_DATE, CURRENT_DATE)
            """, (collection_id, user_id, note_text))
            
        # Подтверждение изменений в базе данных
        connection.commit()
        print("Заметка успешно добавлена!")

    except psycopg2.Error as error:
        print("Ошибка при работе с PostgreSQL:", error)

    finally:
        # Закрытие соединения
        if connection:
            connection.close()

def get_note_by_id(note_id):
    try:
        connection = psycopg2.connect(
            host=config.PSQL_HOST,
            user=config.PSQL_USER,
            password=config.PSQL_PASSWORD,
            database=config.PSQL_DB_NAME,
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM Notes WHERE NoteID = %s
            """, (note_id,))
            note_data = cursor.fetchone()
            if note_data:
                return note_data
            else:
                return None

    except psycopg2.Error as error:
        print("Ошибка при работе с PostgreSQL:", error)
        return None

    finally:
        if connection:
            connection.close()

def create_collection(user_id, author_username, creation_date):
    try:
        connection = psycopg2.connect(
            host=config.PSQL_HOST,
            user=config.PSQL_USER,
            password=config.PSQL_PASSWORD,
            database=config.PSQL_DB_NAME,
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Collections (UserID, AuthorUsername, CreationDate)
                VALUES (%s, %s, %s)
            """, (user_id, author_username, creation_date))
            
        connection.commit()
        print("Коллекция успешно создана!")

    except psycopg2.Error as error:
        print("Ошибка при работе с PostgreSQL:", error)

    finally:
        if connection:
            connection.close()

def get_notes_in_collection(collection_id):
    try:
        connection = psycopg2.connect(
            host=config.PSQL_HOST,
            user=config.PSQL_USER,
            password=config.PSQL_PASSWORD,
            database=config.PSQL_DB_NAME,
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT NoteID FROM Notes WHERE CollectionID = %s
            """, (collection_id,))
            notes_ids = cursor.fetchall()
            return [note[0] for note in notes_ids]

    except psycopg2.Error as error:
        print("Ошибка при работе c PostgreSQL:", error)
        return None

    finally:
        if connection:
            connection.close()

def get_user_collections(user_id):
    try:
        connection = psycopg2.connect(
            host=config.PSQL_HOST,
            user=config.PSQL_USER,
            password=config.PSQL_PASSWORD,
            database=config.PSQL_DB_NAME,
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM Collections WHERE UserID = %s
            """, (user_id,))
            user_collections = cursor.fetchall()
            return user_collections

    except psycopg2.Error as error:
        print("Ошибка при работе с PostgreSQL:", error)
        return None

    finally:
        if connection:
            connection.close()


def init_archivist_database():
    
    try:
        # connect to exist db
        connection = psycopg2.connect(
            host=config.PSQL_HOST,
            user=config.PSQL_USER,
            password=config.PSQL_PASSWORD,
            database=config.PSQL_DB_NAME,
        )

        # the cursor for performing database operations
        # curson = connection.cursor()

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            print(f"Server version: {cursor.fetchone()}")
            
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TYPE FileType AS ENUM ('image', 'audio', 'video')
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    UserID SERIAL PRIMARY KEY,
                    Username VARCHAR(50) NOT NULL
                    -- Другие поля пользователя
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Collections (
                    CollectionID SERIAL PRIMARY KEY,
                    UserID INT REFERENCES Users(UserID),
                    AuthorUsername VARCHAR(50) NOT NULL,
                    CreationDate DATE
                    -- Другие поля коллекции
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Notes (
                    NoteID SERIAL PRIMARY KEY,
                    CollectionID INT REFERENCES Collections(CollectionID),
                    UserID INT REFERENCES Users(UserID),
                    NoteText TEXT,
                    ParentNoteID INT,
                    CreationDate DATE,
                    LastModifiedDate DATE
                    -- Другие поля заметки
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS NoteFiles (
                    FileID SERIAL PRIMARY KEY,
                    NoteID INT REFERENCES Notes(NoteID),
                    FileType FileType
                    -- Другие поля файлов заметки
                )
            """)
            
        # Подтверждение изменений в базе данных
        connection.commit()     
        #     # connection.commit()
        #     print("[INFO] Table created successfully")
            
        # insert data into a table
        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         """INSERT INTO users (first_name, nick_name) VALUES
        #         ('Oleg', 'barracuda');"""
        #     )
            
        #     print("[INFO] Data was succefully inserted")
            
        # get data from a table
        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         """SELECT nick_name FROM users WHERE first_name = 'Oleg';"""
        #     )
            
        #     print(cursor.fetchone())
            
        # delete a table
        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         """DROP TABLE users;"""
        #     )
            
        #     print("[INFO] Table was deleted")
    except Exception as _ex:
        print("[INFO] Error while launching PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

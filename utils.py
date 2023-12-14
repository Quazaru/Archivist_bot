import config
import psycopg2

def add_note(collection_name, user_id, note_text, name="Untilted"):
    try:
        connection = psycopg2.connect(
            host=config.PSQL_HOST,
            user=config.PSQL_USER,
            password=config.PSQL_PASSWORD,
            database=config.PSQL_DB_NAME,
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Notes (CollectionID, UserID, NoteText, Name)
                SELECT 
                    COALESCE((SELECT CollectionID FROM Collections WHERE Name = %s LIMIT 1), 1) AS CollectionID,
                    %s,
                    %s,
                    %s
                ON CONFLICT DO NOTHING;
            """, (collection_name, user_id, note_text, name))

        connection.commit()
        print("Note added successfully!")

    except psycopg2.Error as error:
        print("Error adding note:", error)

    finally:
        if connection:
            connection.close()

def get_collections_by_name(collection_name):
    try:
        connection = psycopg2.connect(
            host=config.PSQL_HOST,
            user=config.PSQL_USER,
            password=config.PSQL_PASSWORD,
            database=config.PSQL_DB_NAME,
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM Collections WHERE Name = %s
            """, (collection_name,))
            collections = cursor.fetchall()
            return collections

    except psycopg2.Error as error:
        print("Error fetching collections:", error)
        return None

    finally:
        if connection:
            connection.close()

def get_collection_list(user_id):
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
            collections = cursor.fetchall()
            return collections

    except psycopg2.Error as error:
        print("Error fetching collections:", error)
        return None

    finally:
        if connection:
            connection.close()

def get_notes(collection_id):
    try:
        connection = psycopg2.connect(
            host=config.PSQL_HOST,
            user=config.PSQL_USER,
            password=config.PSQL_PASSWORD,
            database=config.PSQL_DB_NAME,
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM Notes WHERE CollectionID = %s
            """, (collection_id,))
            notes = cursor.fetchall()
            return notes

    except psycopg2.Error as error:
        print("Error fetching notes:", error)
        return None

    finally:
        if connection:
            connection.close()

def init_archivist_database():
    try:
        # connect to existing db
        connection = psycopg2.connect(
            host=config.PSQL_HOST,
            user=config.PSQL_USER,
            password=config.PSQL_PASSWORD,
            database=config.PSQL_DB_NAME,
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT version();
            """)
            print(f"Server version: {cursor.fetchone()}")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Collections (
                    CollectionID SERIAL PRIMARY KEY,
                    UserID VARCHAR(50) NOT NULL,
                    Name VARCHAR(50) NOT NULL
                );

                CREATE TABLE IF NOT EXISTS Notes (
                    NoteID SERIAL PRIMARY KEY,
                    CollectionID INT REFERENCES Collections(CollectionID),
                    UserID VARCHAR(50) NOT NULL,
                    NoteText TEXT,
                    Name VARCHAR(50) NOT NULL
                );

                INSERT INTO Collections (UserID, Name)
                VALUES ('1', 'Base Collection');
                        
            """)

        connection.commit()
        print("[INFO] Tables created successfully")
    except Exception as _ex:
        print("[INFO] Error while launching PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

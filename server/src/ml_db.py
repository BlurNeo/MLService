import sqlite3
from sqlite3 import Error

create_metadata_table = """
CREATE TABLE IF NOT EXISTS metadata (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  model_version TEXT NOT NULL,
  model_path TEXT NOT NULL
);
"""

create_history_table = """
CREATE TABLE IF NOT EXISTS history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  model_version TEXT NOT NULL,
  picture_path TEXT NOT NULL,
  result TEXT NOT NULL
);
"""

class MLDataBase(object):
    def __init__(self, db_path):
        self._connection = None
        try:
            self._connection = sqlite3.connect(db_path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        self._execute_write_query(create_metadata_table)
        self._execute_write_query(create_history_table)
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._connection.close()

    def _execute_write_query(self, query):
        cursor = self._connection.cursor()
        try:
            cursor.execute(query)
            self._connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def _execute_read_query(self, query, only_latest = False):
        cursor = self._connection.cursor()
        result = None
        try:
            cursor.execute(query)
            if only_latest:
                # TODO: makesure this fetches the latest not the earliest
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def insert_metadata(self, model_version, model_path):
        metadata = """
        INSERT INTO
            metadata (model_version, model_path)
        VALUES 
        """
        # TODO: use %s to replace string
        metadata = metadata + '(\''+ model_version + '\',' + '\'' + model_path + '\');'
        self._execute_write_query(metadata)

    def insert_history(self, model_version, picture_path, result):
        history = """
        INSERT INTO
            history (model_version, picture_path, result)
        VALUES 
        """
        # TODO: use %s to replace string
        history = history + '(\''+ model_version + '\',' + '\'' + picture_path + '\'' + result + '\');'
        self._execute_write_query(history)

    def query_metadata(self):
        select = "SELECT * from metadata"
        return self._execute_read_query(select)

    def query_history(self):
        select = "SELECT * from history"
        return self._execute_read_query(select)
    
    def query_latest_model_info(self):
        select = "SELECT * from metadata"
        # select = ("SELECT model_version,model_path from metadata")
        # TODO: convert str to dict
        return self._execute_read_query(select)

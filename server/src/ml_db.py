import os
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

    def _execute_read_query(self, query):
        cursor = self._connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def _tupleList2metaDataList(self, tuple_list):
        metadata_list = []
        for i in range(len(tuple_list)):
            tup = tuple_list[i]
            dic = {}
            dic['model_version'] = tup[1]
            dic['model_path'] = tup[2]
            metadata_list.append(dic)
        return metadata_list
    
    def _tupleList2historyList(self, tuple_list):
        history_list = []
        for i in range(len(tuple_list)):
            tup = tuple_list[i]
            dic = {}
            dic['model_version'] = tup[1]
            dic['picture_path'] = tup[2]
            dic['result'] = tup[3]
            history_list.append(dic)
        return history_list

    def insert_metadata(self, model_version, model_path):
        metadata = 'INSERT INTO metadata (model_version, model_path) VALUES (\'%s\', \'%s\');' % (model_version, model_path)
        self._execute_write_query(metadata)

    def insert_history(self, model_version, picture_path, result):
        history = 'INSERT INTO history (model_version, picture_path, result) VALUES (\'%s\', \'%s\', \'%s\');' % (model_version, picture_path, result)
        self._execute_write_query(history)

    def query_metadata(self):
        select = "SELECT * from metadata"
        tuple_list = self._execute_read_query(select)
        return self._tupleList2metaDataList(tuple_list)
        
    def query_history(self):
        select = "SELECT * from history"
        tuple_list = self._execute_read_query(select)
        return self._tupleList2historyList(tuple_list)
    
    def query_latest_model_info(self, top_n = 2):
        # select = "SELECT * from metadata WHERE id = (SELECT MAX(id) from metadata)"
        select = "SELECT * FROM metadata ORDER BY id DESC LIMIT %d" % top_n
        tuple_list = self._execute_read_query(select)
        metadata_list = self._tupleList2metaDataList(tuple_list)
        # make sure there is at least one model info is returned
        assert(len(metadata_list) >= 1)
        # make sure there is at least top_n model info are returned
        if len(metadata_list) < top_n:
            metadata_list.append(metadata_list[-1])
        return metadata_list

import threading
import time
if __name__ == "__main__":
    def worker():
        while True:
            with MLDataBase('/Users/ssc/Desktop/workspace/git_repos/MLService/db/ml.db') as db:
                print(db.insert_metadata('1', 'this is a path'))
                print(db.insert_metadata('2', 'this is a path'))
                print(db.insert_metadata('3', 'this is a path'))
                print(db.insert_metadata('4', 'this is a path'))
                print(db.insert_metadata('5', 'this is a path'))
                # print(db.query_metadata())
                print(db.query_latest_model_info(2))
            time.sleep(1)
    t1 = threading.Thread(target=worker)
    t2 = threading.Thread(target=worker)
    t1.start()
    t2.start()

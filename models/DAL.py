import os
import psycopg2 as psql

class DAL:
    def __init__(self):
        self.__connection_string = os.environ.get('AIVEN_SERVICE_URI')

        assert type(self.__connection_string) == str        
    
    def _psql_fetchall(self, query: str, params: tuple = None):
        conn = psql.connect(self.__connection_string)
        cur = conn.cursor()
        
        cur.execute(query, params)

        records = cur.fetchall()
        return records
    
    def _psql_fetchone(self, query: str, params: tuple = None):
        conn = psql.connect(self.__connection_string)
        cur = conn.cursor()
        
        cur.execute(query, params)

        records = cur.fetchone()
        return records
    
    def _psql_fetchone(self, query: str, params: list = None):
        conn = psql.connect(self.__connection_string)
        cur = conn.cursor()
        
        cur.execute(query, params)

        records = cur.fetchone()
        return records
    
    def _psql_execute_and_commit(self, query: str, params: list = None):
        conn = psql.connect(self.__connection_string)
        cur = conn.cursor()
        
        cur.execute(query, params)
        conn.commit()
import os
import psycopg2 as psql

def psql_fetchall(query: str, params: list = None):
    connection_string = os.environ.get('AIVEN_SERVICE_URI')
    assert type(connection_string) == str

    conn = psql.connect(connection_string)
    cur = conn.cursor()
    
    cur.execute(query, params)

    records = cur.fetchall()
    return records

def psql_fetchone(query: str, params: list = None):
    connection_string = os.environ.get('AIVEN_SERVICE_URI')
    assert type(connection_string) == str
    
    conn = psql.connect(connection_string)
    cur = conn.cursor()
    
    cur.execute(query, params)

    records = cur.fetchone()
    return records

def psql_execute_and_commit(query: str, params: list = None):
    connection_string = os.environ.get('AIVEN_SERVICE_URI')
    assert type(connection_string) == str
    
    conn = psql.connect(connection_string)
    cur = conn.cursor()
    
    cur.execute(query, params)
    conn.commit()
    
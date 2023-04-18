import psycopg2
from psycopg2 import pool
from page_analyzer.settings import DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME


def create_connection(*args, **kwargs):
    """Create connection for work with PostgresSQL"""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME)


def create_pool(min_conn=1, max_conn=5):
    """Create connection for work with PostgresSQL"""
    return pool.SimpleConnectionPool(minconn=min_conn,
                                     maxconn=max_conn,
                                     connection_factory=create_connection,
                                     host=DB_HOST,
                                     port=DB_PORT,
                                     user=DB_USER,
                                     password=DB_PASS,
                                     database=DB_NAME)


conn_pool = create_pool()

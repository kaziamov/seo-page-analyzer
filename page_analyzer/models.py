import psycopg2
from page_analyzer.settings import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from datetime import datetime


class Database:
    def __init__(self) -> None:
        self.connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME)
        try:
            self.cursor = self.connection.cursor()
        except psycopg2.OperationalError:
            print('Can`t establish connection to database')

    def create_new_db(self):
        # self.take_command("""CREATE TABLE urls (id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY, name varchar(255), created_at TIMESTAMP)""")
        return self

    def add_new_url(self, url):
        self.cursor.execute('''INSERT INTO urls (name, created_at) VALUES (%s, %s) ;''', (url, datetime.now()))
        # self.cursor.execute(f'''INSERT INTO urls (name, created_at) VALUES ('{url}', '{datetime.now()}')''')
        self.connection.commit()
        return self

    def is_url_exist(self, url):
        self.cursor.execute("""SELECT * FROM urls WHERE name=%s ;""", (url, ))
        response = self.cursor.fetchone()
        self.connection.commit()
        if response:
            return response[0]
        return False

    def get_data_by_id(self, id):
        self.cursor.execute("""SELECT * FROM urls WHERE id=%s ;""", (id, ))
        return self.cursor.fetchone()

    def get_all_urls(self):
        self.cursor.execute("""SELECT * FROM urls ORDER BY created_at DESC ;""")
        return self.cursor.fetchall()

    def is_checks_exist(self, id):
        self.cursor.execute("""SELECT * FROM url_checks WHERE url_id=%s ;""", (id, ))
        response = self.cursor.fetchone()
        self.connection.commit()
        if response:
            return True
        return False

    def get_checks_by_id(self, id):
        self.cursor.execute("""SELECT * FROM url_checks WHERE url_id=%s ORDER BY created_at DESC ;""", (id, ))
        return self.cursor.fetchall()

    def add_new_check(self, url_id, status_code, h1, title, description):
        self.cursor.execute('''INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s) ;''', (url_id, status_code, h1, title, description, datetime.now()))
        self.connection.commit()
        return self

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

    def create_cursor(self):
        try:
            self.cursor = self.connection.cursor()
        except psycopg2.OperationalError:
            return self.create_cursor()
        return self

    def delete_all_data(self):
        self.create_cursor()
        self.cursor.execute("""DROP TABLE url_checks ;""")
        self.cursor.execute("""DROP TABLE urls ;""")
        return self

    def create_new_db(self):
        # self.cursor.execute("""CREATE TABLE urls (id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY, name varchar(255), created_at TIMESTAMP)""")
        return self

    def add_new_url(self, url):
        self.create_cursor()
        self.cursor.execute('''INSERT INTO urls (name, created_at) VALUES (%s, %s) ;''', (url, datetime.now()))
        # self.cursor.execute(f'''INSERT INTO urls (name, created_at) VALUES ('{url}', '{datetime.now()}')''')
        self.connection.commit()
        return self

    def is_url_exist(self, url):
        self.create_cursor()
        self.cursor.execute("""SELECT * FROM urls WHERE name=%s ;""", (url, ))
        response = self.cursor.fetchone()
        self.connection.commit()
        if response:
            return response[0]
        return False

    def get_data_by_id(self, id):
        self.create_cursor()
        self.cursor.execute("""SELECT * FROM urls WHERE id=%s ;""", (id, ))
        return self.cursor.fetchone()

    def get_all_urls(self):
        self.create_cursor()
        self.cursor.execute("""SELECT urls.id, urls.name, url_checks.created_at, url_checks.status_code
                            FROM urls LEFT JOIN (
                                SELECT DISTINCT ON (url_id) url_id, created_at, status_code
                                FROM url_checks
                                ORDER BY url_id, created_at DESC) AS url_checks ON urls.id = url_checks.url_id
                            ORDER BY urls.id DESC ;""")
        return self.cursor.fetchall()

    def get_all_time_checks(self):
        self.create_cursor()
        self.cursor.execute("""SELECT created_at FROM url_checks ORDER BY id DESC ;""")
        return self.cursor.fetchall()

    def is_checks_exist(self, id):
        self.create_cursor()
        self.cursor.execute("""SELECT * FROM url_checks WHERE url_id=%s ;""", (id, ))
        response = self.cursor.fetchone()
        self.connection.commit()
        if response:
            return True
        return False

    def get_checks_by_id(self, id):
        self.create_cursor()
        self.cursor.execute("""SELECT * FROM url_checks WHERE url_id=%s ORDER BY created_at DESC ;""", (id, ))
        return self.cursor.fetchall()

    def add_new_check(self, url_id, status_code, h1, title, description):
        self.create_cursor()
        self.cursor.execute('''INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s) ;''', (url_id, status_code, h1, title, description, datetime.now()))
        self.connection.commit()
        return self

import psycopg2
from page_analyzer.settings import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from datetime import datetime


class Database:
    def __init__(self) -> None:
        self.connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_NAME,
            password=DB_USER,
            database=DB_PASS)
        try:
            self.cursor = self.connection.cursor()
        except:
            print('Can`t establish connection to database')

    def create_new_db(self):
        # self.take_command("""CREATE TABLE urls (id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY, name varchar(255), created_at TIMESTAMP)""")
        return self

    def add_new_url(self, url):
        self.cursor.execute(f'''INSERT INTO urls (name, created_at) VALUES ('{url}', '{datetime.now()}')''')
        self.connection.commit()
        return self

    def is_url_exist(self, url):
        self.cursor.execute(f"""SELECT * FROM urls WHERE name='{url}'""")
        response = self.cursor.fetchone()
        self.connection.commit()
        if response:
            return response[0]
        return False

    def get_data(self, command):
        self.cursor.execute(command)
        return self.cursor.fetchone()

    def get_all_urls(self):
        self.cursor.execute("""SELECT * FROM urls ORDER BY created_at DESC""")
        return self.cursor.fetchall()

# if __name__ == '__main__':
#     d = Database()
#     d.create_new_db().take_command("""INSERT INTO urls VALUES (1, "https://example/1", 2022-01-01);""")
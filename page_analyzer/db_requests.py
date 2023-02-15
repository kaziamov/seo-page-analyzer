import psycopg2
from settings import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


class Database:
    def __init__(self) -> None:
        self.connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_NAME,
            password=DB_USER,
            database=DB_PASS)
        self.cursor = self.connection.cursor()

    def _create_new_db(self):
        self.take_command("""CREATE TABLE urls (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name varchar(255),
    created_at TIMESTAMP
    )""")

    def take_command(self, command):
        self.cursor.execute(command)
        self.connection.commit()
        return self


if __name__ == '__main__':
    d = Database()
    d.take_command()

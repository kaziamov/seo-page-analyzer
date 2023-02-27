import psycopg2
from page_analyzer.settings import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from datetime import datetime


def make_connection():
    """Create connection for work with PostgresSQL"""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME)


def add_new_url(url):
    """Create new name in database from url and return """
    c = make_connection()
    cursor = c.cursor()
    cursor.execute('''INSERT INTO urls (name, created_at) VALUES (%s, %s) ;''', (url, datetime.now()))
    c.commit()
    c.close()


def is_url_exist(url):
    """Check exist url in database and return ID or False"""
    c = make_connection()
    cursor = c.cursor()
    cursor.execute("""SELECT * FROM urls WHERE name=%s ;""", (url, ))
    response = cursor.fetchone()
    c.commit()
    c.close()
    if response:
        return response[0]
    return False


def get_data_by_id(id):
    """Return all column for selected ID"""
    c = make_connection()
    cursor = c.cursor()
    cursor.execute("""SELECT * FROM urls WHERE id=%s ;""", (id, ))
    result = cursor.fetchone()
    c.close()
    return result


def get_all_urls():
    """Return id, name, last check data and status code for selected id"""
    c = make_connection()
    cursor = c.cursor()
    cursor.execute("""SELECT urls.id, urls.name, url_checks.created_at, url_checks.status_code
                        FROM urls LEFT JOIN (
                            SELECT DISTINCT ON (url_id) url_id, created_at, status_code
                            FROM url_checks
                            ORDER BY url_id, created_at DESC) AS url_checks ON urls.id = url_checks.url_id
                        ORDER BY urls.id DESC ;""")
    result = cursor.fetchall()
    c.close()
    return result


def is_checks_exist(id):
    """Check if exist and return bool"""
    c = make_connection()
    cursor = c.cursor()
    cursor.execute("""SELECT * FROM url_checks WHERE url_id=%s ;""", (id, ))
    response = cursor.fetchone()
    c.commit()
    c.close()
    if response:
        return True
    return False


def get_checks_by_id(id):
    """Return all checks for selected id"""
    c = make_connection()
    cursor = c.cursor()
    cursor.execute("""SELECT id, status_code, h1, title, description, created_at FROM url_checks WHERE url_id=%s ORDER BY id DESC ;""", (id, ))
    result = cursor.fetchall()
    c.commit()
    c.close()
    return result


def add_new_check(url_id, status_code, h1, title, description):
    """Add check data to db"""
    c = make_connection()
    cursor = c.cursor()
    cursor.execute('''INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s) ;''', (url_id, status_code, h1, title, description, datetime.now()))
    c.commit()
    c.close()

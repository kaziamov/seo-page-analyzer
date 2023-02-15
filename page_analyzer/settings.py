import dotenv
import os

env_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv()
e = os.environ.get

DB_HOST = e('DB_HOST')
DB_PORT = e('DB_PORT')
DB_NAME = e('DB_NAME')
DB_USER = e('DB_USER')
DB_PASS = e('DB_PASS')
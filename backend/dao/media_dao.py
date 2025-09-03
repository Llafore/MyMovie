import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


class MediaDAO(object):
    def __init__(self):
        self.config = {
            'host': os.getenv("DB_HOST"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'database': os.getenv("DB_NAME")
        }

    def _connect(self):
        return mysql.connector.connect(**self.config)
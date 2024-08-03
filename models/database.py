import mysql.connector
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
    
    def get_connection(self):
        return self.connection
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def __del__(self):
        self.close()

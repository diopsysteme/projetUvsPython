from models.database import Database
import mysql.connector

class Inscription:
    def __init__(self):
        self.db = Database()
    
    def add(self, nom, prenom, email, telephone):
        connection = self.db.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO inscriptions (nom, prenom, email, telephone) VALUES (%s, %s, %s, %s)",
                           (nom, prenom, email, telephone))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def all(self):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM inscriptions")
            inscriptions = cursor.fetchall()
            return inscriptions
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()

    def find_by(self, field, value):
        connection = self.db.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(f"SELECT * FROM inscriptions WHERE {field} = %s", (value,))
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
       


    def update(self, id, nom, prenom, email, telephone):
        connection = self.db.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE inscriptions SET nom=%s, prenom=%s, email=%s, telephone=%s WHERE id=%s",
                           (nom, prenom, email, telephone, id))
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def __del__(self):
        self.db.close()
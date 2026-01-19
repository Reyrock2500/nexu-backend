import sqlite3
import os

database_file = os.getenv("DB_PATH")

def create_db():
    with sqlite3.connect(database_file) as connection:
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        ); 
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            brand_id INTEGER,
            FOREIGN KEY (brand_id) REFERENCES brands(id)
        ); 
        ''')
        connection.commit()


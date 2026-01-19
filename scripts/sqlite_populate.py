import os
import sqlite3
import json
import sys


database_file = os.getenv("DB_PATH")
json_models = os.getenv("JSON_PATH")

def create_db():
    """
    Creates the database tables and populates them with data from the JSON file.
    """
    try:
        with sqlite3.connect(database_file) as connection:
            cursor = connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS brands;")
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS brands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            ); 
            ''')
            cursor.execute("DROP TABLE IF EXISTS models;")
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                average_price INTEGER,
                brand_id INTEGER,
                FOREIGN KEY (brand_id) REFERENCES brands(id)
            ); 
    ''')
            connection.commit()
    except sqlite3.Error as e:
        print (f"Somehow the DB creation died:\n{e}")
        sys.exit(1) # No point in carrying on really
    
    try:
        with open(json_models, 'r', encoding='utf-8') as jm:
            j_data: dict = json.load(jm)

            isolated_brands = {item['brand_name'] for item in j_data if 'brand_name' in item}
            
            hash_mapcito = {}

            for brand in sorted(isolated_brands):
                cursor.execute("""INSERT INTO brands(name) VALUES(?)""", (brand,))
                hash_mapcito[brand] = cursor.lastrowid # map {"brand": id}
            connection.commit()

            for model in j_data:
                brand_name = model["brand_name"]
                brand_id = hash_mapcito.get(brand_name)
                cursor.execute("""INSERT INTO models(id,name,average_price,brand_id)
                            VALUES (?,?,?,?)""",
                            (model['id'], model['name'], model['average_price'], brand_id))
            connection.commit()
    except sqlite3.Error as e:
        print (f"Somehow the DB population died :(\n{e}")
        sys.exit(1) # No info to continue whatsoever

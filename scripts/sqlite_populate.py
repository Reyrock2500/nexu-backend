import sqlite3
import os
import json


database_file = os.getenv("DB_PATH")
json_models = os.getenv("JSON_PATH")

def create_db():
    print("hello")
    try:
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
                average_price INTEGER,
                brand_id INTEGER,
                FOREIGN KEY (brand_id) REFERENCES brands(id)
            ); 
            ''')
            connection.commit()
    except Exception as e:
        print (f"Somehow the DB creation died:\n{e}")
        exit(1) # No point in carrying on really
    
    try:
        with open(json_models, 'r') as jm:
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
                            VALUES (?,?,?,?)""", (model['id'], model['name'], model['average_price'], brand_id))
            connection.commit()

            cursor.execute("SELECT * FROM models")
            models = cursor.fetchall()
            for model in models:
                print(model)
            cursor.execute("SELECT * FROM brands")
            models = cursor.fetchall()
            for model in models:
                print(model)
    except Exception as e:
        print (f"Somehow the DB population died :(\n{e}")
        exit(1) # No info to continue whatsoever

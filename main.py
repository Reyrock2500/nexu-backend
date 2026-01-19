from fastapi import FastAPI
from scripts import sqlite_populate
import os
import sqlite3
import json

app = FastAPI()
sqlite_populate.create_db()
database_file = os.getenv("DB_PATH")


@app.get("/")
async def test():
    return {"mensaje": "Hello World :DDD"}


@app.get("/models")
async def models():
    with sqlite3.connect(database_file) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT COUNT(*) FROM models")
        models = cursor.fetchone()
        
    print("Here models")
    return {"total": models}

@app.get("/brands")
async def brands():
    brands_json = []
    with sqlite3.connect(database_file) as connect:
        cursor = connect.cursor()
        cursor.execute("""
        SELECT b.id, b.name, ROUND(AVG(m.average_price), 2) FROM brands b
        JOIN models m on m.brand_id = b.id
        GROUP BY b.id, b.name;
                   """)
        brands = cursor.fetchall()
        for brand in brands:
            brand_id, brand_name, average_price = brand
            brands_json.append( {
            "id": brand_id,
            "name": brand_name,
            "average_price": average_price
            })
    return brands_json


@app.get("/brands/{id}/models")
def list_brand_models(id: int):
    models_per_brand = []
    with sqlite3.connect(database_file) as connect:
        cursor = connect.cursor()
        cursor.execute("""
        SELECT m.id, m.name, m.average_price FROM models m
        JOIN brands b ON m.brand_id = b.id
        WHERE ? = b.id
        GROUP BY m.id;
      """, (id,))
        models_p_brand = cursor.fetchall()
        for model in models_p_brand:
            model_id, model_name, average_price = model
            models_per_brand.append( {
            "id": model_id,
            "name": model_name,
            "average_price": average_price
            })
    return models_per_brand
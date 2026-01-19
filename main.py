from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
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

class Brand(BaseModel):
    name: str

@app.post("/brands")
async def create_brand(brand: Brand):
    try:
        with sqlite3.connect(database_file) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO brands (name) VALUES (?)", (brand.name,))
            connection.commit()
            return {"id": cursor.lastrowid, "name": brand.name}
    except sqlite3.IntegrityError: #unique does the job
        raise HTTPException(status_code=400, detail="Brand already exists. Try again.")
    except Exception as e: # other tragedy
        raise HTTPException(status_code=500, detail=str(e))


class Model(BaseModel):
    name: str
    average_price: Optional[int] = Field(None, gt=100000)


@app.post("/brands/{id}/models")
async def create_model(id: int, model: Model):
    with sqlite3.connect(database_file) as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT id FROM brands WHERE id = ?", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Brand not found. Try again :D")
            
        cursor.execute("SELECT id FROM models WHERE brand_id = ? AND name = ?", (id, model.name))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Model name already exists for this brand. Try another one")

        try:
            cursor.execute("INSERT INTO models (name, average_price, brand_id) VALUES (?, ?, ?)", 
                           (model.name, model.average_price, id))
            connection.commit()
            return {
                "id": cursor.lastrowid, 
                "name": model.name, 
                "average_price": model.average_price, 
                "brand_id": id
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


class ModelUpdate(BaseModel):
    average_price: int = Field(..., gt=100000)


@app.put("/models/{id}")
async def update_model(id: int, model: ModelUpdate):
    with sqlite3.connect(database_file) as connection:
        cursor = connection.cursor()
        
        cursor.execute("SELECT id FROM models WHERE id = ?", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Model not found. Try again.")

        try:
            cursor.execute("UPDATE models SET average_price = ? WHERE id = ?", (model.average_price, id))
            connection.commit()
            return {"id": id, "average_price": model.average_price}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

import os
import sqlite3
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from scripts import sqlite_populate


app = FastAPI()
sqlite_populate.create_db()
database_file = os.getenv("DB_PATH")


@app.get("/")
async def test():
    """
    Health check endpoint.
    """
    return {"mensaje": "Hello World :DDD"}


@app.get("/models_qty")
async def models_qty():
    """
    Returns the total number of models in the database.
    """
    with sqlite3.connect(database_file) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT COUNT(*) FROM models")
        models = cursor.fetchone()

    print("Here models")
    return {"total": models}

@app.get("/brands")
async def brands():
    """
    Retrieves all brands with their average model price.
    """
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
    """
    Lists all models for a specific brand.
    """
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
    """
    Creates a new brand.
    """
    try:
        with sqlite3.connect(database_file) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO brands (name) VALUES (?)", (brand.name,))
            connection.commit()
            return {"id": cursor.lastrowid, "name": brand.name}
    except sqlite3.IntegrityError as e: #unique does the job
        raise HTTPException(status_code=400, detail="Brand already exists. Try again.") from e
    except Exception as e: # other tragedy
        raise HTTPException(status_code=500, detail=str(e)) from e


class Model(BaseModel):
    name: str
    average_price: Optional[int] = Field(None, gt=100000)
    
@app.post("/brands/{id}/models")
async def create_model(id: int, model: Model):
    """
    Creates a new model associated with a brand.
    """
    with sqlite3.connect(database_file) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM brands WHERE id = ?", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Brand not found. Try again :D")
            
        cursor.execute("SELECT id FROM models WHERE brand_id = ? AND name = ?", (id, model.name))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Model name already exists for this brand.")

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
            raise HTTPException(status_code=500, detail=str(e)) from e


class ModelUpdate(BaseModel):
    average_price: int = Field(..., gt=100000)
    
@app.put("/models/{id}")
async def update_model(id: int, model: ModelUpdate):
    """
    Updates the average price of a model.
    """
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
            raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/models")
async def get_models(greater: Optional[int] = None, lower: Optional[int] = None):
    """
    Retrieves models, optionally filtered by average price range.
    """
    sql = "SELECT id, name, average_price FROM models"
    filters = []
    args = []
    models = []

    # in can list all models if greater and lower not in the "query"
    if greater is not None:
        filters.append("average_price > ?")
        args.append(greater)
    
    if lower is not None:
        filters.append("average_price < ?")
        args.append(lower)

    if filters: # hardest part
        sql += " WHERE " + " AND ".join(filters) 
    sql += "ORDER BY average_price"
        
    with sqlite3.connect(database_file) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, args)
        for row in cursor.fetchall():
            model_id, model_name, average_price = row
            models.append({
            "id": model_id,
            "name": model_name,
            "average_price": average_price
            })
        data = models
        return data

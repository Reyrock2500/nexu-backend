from fastapi import FastAPI
from scripts import sqlite_populate
import os
import sqlite3

app = FastAPI()
sqlite_populate.create_db()
database_file = os.getenv("DB_PATH")


@app.get("/")
async def test():
    return {"mensaje": "Hello World :DDD"}


@app.get("/models")
async def brands():
    with sqlite3.connect(database_file) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT COUNT(*) FROM models")
        models = cursor.fetchone()
        
    print("Here models")
    return {"total": models}
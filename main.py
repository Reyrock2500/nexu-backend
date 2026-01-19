from fastapi import FastAPI
from scripts import sqlite_populate

app = FastAPI()
sqlite_populate.create_db()


@app.get("/")
async def test():
    return {"mensaje": "Hello World :DDD"}


@app.get("/brands")
async def brands():
    print("Here brands")
    return {"mensaje": "Hello World :DDD"}
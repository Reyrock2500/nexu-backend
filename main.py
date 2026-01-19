from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def test():
    return {"mensaje": "Hello World :DDD"}
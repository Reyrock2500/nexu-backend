import os
from fastapi.testclient import TestClient
from main import app

os.environ["DB_PATH"] = "test.db"
os.environ["JSON_PATH"] = "data/models.json"


client = TestClient(app)

def test_get_brands_check_acura():
    response = client.get("/brands")
    assert response.status_code == 200
    data = response.json()
    
    # Find Acura in the list
    acura = next((b for b in data if b["name"] == "Acura"), None)
    assert acura is not None
    assert acura["average_price"] == 702109.5

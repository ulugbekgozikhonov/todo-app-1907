from main import app
from fastapi.testclient import TestClient

client = TestClient(app)
def test_main():
	response = client.get("/ketmon")
	assert response.status_code == 200
	assert response.json() == {"status": "Salom Ketmon"}
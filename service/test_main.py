import json
from fastapi.testclient import TestClient
from cxwebhooks import WebhookResponse

from main import app

client = TestClient(app)

def payload(path: str):
    with open(path) as src:
        return json.load(src)

def test_verify_address():
    path = 'tests/verify-address.json'
    response = client.post("/verify-address", json=payload(path))
    assert response.status_code == 200
    model = WebhookResponse(**response.json())
    assert model.sessionInfo.parameters.get('place_id') == 'ChIJ_ef_q_Q10YkR-VlhFa9pS0Q'
    

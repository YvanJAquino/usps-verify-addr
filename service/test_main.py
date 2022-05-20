# Copyright 2022 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    

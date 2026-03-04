import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv('.env.tests.e2e.secret')

API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')
API_KEY = os.getenv('API_KEY', 'test')

@pytest.fixture
def client():
    class TestClient:
        def __init__(self):
            self.base_url = API_BASE_URL
            self.headers = {
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            }
        
        def get(self, path):
            url = f"{self.base_url}{path}"
            return requests.get(url, headers=self.headers)
    
    return TestClient()

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'secure'))
from app import app as secure_app

@pytest.fixture
def client():
    secure_app.config['TESTING'] = True
    secure_app.config['SECRET_KEY'] = 'test-secret-key'
    with secure_app.test_client() as client:
        yield client

def test_sql_injection_blocked(client):
    response = client.post('/login', json={
        "username": "admin' OR '1'='1",
        "password": "anything"
    })
    assert response.status_code == 401

def test_admin_requires_auth(client):
    response = client.get('/admin/users')
    assert response.status_code == 401

def test_order_requires_auth(client):
    response = client.post('/order', json={"product_id": 1, "quantity": 1})
    assert response.status_code == 401

def test_password_validation(client):
    response = client.post('/register', json={"username": "user", "password": "123"})
    assert response.status_code == 400

def test_input_validation_blocks_negative_quantity(client):
    client.post('/register', json={"username": "buyer", "password": "SecurePass123!"})
    login = client.post('/login', json={"username": "buyer", "password": "SecurePass123!"})
    token = login.get_json()["token"]
    
    response = client.post('/order',
        json={"product_id": 1, "quantity": -5},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vulnerable'))
from app import app as vulnerable_app

@pytest.fixture
def client():
    vulnerable_app.config['TESTING'] = True
    with vulnerable_app.test_client() as client:
        yield client

def test_sql_injection_login_bypass(client):
    """A03: SQL Injection allows authentication bypass"""
    response = client.post('/login', json={
        "username": "admin' OR '1'='1",
        "password": "anything"
    })
    assert response.status_code == 200

def test_admin_access_without_auth(client):
    """A01: Broken Access Control — no auth required"""
    response = client.get('/admin/users')
    assert response.status_code == 200

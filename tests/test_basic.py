"""Tests for WMS Operacional API."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "WMS Operacional API"


def test_health():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_product():
    """Test product creation."""
    product_data = {
        "name": "Camiseta Algodão P",
        "sku": "CAM-P001",
        "ean": "7891234000001",
        "price": 29.90,
        "quantity": 150,
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Camiseta Algodão P"
    assert data["sku"] == "CAM-P001"
    assert data["ean"] == "7891234000001"


def test_create_user():
    """Test user creation."""
    user_data = {
        "username": "testuser",
        "email": "test@wms.com",
        "full_name": "Test User",
        "password": "testpass123",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_create_order():
    """Test order creation."""
    # First create a product
    product_data = {
        "name": "Produto Teste",
        "sku": "PRO-TST",
        "ean": "7891234000099",
        "price": 10.00,
        "quantity": 50,
    }
    client.post("/products/", json=product_data)
    
    # Create order
    order_data = {
        "user_id": 1,
        "items": [{"product_id": 1, "quantity": 2}],
        "shipping_address": "Test Address",
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"
    assert data["total_amount"] == 20.00
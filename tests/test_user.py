from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_user():
    """Проверка получения пользователя по email"""
    response = client.get("/api/v1/user", params={'email': 'i.i.ivanov@mail.com'})
    assert response.status_code == 200
    assert response.json()['name'] == 'Ivan Ivanov'

    response = client.get("/api/v1/user", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user():
    """Проверка создания нового пользователя"""
    new_user = {
        'name': 'Alexey Alexandrov',
        'email': 'a.a.alexandrov@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert response.json() == 3  # ID нового пользователя

    # Проверяем, что новый пользователь действительно создан
    response = client.get("/api/v1/user", params={'email': 'a.a.alexandrov@mail.com'})
    assert response.status_code == 200
    assert response.json()['name'] == 'Alexey Alexandrov'

def test_create_user_with_duplicate_email():
    """Проверка попытки создать пользователя с уже занятой почтой"""
    existing_user = {
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com'
    }
    response = client.post("/api/v1/user", json=existing_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    """Проверка удаления пользователя"""
    response = client.delete("/api/v1/user", params={'email': 'i.i.ivanov@mail.com'})
    assert response.status_code == 204

    # Проверяем, что пользователь был удалён
    response = client.get("/api/v1/user", params={'email': 'i.i.ivanov@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

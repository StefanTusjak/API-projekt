import requests
import uuid

BASE_URL = "http://127.0.0.1:8000"

def generate_email(name):
    return f"{name}_{uuid.uuid4().hex[:6]}@example.com"

def test_get_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("✅ test_get_users OK")

def test_create_user():
    new_user = {"jmeno": "Test User", "email": generate_email("test")}
    response = requests.post(f"{BASE_URL}/users", json=new_user)
    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert "id" in data
    print("✅ test_create_user OK")
    return data["id"]

def test_create_user_empty_fields():
    response = requests.post(f"{BASE_URL}/users", json={"jmeno": "", "email": ""})
    assert response.status_code == 400
    assert "error" in response.json()
    print("✅ test_create_user_empty_fields OK")

def test_create_user_invalid_email():
    response = requests.post(f"{BASE_URL}/users", json={"jmeno": "Neplatný", "email": "neplatnyemail"})
    assert response.status_code == 400
    assert "error" in response.json()
    print("✅ test_create_user_invalid_email OK")

def test_create_user_duplicate_email():
    email = generate_email("duplicitni")
    new_user = {"jmeno": "Duplicitní", "email": email}
    r1 = requests.post(f"{BASE_URL}/users", json=new_user)
    assert r1.status_code == 201
    r2 = requests.post(f"{BASE_URL}/users", json=new_user)
    assert r2.status_code == 409
    assert "error" in r2.json()
    print("✅ test_create_user_duplicate_email OK")
    return r1.json()["id"]

def test_update_user_duplicate_email():
    email1 = generate_email("usera")
    email2 = generate_email("userb")

    user1 = {"jmeno": "User A", "email": email1}
    user2 = {"jmeno": "User B", "email": email2}

    r1 = requests.post(f"{BASE_URL}/users", json=user1)
    r2 = requests.post(f"{BASE_URL}/users", json=user2)

    id1 = r1.json()["id"]
    id2 = r2.json()["id"]

    # Pokusíme se změnit uživatele B tak, aby měl e-mail jako A
    response = requests.put(f"{BASE_URL}/users/{id2}", json={"jmeno": "User B", "email": email1})
    assert response.status_code == 409
    print("✅ test_update_user_duplicate_email OK")

def delete_user_by_id(user_id):
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Uživatel smazán"
    print(f"✅ test_delete_user (id {user_id}) OK")

if __name__ == "__main__":
    test_get_users()
    test_create_user_empty_fields()
    test_create_user_invalid_email()

    id1 = test_create_user()
    id2 = test_create_user()
    delete_user_by_id(id1)
    delete_user_by_id(id2)

    dup_id = test_create_user_duplicate_email()
    delete_user_by_id(dup_id)

    test_update_user_duplicate_email()

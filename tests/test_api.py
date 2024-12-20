import pytest
import requests
import allure
from conftest import BASE_URL

class TestEndpointsAPI:
    @allure.story("Проверка получения пользователя с разными ID")
    @allure.title("Проверка статуса ответа")
    @pytest.mark.parametrize("user_id, expected_status", [
        (2, 200),
        (9999, 404)
    ])
    def test_get_user_status(self, user_id, expected_status):    #Проверка получения пользователя с разными ID
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        assert response.status_code == expected_status
        if expected_status == 200:
            assert "data" in response.json()
        else:
            assert response.json() == {}

    @allure.story("Создание нового пользователя")
    @allure.title("Проверка успешного создания пользователя")
    def test_create_user_positive(self, user_payload):          #Проверка успешного создания пользователя.
        response = requests.post(f"{BASE_URL}/users", json=user_payload)
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["name"] == user_payload["name"]
        assert response_data["job"] == user_payload["job"]

    @allure.story("Проверка логина с разными параметрами")
    @allure.title("Проверка авторизации")
    @pytest.mark.parametrize("payload, expected_status, token_check", [
        ({"email": "eve.holt@reqres.in", "password": "cityslicka"}, 200, True),
        ({"email": "eve.holt@reqres.in"}, 400, False)
    ])
    def test_login(self, payload, expected_status, token_check):        #Проверка логина с разными параметрами.
        response = requests.post(f"{BASE_URL}/login", json=payload)
        assert response.status_code == expected_status
        response_data = response.json()
        if token_check:
            assert "token" in response_data
        else:
            assert response_data["error"] == "Missing password"

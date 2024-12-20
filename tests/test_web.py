import json
import allure
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import BASE_URL
from locators import PageObject_locator

class TestWebElementsMainPage:
    @allure.story("Сравнение данных API и веб-формы")
    @allure.title("Проверка равенства полученных данных")
    def test_web_api_consistency(self, driver):         # Сравнение данных API и веб-формы

        # Получаем данные через API
        api_response = requests.get(f"{BASE_URL}/users/2")
        assert api_response.status_code == 200, "Ошибка: API запрос вернул неверный статус-код."
        api_user_data = api_response.json().get("data", {})
        assert api_user_data, "Ошибка: Данные пользователя из API пустые."

        # Ищем и кликаем по кнопке для получения данных через веб-форму
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, PageObject_locator.BUTTON_SINGLE_USER))
        )
        driver.execute_script("arguments[0].scrollIntoView();", button)
        button.click()

        # Ожидаем появления данных пользователя в текстовом поле
        web_response_txt = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, PageObject_locator.TEXT_AREA))
        )
        web_user_data = json.loads(web_response_txt.text).get("data", {})
        assert web_user_data, "Ошибка: Данные пользователя из веб-формы пустые."

        # Ожидаем загрузки поля с кодом ответа
        web_response_code = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, PageObject_locator.CODE_AREA))
        )
        web_status_code = int(web_response_code.text)

        # Сравниваем данные API и веб-формы
        assert web_user_data == api_user_data, "Данные пользователя в API и веб-форме не совпадают."
        assert web_status_code == api_response.status_code, "Код API и веб-формы не совпадают."





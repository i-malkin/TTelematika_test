import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

BASE_URL = "https://reqres.in/api"
WEB_URL = "https://reqres.in/"


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="запуск браузера режиме без UI"
    )
@pytest.fixture(params=['Chrome', 'Firefox'], scope="class")
def driver(request):
    headless = request.config.getoption("--headless")                    # Получаем флаг из командной строки
    global driver

    if request.param == 'Firefox':
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument("--headless")                   # Запуск без UI
        firefox_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Firefox(options=firefox_options)
        driver.maximize_window()

    elif request.param == 'Chrome':
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")                       # Запуск без UI
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()

    driver.get(WEB_URL)
    yield driver
    driver.quit()

@pytest.fixture
def user_payload():
    """Фикстура для данных создания пользователя."""
    return {
        "name": "morpheus",
        "job": "leader"
    }

@pytest.fixture
def login_payload_success():
    """Фикстура для успешного логина."""
    return {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }

@pytest.fixture
def login_payload_unsuccess():
    """Фикстура для неуспешного логина."""
    return {
        "email": "eve.holt@reqres.in"
    }

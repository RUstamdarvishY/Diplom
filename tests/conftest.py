import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def get_chrome_options():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--start-maximized')
    return options


@pytest.fixture
def get_webdriver(get_chrome_options):
    options = get_chrome_options
    driver = webdriver.Chrome(
        executable_path='/home/rustam/selenium_drivers/chromedriver', options=options)
    driver.implicitly_wait(3)
    return driver


@pytest.fixture
def find_by():
    def do_find_by(selector: str):
        find_by = selector.lower()
        location = {
            'css': By.CSS_SELECTOR,
            'xpath': By.XPATH,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT,
            'class': By.CLASS_NAME,
            'id': By.ID,
            'tag': By.TAG_NAME,
            'name': By.NAME
        }
        return location[find_by]
    return do_find_by


@pytest.fixture
def wait_for(get_webdriver):
    def do_wait_for(element):
        driver = get_webdriver
        wait = WebDriverWait(driver, 3, 0.3)
        return wait.until(ec.visibility_of_element_located(element))
    return do_wait_for

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pytest_factoryboy import register
from django.contrib.auth.models import User
from tests.factories import UserFactory, ProfileFactory, PostFactory, CommentFactory


register(UserFactory)
register(ProfileFactory)
register(PostFactory)
register(CommentFactory)


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
    return driver


@pytest.fixture
def get_url(request, get_webdriver):
    def do_get_url(url):
        driver = get_webdriver
        driver.get(url)
        yield driver
        driver.quit()
    return do_get_url        
        
        
@pytest.fixture
def auth_user(client):
    def do_auth_user(is_staff=False):
        return client.force_authenticate(user=User(is_staff=is_staff))
    return do_auth_user

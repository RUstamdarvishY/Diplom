import pytest
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.auth.models import User


@pytest.fixture
def get_data():
    data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'QWErty123',
        'password2': 'QWErty123'
    }
    return data


class TestRegistration:

    @pytest.mark.django_db
    def test_register_user(self, get_data, get_webdriver, find_by):
        driver = get_webdriver
        driver.get('http://localhost:8000/register/')
        selector = find_by('id')
        wait = WebDriverWait(driver, 5, 0.3)
        username = wait.until(
            ec.visibility_of_element_located((selector, 'id_username')))
        email = wait.until(ec.visibility_of_element_located(
            (selector, 'id_email')))
        password = wait.until(
            ec.visibility_of_element_located((selector, 'id_password')))
        password2 = wait.until(
            ec.visibility_of_element_located((selector, 'id_password2')))

        username.send_keys(get_data['username'])
        email.send_keys(get_data['email'])
        password.send_keys(get_data['password'])
        password2.send_keys(get_data['password2'])

        assert driver.title == 'Sign Up'
        assert driver.current_url == 'http://localhost:8000/register/'
        # assert User.objects.count() == 1

    def test_register_user_already_exists(self):
        pass

    def test_register_email_already_exists(self):
        pass

    def test_register_passwords_dont_match(self):
        pass

    @pytest.mark.parametrize('test_password, test_password2', [('123456789', '123456789'), ('D5-_3', 'D5-_3'), ('test_user', 'test_user')])
    @pytest.mark.django_db
    def test_register_password_is_weak(self, get_data, get_webdriver, find_by, test_password, test_password2):
        driver = get_webdriver
        driver.get('http://localhost:8000/register/')
        selector = find_by('id')
        wait = WebDriverWait(driver, 5, 0.3)
        username = wait.until(
            ec.visibility_of_element_located((selector, 'id_username')))
        email = wait.until(ec.visibility_of_element_located(
            (selector, 'id_email')))
        password = wait.until(
            ec.visibility_of_element_located((selector, 'id_password')))
        password2 = wait.until(
            ec.visibility_of_element_located((selector, 'id_password2')))

        username.send_keys(get_data['username'])
        email.send_keys(get_data['email'])
        password.send_keys(test_password)
        password2.send_keys(test_password2)

        assert driver.current_url == 'http://localhost:8000/register/'
        assert User.objects.count() == 0


class TestLogin:
    def test_login_user(self):
        pass

    def test_login_user_doesnt_exist(self):
        pass


class TestLogout:
    def test_logout_user(self):
        pass

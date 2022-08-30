import pytest
from django.contrib.auth.models import User
from model_bakery import baker


class TestRegistration:

    @pytest.mark.django_db
    def test_register_user(self, get_webdriver, find_by, wait_for):
        user = baker.make(User)
        driver = get_webdriver
        driver.get('http://localhost:8000/register/')
        selector = find_by('id')
        # передавать как сет т.к. wait_for принимает селектор и элемент как один аргумент
        username = wait_for((selector, 'id_username'))
        email = wait_for((selector, 'id_email'))
        password = wait_for((selector, 'id_password'))
        password2 = wait_for((selector, 'id_password2'))

        username.send_keys(user.username)
        email.send_keys(user.email)
        password.send_keys(user.password)
        password2.send_keys(user.password)

        button_selector = find_by('tag')
        sign_up = wait_for((button_selector, 'button'))
        sign_up.click()

        assert driver.title == 'Sign Up'
        assert driver.current_url == 'http://localhost:8000/register/'
        assert User.objects.count() == 1

    @pytest.mark.django_db
    def test_register_user_already_exists(self, get_webdriver, find_by, wait_for):
        driver = get_webdriver
        driver.get('http://localhost:8000/register/')
        selector = find_by('id')
        username = wait_for((selector, 'id_username'))
        email = wait_for((selector, 'id_email'))
        password = wait_for((selector, 'id_password'))
        password2 = wait_for((selector, 'id_password2'))

        username.send_keys('test_user_1')
        email.send_keys('test@example.com')
        password.send_keys('test_123password')
        password2.send_keys('test_123password')

        button_selector = find_by('tag')
        sign_up = wait_for((button_selector, 'button'))
        sign_up.click()

        error_selector = find_by('xpath')
        error_message = wait_for(
            (error_selector, '/html/body/div[1]/div[2]/div/form/ul/li'))

        assert driver.current_url == 'http://localhost:8000/register/'
        assert User.objects.count() == 0
        assert error_message.text == 'User Already Exist'

    @pytest.mark.django_db
    def test_register_passwords_dont_match(self, get_webdriver, find_by, wait_for):
        driver = get_webdriver
        driver.get('http://localhost:8000/register/')
        selector = find_by('id')
        username = wait_for((selector, 'id_username'))
        email = wait_for((selector, 'id_email'))
        password = wait_for((selector, 'id_password'))
        password2 = wait_for((selector, 'id_password2'))

        username.send_keys('hello world')
        email.send_keys('email@example.com')
        password.send_keys('test_password')
        password2.send_keys('test_123password')

        button_selector = find_by('tag')
        sign_up = wait_for((button_selector, 'button'))
        sign_up.click()

        error_selector = find_by('xpath')
        error_message = wait_for(
            (error_selector, '/html/body/div[1]/div[2]/div/form/ul/li'))

        assert driver.current_url == 'http://localhost:8000/register/'
        assert User.objects.count() == 0
        assert error_message.text == "Passwords don't match"

    @pytest.mark.django_db
    def test_register_password_is_weak(self, get_webdriver, find_by, wait_for):
        driver = get_webdriver
        driver.get('http://localhost:8000/register/')
        selector = find_by('id')
        username = wait_for((selector, 'id_username'))
        email = wait_for((selector, 'id_email'))
        password = wait_for((selector, 'id_password'))
        password2 = wait_for((selector, 'id_password2'))

        username.send_keys('new_user')
        email.send_keys('test_example@gmail.com')
        password.send_keys('12345678')
        password2.send_keys('12345678')

        button_selector = find_by('tag')
        sign_up = wait_for((button_selector, 'button'))
        sign_up.click()

        error_selector = find_by('xpath')
        error_message = wait_for(
            (error_selector, '/html/body/div[1]/div[2]/div/form/ul/li[2]'))

        assert driver.current_url == 'http://localhost:8000/register/'
        assert User.objects.count() == 0
        assert error_message.text == 'This password is entirely numeric.'


class TestLogin:
    @pytest.mark.django_db
    def test_login_user(self, get_webdriver, find_by, wait_for):
        driver = get_webdriver
        driver.get('http://localhost:8000/login/')
        selector = find_by('id')
        username = wait_for((selector, 'username'))
        password = wait_for((selector, 'password'))

        username.send_keys('test_user_1')
        password.send_keys('rty123QWE')

        button_selector = find_by('tag')
        login = wait_for((button_selector, 'button'))
        login.click()

        assert driver.title == 'Home'
        assert driver.current_url == 'http://localhost:8000/'

    @ pytest.mark.django_db
    def test_login_user_doesnt_exist(self, get_webdriver, find_by, wait_for):
        driver = get_webdriver
        driver.get('http://localhost:8000/login/')
        selector = find_by('id')
        username = wait_for((selector, 'username'))
        password = wait_for((selector, 'password'))

        username.send_keys('jjjjjjjjjjjjjjjjjj')
        password.send_keys('dast4339_2dds')

        button_selector = find_by('tag')
        login = wait_for((button_selector, 'button'))
        login.click()

        error_selector = find_by('xpath')
        error_message = wait_for(
            (error_selector, '/html/body/div[1]/div[2]/div/div/h5'))

        assert driver.current_url == 'http://localhost:8000/login/'
        assert error_message.text == 'invalid username or password'


class TestLogout:
    def test_logout_user(self, get_webdriver, find_by, wait_for, login_user):
        driver = get_webdriver

        assert driver.current_url == 'http://localhost:8000/'

        profile_selector = find_by('xpath')
        driver.execute_script(
            "arguments[0].click();", driver.find_element((profile_selector, '/html/body/header/div/div[2]/img')))

        logout_selector = find_by('xpath')
        logout = wait_for(
            (logout_selector, '/html/body/header/div/div[2]/div/ul/li[2]/a'))
        logout.click()

        assert driver.title == 'Sign In'
        assert driver.current_url == 'http://localhost:8000/login/'

import pytest
import factory
import copy
from pytest_factoryboy import register
from tests.factories import UserFactory, ProfileFactory, PostFactory, CommentFactory
from django.urls import reverse
from django.contrib.auth import get_user


register(UserFactory)
register(ProfileFactory)
register(PostFactory)
register(CommentFactory)


@pytest.fixture(scope='session')
def valid_register_data():
    return {
        'username': 'test_username',
        'email': 'test@gmail.com',
        'password1': 'test_password1',
        'password2': 'test_password2',
    }


@pytest.fixture(scope='session')
def invalid_password_register_data(valid_register_data):
    data = copy.copy(valid_register_data)
    assert 'password1' in data
    data['password1'] = 'wrong'
    return data


@pytest.fixture
def is_logged_in(client):
    user = get_user(client)
    test1 = user.is_authenticated
    private_area_url = reverse('user:user_edit')
    response = client.get(private_area_url)
    test2 = response.status_code == 200
    test3 = response.wsgi_request.user.is_authenticated
    return test1 and test2 and test3


@pytest.fixture
def is_not_logged_in(client):
    user = get_user(client)
    test1 = not user.is_authenticated
    private_area_url = reverse('user:user_edit')
    response = client.get(private_area_url)
    test2 = response.status_code == 403
    test3 = not response.wsgi_request.user.is_authenticated
    return test1 and test2 and test3


@pytest.fixture(scope='session')
def valid_login_data(valid_register_data):
    username = valid_register_data['username']
    password = valid_register_data.get('password1')
    return {'username': username, 'password': password}


@pytest.fixture(scope='session')
def invalid_login_data(valid_login_data):
    data = copy.copy(valid_login_data)
    data['username'] = 'wrong_username'
    data['password'] = 'wrong_password'
    return data


@pytest.fixture
def created_user(django_user_model, valid_login_data):
    user = django_user_model.objects.create_user(
        email=valid_login_data['username'],
        password=valid_login_data['password'])
    user.set_password(valid_login_data['password'])
    return user


@pytest.fixture(scope='session')
def login_url():
    return reverse('login')


@pytest.fixture(scope='session')
def logout_url():
    return reverse('logout')


@pytest.fixture(scope='session')
def register_url():
    return reverse('register')

import pytest
from django.contrib.auth import get_user


def is_logged_in(client):
    user = get_user(client)
    test = user.is_authenticated
    return test


def is_not_logged_in(client):
    user = get_user(client)
    test = not user.is_authenticated
    return test


def test_authenticated_user_is_logged_in(client, authenticated_user):
    assert is_logged_in(client)


def test_created_user_is_not_logged_in(client, created_user):
    assert is_not_logged_in(client)


@pytest.mark.django_db
def test_login_user(client, django_user_model, valid_login_data, login_url, created_user):
    assert django_user_model.objects.count() == 1
    response = client.post(login_url, valid_login_data)
    assert response.status_code in (200, 302)
    assert is_logged_in(client)


@pytest.mark.django_db
def test_login_with_wrong_data(
        client, invalid_login_data, created_user, login_url):
    assert invalid_login_data['username'] == 'wrong_username'
    assert invalid_login_data['password'] == 'wrong_password'
    client.post(login_url, data=invalid_login_data)
    assert is_not_logged_in(client)


@pytest.mark.django_db
def test_logout_user(client, logout_url):
    response = client.get(logout_url)
    assert response.status_code == 302
    assert is_not_logged_in(client)


@pytest.mark.django_db
def test_register_with_valid_data(
        client, valid_register_data, django_user_model, register_url):
    assert django_user_model.objects.count() == 0
    response = client.post(register_url, valid_register_data)
    assert response.status_code in (200, 302)
    assert django_user_model.objects.count() == 1
    assert is_logged_in(client)


@pytest.mark.django_db
def test_register_when_passwords_dont_match(
        client, invalid_password_register_data, django_user_model, register_url):
    assert (
        invalid_password_register_data['password1'] == 'wrong' or
        invalid_password_register_data['password2'] == 'wrong')
    response = client.post(register_url, invalid_password_register_data)
    assert response.status_code == 200
    assert django_user_model.objects.count() == 0
    assert is_not_logged_in(client)


# def test_register_when_password_not_strong():
#     pass

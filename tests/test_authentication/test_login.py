import pytest


class PytestError(Exception):
    pass


def test_login_user(client, django_user_model, valid_login_data, is_logged_in, login_url, create_user):
    assert django_user_model.objects.count() == 1
    response = client.post(login_url, valid_login_data)
    assert response.status_code in (200, 302)
    assert is_logged_in(client)


def test_login_with_wrong_data(
        client, invalid_login_data, created_user, login_url, is_not_logged_in):
    assert invalid_login_data['username'] == 'wrong_username'
    assert invalid_login_data['password'] == 'wrong_password'
    with pytest.raises(PytestError):
        client.post(login_url, data=invalid_login_data)
    assert is_not_logged_in(client)

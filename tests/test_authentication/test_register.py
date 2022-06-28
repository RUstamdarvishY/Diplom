import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register_with_valid_data(
        client, valid_register_data, django_user_model, is_logged_in, register_url):
    assert django_user_model.objects.count() == 0
    response = client.post(register_url, valid_register_data)
    assert response.status_code in (200, 302,)
    assert django_user_model.objects.count() == 1
    assert is_logged_in(client)


@pytest.mark.django_db
def test_register_when_passwords_dont_match(
        client, invalid_password_register_data, django_user_model, is_not_logged_in, register_url):
    assert (
        invalid_password_register_data['password1'] == 'wrong' or
        invalid_password_register_data['password2'] == 'wrong')
    response = client.post(register_url, invalid_password_register_data)
    assert response.status_code == 200
    assert django_user_model.objects.count() == 0
    assert is_not_logged_in(client)


# def test_register_when_password_not_strong():
#     pass

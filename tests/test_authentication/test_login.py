import pytest
from django.urls import reverse


def test_login_user(login_user, client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert login_user.is_authenticated == True

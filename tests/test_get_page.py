import pytest
from django.urls import reverse


def test_login_page(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


def test_logout_page(client):
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302


def test_register_page(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200


def test_main_page(client):
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 302


def test_profile_page(client):
    url = reverse('another_profile')
    response = client.get(url)
    assert response.status_code == 302


def test_create_profile_page(client):
    url = reverse('create_profile')
    response = client.get(url)
    assert response.status_code == 200


def test_delete_profile_page(client):
    url = reverse('delete_profile')
    response = client.get(url)
    assert response.status_code == 302


def test_update_profile_page(client):
    url = reverse('update_profile')
    response = client.get(url)
    assert response.status_code == 302


def test_create_post_page(client):
    url = reverse('create_post')
    response = client.get(url)
    assert response.status_code == 302


def test_comment_page(client):
    url = reverse('comment')
    response = client.get(url)
    assert response.status_code == 200

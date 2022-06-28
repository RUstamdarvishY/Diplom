import pytest


@pytest.mark.django_db
def test_logout_user(client, is_not_logged_in, logout_url):
    response = client.get(logout_url)
    assert response.status_code == 302
    assert is_not_logged_in(client)
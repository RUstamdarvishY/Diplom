import pytest
from django.contrib.auth import logout


@pytest.mark.django_db
def test_logout_user(client, login_user, request):
    if login_user.is_authenticated:
        logout(request)
    assert login_user.is_authenticated == False

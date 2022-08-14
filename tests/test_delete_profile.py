import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_delete_profile(user_factory):
    assert User.objects.count() == 0
    user = user_factory.create()
    assert User.objects.count() == 1
    User.objects.get(username=user.username).delete()
    assert User.objects.count() == 0

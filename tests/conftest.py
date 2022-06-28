import pytest
import factory
from pytest_factoryboy import register
from tests.factories import UserFactory, ProfileFactory, PostFactory, CommentFactory
from django.urls import reverse
from django.contrib.auth.models import User


register(UserFactory)
register(ProfileFactory)
register(PostFactory)
register(CommentFactory)


@pytest.fixture
def login_user(client, db):
    user = User.objects.create(
        username='test_username', password='test_password')
    client.force_login(user)
    return user



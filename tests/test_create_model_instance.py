from calendar import c
import pytest
from mainapp.models import Profile, Post, Comment
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_create_user(user_factory):
    assert User.objects.count() == 0
    user = user_factory.create()
    assert User.objects.count() == 1
    assert user.username == 'test_username'
    assert user.password == 'test_password'


@pytest.mark.django_db
def test_create_profile(profile_factory):
    assert Profile.objects.count() == 0
    profile = profile_factory.create()
    assert Profile.objects.count() == 1
    assert profile.firstname == 'test_firstname'
    assert profile.lastname == 'test_lastname'


@pytest.mark.django_db
def test_create_post(post_factory):
    assert Post.objects.count() == 0
    post = post_factory.create()
    assert Post.objects.count() == 1
    assert post.title == 'test_title'
    assert post.text == 'test_text'


@pytest.mark.django_db
def test_create_comment(comment_factory):
    assert Comment.objects.count() == 0
    comment = comment_factory.create()
    assert Comment.objects.count() == 1
    assert comment.text == 'test_comment_text'

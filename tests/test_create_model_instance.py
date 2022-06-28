import pytest


@pytest.mark.django_db
def test_create_user(user_factory):
    user = user_factory.create()
    assert user.username == 'test_username'
    assert user.password == 'test_password'


@pytest.mark.django_db
def test_create_profile(profile_factory):
    profile = profile_factory.create()
    assert profile.firstname == 'test_firstname'
    assert profile.lastname == 'test_lastname'
    

@pytest.mark.django_db
def test_create_post(post_factory):
    post = post_factory.create()
    assert post.title == 'test_title'
    assert post.text == 'test_text'
    
    
@pytest.mark.django_db
def test_create_comment(comment_factory):
    comment = comment_factory.create()
    assert comment.text == 'test_comment_text'
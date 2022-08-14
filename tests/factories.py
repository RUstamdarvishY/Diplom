import factory
from django.contrib.auth.models import User
from mainapp.models import Post, Profile, Comment


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'test_username'
    password = 'test_password'


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    firstname = 'test_firstname'
    lastname = 'test_lastname'
    user = factory.SubFactory(UserFactory)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = 'test_title'
    text = 'test_text'
    author = factory.SubFactory(UserFactory)


class NewUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = 'test_comment_text'
    author = factory.SubFactory(NewUserFactory)
    post = factory.SubFactory(PostFactory)

from django.db import models
from django.contrib.auth import get_user_model


user = get_user_model()


class Profile(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    profile_picture = models.ImageField(default=None, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    text = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    number_of_likes = models.IntegerField(default=0, null=True, blank=True)
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    comments = models.ForeignKey(
        Comment, on_delete=models.DO_NOTHING, default=None)

    def __str__(self):
        return f'{self.title}, {self.created_at}'

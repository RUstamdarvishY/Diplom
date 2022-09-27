from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from mainapp.validators import validate_file_size


user = get_user_model()
allowed_extention = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg'])


class Profile(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='images/',
                                        validators=[
                                            validate_file_size, allowed_extention],
                                        null=True, blank=True)
    location = models.CharField(
        max_length=255, default='', null=True, blank=True)
    bio = models.CharField(max_length=255, default='', null=True, blank=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to='images/',
                              validators=[validate_file_size,
                                          allowed_extention],
                              null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    number_of_likes = models.IntegerField(default=0, null=True, blank=True)
    author = models.ForeignKey(
        user, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments', null=True, blank=True)
    text = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.username

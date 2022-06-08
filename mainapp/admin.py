from django.contrib import admin
from mainapp.models import Profile, Post, Comment, LikePost


admin.site.register(Profile)

admin.site.register(Post)

admin.site.register(Comment)

admin.site.register(LikePost)

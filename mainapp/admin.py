from django.contrib import admin
from mainapp.models import Profile, Post, Comment, LikePost


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'user',
                    'location']
    list_editable = ['firstname', 'lastname', 'location']
    list_display_links = ['user']
    list_per_page = 5
    ordering = ['firstname', 'lastname', 'user']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'number_of_likes']
    list_editable = ['title']
    list_display_links = ['author']
    list_per_page = 5
    ordering = ['created_at', 'title', 'number_of_likes']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'commented_at', 'text']
    list_editable = ['text']
    list_display_links = ['author']
    list_per_page = 5
    ordering = ['commented_at']


admin.site.register(LikePost)

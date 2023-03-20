from django.urls import path
from mainapp.views import RegisterView, MainView, profile, CreateProfileView, user_login, user_logout, update_profile, delete_profile, CreatePostView, like_post, CommentView, update_post, delete_post


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='another_profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('', MainView.as_view(), name='main'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('update_post/', update_post, name='update_post'),
    path('delete_post', delete_post, name='delete_post'),
    path('like_post/', like_post, name='like_post'),
    path('comment/', CommentView.as_view(), name='comment'),
]

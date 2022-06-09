from django.urls import path
from mainapp.views import RegisterView, MainView, another_profile, ProfileView, CreateProfileView, user_login, user_logout, UpdateProfileView, delete_profile, CreatePostView, like_post


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/<int:pk>', another_profile, name='_another_profile'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('main/', MainView.as_view(), name='main'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('like_post/', like_post, name='like_post')
]

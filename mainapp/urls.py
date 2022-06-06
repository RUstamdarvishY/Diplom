from django.urls import path
from mainapp.views import RegisterView, MainView, ProfileView, CreateProfileView, user_login, user_logout, UpdateProfileView, delete_profile, CreatePostView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('main/', MainView.as_view(), name='main'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
]

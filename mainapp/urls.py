from django.urls import path
from mainapp.views import RegistrationView, PostView, ProfileView, CreateProfileView, login, logout, UpdateProfileView, DeleteProfileView, CreatePostView, UpdatePostView, DeletePostView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update_profile/', UpdateProfileView.as_view(), name='update'),
    path('delete_profile/', DeleteProfileView.as_view(), name='delete'),
    path('post/', PostView.as_view(), name='post'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('update_post/', UpdatePostView.as_view(), name='update_post'),
    path('delete_post/', DeletePostView.as_view(), name='delete_post')
]

from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import info, error, success
from mainapp.forms import ProfileForm
from django.views import View


class RegistrationView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return render(request, 'registration.html')
        else:
            return redirect('post')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            user = User.objects.create(
                username=username,
                email=email,
                password=password
            )
            user.save()
            return redirect('create_profile')
        else:
            error(request, 'passwords do not match')
            return render(request, 'registration.html')


class CreateProfileView(FormView):
    template_name = 'create_profile.html'
    form_class = ProfileForm
    success_url = '/post/'


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post')
        else:
            error(request, 'invalid username or password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


@login_required(login_url='/login/')
def logout(request):
    logout(request)
    return redirect('login')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    login_url = '/login/'


class UpdateProfileView(LoginRequiredMixin, TemplateView):
    pass


class DeleteProfileView(LoginRequiredMixin, TemplateView):
    pass


class PostView(LoginRequiredMixin, TemplateView):
    template_name = 'post.html'
    login_url = '/login/'


class CreatePostView(LoginRequiredMixin, TemplateView):
    pass


class UpdatePostView(LoginRequiredMixin, TemplateView):
    pass


class DeletePostView(LoginRequiredMixin, TemplateView):
    pass

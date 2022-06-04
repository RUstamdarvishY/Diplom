from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import error, success
from django.views import View
from mainapp.forms import ProfileForm
from mainapp.models import Profile


class RegisterView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return render(request, 'register.html')
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
            login(request, user)
            return redirect('create_profile')
        else:
            error(request, 'passwords do not match')
            return render(request, 'register.html')


class CreateProfileView(TemplateView, FormMixin):
    template_name = 'create_profile.html'
    form_class = ProfileForm

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            profile = Profile.objects.create(**data, user=request.user)
            profile.save()
        return redirect('main')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            error(request, 'invalid username or password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('login')


class ProfileView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'
    login_url = '/login/'


class UpdateProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'update_profile.html'
    login_url = '/login/'

    def post(self, request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        profile_picture = request.POST.get('profile_picture')
        bio = request.POST.get('bio')
        location = request.POST.get('location')

        profile = Profile.objects.update(
            firstname=firstname,
            lastname=lastname,
            profile_picture=profile_picture,
            bio=bio,
            location=location
        )
        profile.save()
        user = User.objects.update(
            email=email,
        )
        user.save()


class DeleteProfileView(LoginRequiredMixin, TemplateView):
    pass


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'main.html'
    login_url = '/login/'


class CreatePostView(LoginRequiredMixin, TemplateView):
    pass

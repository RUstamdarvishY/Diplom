from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from mainapp.forms import ProfileForm, UserForm, PostForm
from mainapp.models import Profile, Post

# TODO: fix reloading on register


def register(request):
    if request.POST == 'POST':
        form = UserForm()
        if form.is_valid():
            form.save()
            return redirect('create_profile')
        else:
            messages.error(request, 'something went wrong')
            return redirect('register')
    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


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
            messages.error(request, 'invalid username or password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    return redirect('login')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(user=self.request.user)
        context["number_of_posts"] = Post.objects.filter(
            author=self.request.user).count()
        return context


class UpdateProfileView(LoginRequiredMixin, TemplateView, FormMixin):
    template_name = 'update_profile.html'
    form_class = ProfileForm
    login_url = '/login/'

    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            profile = Profile.objects.get(user=request.user)
            profile.firstname = data['firstname']
            profile.lastname = data['lastname']
            profile.profile_picture = data['profile_picture']
            profile.location = data['location']
            profile.bio = data['bio']
            profile.save()
        return redirect('main')


@login_required(login_url='/login/')
def delete_profile(request):
    user = User.objects.get(username=request.user.username)
    user.delete()
    return redirect('register')


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'main.html'
    login_url = '/login/'


class CreatePostView(LoginRequiredMixin, TemplateView, FormMixin):
    template_name = 'create_post.html'
    login_url = '/login/'
    form_class = PostForm

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post = Post.objects.create(**data, author=request.user)
            post.save()
        return redirect('main')

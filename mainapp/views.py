from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin, CreateView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from mainapp.forms import ProfileForm, UpdateProfileForm, UserForm, PostForm, CommentForm
from mainapp.models import Profile, Post, Comment, LikePost
from mainapp.tasks import send_email


login_url = '/login/'


class RegisterView(TemplateView, FormMixin):
    template_name = 'register.html'
    form_class = UserForm

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form.save()
            user = User.objects.get(username=data.get('username'))
            login(request, user)
            send_email.delay(data.get('email'), data.get('username'))
            return redirect('create_profile')
        else:
            context = {'form': form}
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


@login_required(login_url=login_url)
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url=login_url)
def profile(request):
    pk = request.GET.get('user_pk')
    user = User.objects.get(pk=pk)
    user_profile = Profile.objects.filter(user=user).first()
    post_number = Post.objects.filter(author=pk).count()

    context = {
        'user': user,
        'user_profile': user_profile,
        'post_number': post_number
    }

    if user == request.user:
        context["profile"] = Profile.objects.get(user=request.user)
        context["number_of_posts"] = Post.objects.filter(
            author=request.user).count()
        return render(request, 'profile.html', context)
    else:
        return render(request, 'another_profile.html', context)


class UpdateProfileView(LoginRequiredMixin, TemplateView, FormMixin):
    form_class = UpdateProfileForm
    template_name = 'update_profile.html'
    login_url = login_url

    def post(self, request):
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            profile = Profile.objects.get(user=request.user)
            profile.profile_picture = data['profile_picture']
            profile.location = data['location']
            profile.bio = data['bio']
            profile.save()
        return redirect('main')


@login_required(login_url=login_url)
def delete_profile(request):
    user = User.objects.get(username=request.user.username)
    logout(request)
    user.delete()
    return redirect('register')


class MainView(LoginRequiredMixin, ListView):
    template_name = 'main.html'
    login_url = login_url
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_image'] = Profile.objects.get(user=self.request.user)
        return context


class CreatePostView(LoginRequiredMixin, TemplateView, FormMixin):
    template_name = 'create_post.html'
    login_url = login_url
    form_class = PostForm

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        return redirect('main')


@login_required(login_url=login_url)
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(
        post_id=post_id, username=username).first()

    if like_filter is None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.number_of_likes += 1
        post.save()
        return redirect('main')
    else:
        like_filter.delete()
        post.number_of_likes -= 1
        post.save()
        return redirect('main')


class CommentView(CreateView, LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'comments.html'
    login_url = login_url
    success_url = '/main/'

    def post(self, *args):
        pk = self.request.GET.get('post_id')
        post = Post.objects.get(pk=pk)
        author = self.request.user
        text = self.request.POST.get('text')
        comment = Comment.objects.create(
            post=post,
            author=author,
            text=text
        )
        comment.save()
        return redirect('main')

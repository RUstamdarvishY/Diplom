import logging
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin, CreateView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from mainapp.forms import ProfileForm, UpdateProfileForm, UserForm, PostForm, CommentForm, UpdatePostForm
from mainapp.models import Profile, Post, Comment, LikePost
from mainapp.tasks import send_email


login_url = '/login/'
logger = logging.getLogger(__name__)


class RegisterView(TemplateView, FormMixin):
    template_name = 'register.html'
    form_class = UserForm

    def post(self, request):
        logger.info('calling /register')
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form.save()
            logger.info('user registration successful')
            try:
                user = User.objects.get(username=data.get('username'))
            except User.DoesNotExist:
                logger.error('User does not exist')
            login(request, user)
            send_email.delay(data.get('email'), data.get('username'))
            return redirect('create_profile')
        else:
            context = {'form': form}
            logger.info('form is invalid')
            return render(request, 'register.html', context)


class CreateProfileView(TemplateView, FormMixin):
    template_name = 'create_profile.html'
    form_class = ProfileForm

    def post(self, request):
        logger.info('calling /create_profile')
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            profile = Profile.objects.create(**data, user=request.user)
            profile.save()
            logger.info('profile created successfully')
        return redirect('/')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info('login successful')
            return redirect('/')
        else:
            messages.error(request, 'invalid username or password')
            logger.info('invalid username or password')
            return render(request, 'login.html')
    else:
        logger.info('calling /login')
        return render(request, 'login.html')


@login_required(login_url=login_url)
def user_logout(request):
    logout(request)
    logger.info('logout successful')
    return redirect('login')


@login_required(login_url=login_url)
def profile(request):
    logger.info('calling /profile')
    try:
        pk = request.GET.get('user_pk')
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        logger.error('user does not exist')
    user_profile = Profile.objects.filter(user=user).first()
    post_number = Post.objects.filter(author=pk).count()
    posts = Post.objects.filter(author=pk).order_by('-created_at')

    context = {
        'user': user,
        'user_profile': user_profile,
        'post_number': post_number,
        'posts': posts
    }

    if user == request.user:
        context["profile"] = Profile.objects.get(user=request.user)
        context["number_of_posts"] = Post.objects.filter(
            author=request.user).count()
        context["posts"] = Post.objects.filter(
            author=pk).order_by('-created_at')
        logger.info('get my profile')
        return render(request, 'profile.html', context)
    else:
        logger.info(f'get {user.username} profile')
        return render(request, 'another_profile.html', context)


@login_required(login_url=login_url)
def update_profile(request):
    profile = Profile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        logger.info('calling /update_profile')
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            profile.firstname = data['firstname']
            profile.lastname = data['lastname']
            profile.profile_picture = data['profile_picture']
            profile.location = data['location']
            profile.bio = data['bio']
            profile.save()
            logger.info('Profile updated successfully')
        return redirect('/')

    else:
        form = UpdateProfileForm(instance=profile)

        context = {
            'form': form,
            'profile': profile
        }
        return render(request, "update_profile.html", context)


@login_required(login_url=login_url)
def delete_profile(request):
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        logger.error('user does not exist')
    logout(request)
    user.delete()
    logger.info('Profile deleted successfully')
    return redirect('register')


class MainView(LoginRequiredMixin, ListView):
    template_name = 'main.html'
    login_url = login_url
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        logger.info('calling /main')
        context = super().get_context_data(**kwargs)
        context['user_image'] = Profile.objects.get(user=self.request.user)
        # context['author-image'] =
        return context


class CreatePostView(LoginRequiredMixin, TemplateView, FormMixin):
    template_name = 'create_post.html'
    login_url = login_url
    form_class = PostForm

    def post(self, request):
        logger.info('calling /create_post')
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            try:
                post.author = request.user
            except User.DoesNotExist:
                logger.error('user does not exist')
            post.save()
        return redirect('/')


@login_required(login_url=login_url)
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        logger.error('post does not exist')
    like_filter = LikePost.objects.filter(
        post_id=post_id, username=username).first()

    if like_filter is None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.number_of_likes += 1
        post.save()
        logger.info('+1 like')
        return redirect('/')
    else:
        like_filter.delete()
        post.number_of_likes -= 1
        post.save()
        logger.info('-1 like')
        return redirect('/')


@login_required(login_url=login_url)
def delete_post(request):
    user_pk = request.user.pk
    post_id = request.GET.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
    except ObjectDoesNotExist:
        logger.error('Post does not exist')
    post.delete()
    logger.info('Post deleted successfully')
    return redirect(f'profile/?user_pk={user_pk}')


@login_required(login_url=login_url)
def update_post(request):
    post = Post.objects.filter(author=request.user.pk).first()

    if request.method == 'POST':
        form = UpdatePostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post.title = data['title']
            post.text = data['text']
            post.image = data['image']
            post.save()
        return redirect(f'/profile/?user_pk={request.user.pk}')

    else:
        form = UpdatePostForm(instance=post)

        context = {
            'form': form,
            'post': post
        }
        return render(request, "update_post.html", context)


class CommentView(CreateView, LoginRequiredMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'comments.html'
    login_url = login_url
    success_url = '/'

    def post(self, *args):
        logger.info('calling /comment')
        try:
            pk = self.request.GET.get('post_id')
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist:
            logger.error('post does not exist')
        try:
            author = self.request.user
        except User.DoesNotExist:
            logger.error('author does not exist')
        text = self.request.POST.get('text')
        comment = Comment.objects.create(
            post=post,
            author=author,
            text=text
        )
        comment.save()
        logger.info('Comment created successfully')
        return redirect('/')

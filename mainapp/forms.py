import logging
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from mainapp.models import Profile, Post, Comment

logger = logging.getLogger(__name__)


class UserForm(forms.Form):
    username = forms.CharField(label='Username', min_length=1, max_length=255,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput
                             (attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput
                               (attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
        (attrs={'placeholder': 'Confirm Password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        new = User.objects.filter(username=username)
        if new.exists():
            logger.info("User already exists")
            raise ValidationError("User Already Exist")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        new = User.objects.filter(email=email)
        if new.exists():
            logger.info("Email already exists")
            raise ValidationError("Email Already Exist")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def clean_password2(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password:
            if password != password2:
                logger.info("Passwords do not match")
                raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password']
        )
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('firstname', 'lastname',
                  'profile_picture', 'location', 'bio')


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture', 'location', 'bio')


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'image')


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'image')

    def save(self, commit=True):
        post = Post()
        post.title = self.cleaned_data['title']
        post.text = self.cleaned_data['text']
        post.image = self.cleaned_data['image']
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

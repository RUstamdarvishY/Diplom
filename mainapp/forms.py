from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from mainapp.models import Profile, Post, Comment


class UserForm(forms.Form):
    username = forms.CharField(label='Username', min_length=1, max_length=255)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        new = User.objects.filter(username=username)
        if new.exists():
            raise ValidationError("User Already Exist")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        new = User.objects.filter(email=email)
        if new.exists():
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

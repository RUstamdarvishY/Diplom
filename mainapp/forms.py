from django.forms import ModelForm
from mainapp.models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('firstname', 'lastname',
                  'profile_picture', 'location', 'bio')

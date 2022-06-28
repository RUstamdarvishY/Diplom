import pytest
from mainapp.models import Profile


@pytest.mark.django_db
def test_update_profile(profile_factory):
    assert Profile.objects.count() == 0
    profile = profile_factory.create()
    assert Profile.objects.count() == 1
    assert profile.firstname == 'test_firstname'
    profile.firstname = 'new_firstname'
    profile.save()
    assert profile.firstname == 'new_firstname'

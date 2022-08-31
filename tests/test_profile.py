import pytest
from django.contrib.auth.models import User
from model_bakery import baker


class TestGetProfile:
    @pytest.mark.django_db
    def test_get_my_profile(self, get_webdriver, find_by, wait_for, login_user):
        driver = get_webdriver
        driver.get('http://localhost:8000/profile/?user_pk=8')

        selector = find_by('xpath')
        get_extra_options = wait_for((selector, '/html/body/div[6]/a/b'))

        assert driver.title == 'Profile test_user_1'
        assert get_extra_options is not None

    @pytest.mark.django_db
    @pytest.mark.skip
    def test_get_another_profile(self, get_webdriver, find_by, wait_for, login_user):
        driver = get_webdriver
        driver.get(f'http://localhost:8000/profile/?user_pk=2')

        # selector = find_by('xpath')
        # username_link = wait_for(
        #     (selector, '/html/body/div/div/div[1]/div[1]/div[1]/a'))
        # username_link.click()

        options_selector = find_by('xpath')
        get_extra_options = wait_for(
            (options_selector, '/html/body/div[6]/a/b'))

        assert driver.title == 'Profile Test User 2'
        assert get_extra_options is None


class TestCreateProfile:
    @ pytest.mark.django_db
    def test_create_profile(self):
        pass


class TestUpdateProfile:
    @ pytest.mark.django_db
    def test_update_profile(self):
        pass


class TestDeleteProfile:
    @ pytest.mark.django_db
    def test_delete_profile(self):
        pass

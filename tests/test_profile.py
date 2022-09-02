import pytest


class TestGetProfile:
    @pytest.mark.django_db
    def test_get_my_profile(self, get_webdriver, find_by, wait_for, login_user):
        driver = get_webdriver
        driver.get('http://localhost:8000/profile/?user_pk=8')

        selector = find_by('xpath')
        get_extra_options = wait_for((selector, '/html/body/div[6]/a/b'))

        assert driver.title == 'Profile test_user_1'
        assert get_extra_options is not None

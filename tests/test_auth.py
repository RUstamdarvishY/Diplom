import pytest


class TestRegistration:
    @pytest.mark.django_db
    def test_register_user(self):
        pass

    def test_register_user_already_exists(self):
        pass

    def test_register_email_already_exists(self):
        pass

    def test_register_passwords_dont_match(self):
        pass

    @pytest.mark.parametrize
    def test_register_passwords_is_weak(self):
        pass


class TestLogin:
    def test_login_user(self):
        pass

    def test_login_user_doesnt_exist(self):
        pass


class TestLogout:
    def test_logout_user(self):
        pass

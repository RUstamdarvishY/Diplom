import pytest


@pytest.fixture
def get_data():
    data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'QWErty123',
        'password2': 'QWErty123'
    }
    return data


class TestRegistration:

    def test_register_user(self, get_url, find_by, wait_for, actions, get_data):
        get_url('register/')
        find_by('class')
        username = wait_for('')
        email = wait_for('')
        password = wait_for('')
        password2 = wait_for('')

        actions.send_keys_to_element(username, get_data['username'])
        actions.send_keys_to_element(email, get_data['email'])
        actions.send_keys_to_element(password, get_data['password'])
        actions.send_keys_to_element(password2, get_data['password2'])
        actions.perform()

        assert response.status_code == 200
        assert url = ''
        assert User.objects.get() == get_data

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

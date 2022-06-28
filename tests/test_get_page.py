import pytest


def test_login_page(login_page):
    assert login_page.status_code == 200


def test_logout_page(logout_page):
    assert logout_page.status_code == 302


def test_register_page(register_page):
    assert register_page.status_code == 200


def test_main_page(main_page):
    assert main_page.status_code == 302


def test_profile_page(profile_page):
    assert profile_page.status_code == 302


def test_create_profile_page(create_profile_page):
    assert create_profile_page.status_code == 200


def test_delete_profile_page(delete_profile_page):
    assert delete_profile_page.status_code == 302


def test_update_profile_page(update_profile_page):
    assert update_profile_page.status_code == 302


def test_create_post_page(create_post_page):
    assert create_post_page.status_code == 302


def test_comment_page(comment_page):
    assert comment_page.status_code == 200

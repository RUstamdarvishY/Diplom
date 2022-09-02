import pytest
from model_bakery import baker
from mainapp.models import Post


class TestGetPost:
    @pytest.mark.django_db
    def test_get_all_posts(self, get_webdriver, login_user):
        driver = get_webdriver
        driver.get('http://localhost:8000/')

        assert driver.current_url == 'http://localhost:8000/'
        assert driver.title == 'Home'


class TestCreatePost:
    @pytest.mark.django_db
    def test_create_post(self, get_webdriver, find_by, wait_for, login_user):
        post = baker.make(Post)
        driver = get_webdriver
        driver.get('http://localhost:8000/create_post/')
        selector = find_by('id')
        # передавать как сет т.к. wait_for принимает селектор и элемент как один аргумент
        title = wait_for((selector, 'id_title'))
        text = wait_for((selector, 'id_text'))

        title.send_keys(post.title)
        text.send_keys(post.text)

        button_selector = find_by('tag')
        create_post = wait_for((button_selector, 'button'))
        create_post.click()

        post_selector = find_by('xpath')
        post_title = wait_for(
            (post_selector, '/html/body/div/div/div[1]/div[2]/h2/strong'))

        assert driver.current_url == 'http://localhost:8000/'
        assert Post.objects.count() == 1
        assert post_title.text == post.title


# Error: ElementClickIntercepted (не нажимается кнопка save на странице обновления поста - пофиксить тест)
class TestUpdatePost:
    @pytest.mark.django_db
    @pytest.mark.skip
    def test_update_post(self, get_webdriver, find_by, wait_for, login_user):
        driver = get_webdriver
        driver.get(f'http://localhost:8000/profile/?user_pk=8')

        button_selector = find_by('xpath')
        update_post = wait_for(
            (button_selector, '/html/body/div[7]/div/div[1]/div/a[1]/b'))
        update_post.click()

        selector = find_by('id')
        title = wait_for((selector, 'id_title'))
        text = wait_for((selector, 'id_text'))

        title.send_keys('new_title')
        text.send_keys('new_text')

        save_selector = find_by('xpath')
        driver.execute_script(
            "arguments[0].click();", driver.find_element
            (save_selector, '/html/body/div[1]/div/div[2]/form/div/button'))

        post_selector = find_by('xpath')
        new_post_title = wait_for(
            (post_selector, '/html/body/div[7]/div/div[1]/h2/strong'))

        assert driver.current_url == 'http://localhost:8000/profile/?user_pk=8'
        assert Post.objects.count() == 1
        assert new_post_title.text == 'new_title'


class TestDeletePost:
    @ pytest.mark.django_db
    def test_delete_post(self, get_webdriver, find_by, wait_for, login_user):
        driver = get_webdriver
        driver.get(f'http://localhost:8000/profile/?user_pk=8')

        delete_selector = find_by('xpath')
        delete = wait_for(
            (delete_selector, '/html/body/div[7]/div/div[1]/div/a[2]/b'))
        delete.click()

        assert driver.current_url == 'http://localhost:8000/profile/?user_pk=8'
        # в этом тесте мы удаляем пост, который был создан create_post тестом
        assert Post.objects.count() == 0


# Error: StaleElementReferenceException (не нажимается иконка svg - пофиксить)
class TestLikePost:
    @pytest.mark.django_db
    @pytest.mark.skip
    def test_like_post(self, get_webdriver, find_by, wait_for, login_user):
        driver = get_webdriver
        post = baker.make(Post)
        driver.get('http://localhost:8000/create_post/')
        selector = find_by('id')

        title = wait_for((selector, 'id_title'))
        text = wait_for((selector, 'id_text'))

        title.send_keys(post.title)
        text.send_keys(post.text)

        button_selector = find_by('tag')
        create_post = wait_for((button_selector, 'button'))
        create_post.click()

        like_selector = find_by('xpath')

        get_initial_like_number = wait_for(
            (like_selector,
             '/html/body/div/div/div[1]/div[3]/div[2]/div[2]/strong[1]'))

        like = wait_for(
            (like_selector, '/html/body/div/div/div[1]/div[3]/div[1]/a[1]/div'))
        like.click()

        get_new_like_number = wait_for(
            (like_selector,
             '/html/body/div/div/div[1]/div[3]/div[2]/div[2]/strong[1]'))

        assert driver.current_url == 'http://localhost:8000/'
        assert get_initial_like_number.text == get_new_like_number.text - 1

        like.click()
        get_final_like_number = wait_for((like_selector,
                                          '/html/body/div/div/div[1]/div[3]/div[2]/div[2]/strong[1]'))

        assert driver.current_url == 'http://localhost:8000/'
        assert get_new_like_number.text == get_final_like_number.text + 1


# Error: TimeoutException (скорее всего проблема с svg иконкой - пофиксить)
class TestCommentOnPost:
    @pytest.mark.django_db
    @pytest.mark.skip
    def test_comment_on_post(self, get_webdriver, find_by, wait_for, login_user):
        driver = get_webdriver
        driver.get('http://localhost:8000/')

        comment_selector = find_by('xpath')
        comment_icon = wait_for(
            (comment_selector, '/html/body/div/div/div[1]/div[3]/div[1]/a[2]/div/svg/path'))
        comment_icon.click()

        comment_send = find_by('id')
        comment_text = wait_for((comment_send, 'id_text'))
        comment_text.send_keys('test_comment')

        save_selector = find_by('tag')
        save = wait_for((save_selector, 'button'))
        save.click()

        comment_text = wait_for(
            (comment_text, '/html/body/div/div/div[1]/div[3]/div[2]/div[2]/h2'))

        assert driver.current_url == 'http://localhost:8000/'
        assert comment_text.text == 'test_comment'

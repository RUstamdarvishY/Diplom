from locust import HttpUser, between, task
from random import randint


# TODO: change GET to POST instead (except view_profile)
class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(8)
    def like_post(self):
        post_id = randint(1, 10)
        self.client.get(
            f'/like_post?post_id={post_id}', name='/like_post')

    @task(6)
    def comment(self):
        post_id = randint(1, 10)
        self.client.get(
            f'/comment?post_id={post_id}', name='/comment')

    @task(4)
    def view_profile(self):
        user_id = randint(1, 5)
        self.client.get(f'/profile?user_pk={user_id}', name='/profile')

    @task(2)
    def create_post(self):
        self.client.get(
            f'/create_post', name='/create_post')

    def on_start(self):
        pass

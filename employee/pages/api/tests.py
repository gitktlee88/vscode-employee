# python manage.py test   to run this testcase

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from rest_framework.reverse import reverse as api_reverse

# creating new token manually
from rest_framework_jwt.settings import api_settings
payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

from django.contrib.auth import get_user_model
from pages.models import BlogPost

# https://wsvincent.com/django-referencing-the-user-model/
User = get_user_model()  

from .serializers import UserSerializer


class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        #user_obj = User.object.create(username='testmyuser', email='test@test.com')
        user_obj = User(username='testmyuser', email='test@test.com')
        user_obj.set_password("somepassword")
        user_obj.save()
        blog_posts = BlogPost.objects.create(
            user=user_obj,
            title='New title',
            content='some_random_content'
            )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)


    def test_single_post(self):
        post_count = BlogPost.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        # test GET list
        data = {}
        url = api_reverse("api-pages:pages-listcreate")
        #print(url)
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)
        #print(response.content)

    def test_post_item(self):
        # test POST list
        data = {"title": "Some random title", "content": "some more content"}
        url = api_reverse("api-pages:pages-listcreate")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #print(response.data)

    def test_get_item(self):
        # test GET list
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)

    def test_update_item(self):
        # test POST update
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {"title": "Some random title", "content": "some more content"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        #print(response.data)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #print(response.data)

    def test_update_item_with_user(self):
        # test POST update
        blog_post = BlogPost.objects.first()
        # print(blog_post.content)
        url = blog_post.get_api_url()
        data = {"title": "Some random title", "content": "some more content"}

        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        #print(token_rsp)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)


    def test_post_item_with_user(self):
        # test POST list
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        data = {"title": "another random title", "content": "other more content"}
        url = api_reverse("api-pages:pages-listcreate")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #print

    def test_user_ownership(self):
        # test new user ownership
        owner = User.objects.create(username='testuser222')
        blog_post = BlogPost.objects.create(
            user=owner,
            title='New title',
            content='some_random_content'
            )

        user_obj = User.objects.first()
        #self.assertEqual(user_obj.username, owner.username)
        #print(User.objects.all())

        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        url = blog_post.get_api_url()
        data = {"title": "another random title", "content": "other more content"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login_and_update(self):
        data = {
            'username': 'testmyuser',
            'password': 'somepassword'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            blog_post = BlogPost.objects.first()
            # print(blog_post.content)
            url = blog_post.get_api_url()
            data = {"title": "Some random title", "content": "some more content"}

            # user_obj = User.objects.first()
            # payload = payload_handler(user_obj)
            # token_rsp = encode_handler(payload)

            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user(self):
        data = {
            'username': 'testmyuser',
            'password': 'somepassword'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        #print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            data = {
                'username': 'newuser1',
                'password': 'somepassword',
                'first_name': 'KT',
                'last_name': 'Lee',
            }
            url = api_reverse("api-pages:register")

            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

            response = self.client.post(url, data)
            print(User.objects.all())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

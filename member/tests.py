from unittest import mock
from django.test import TestCase, Client
from django.urls import reverse
from member.domains import Member
from django.contrib.auth.hashers import make_password
# Create your tests here.

class SignInTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signin_url = reverse('member:signin')
        self.member = Member(
            email="useruser@example.com",
            password=make_password("!123testtest"),
            name="test",
            phone_number="01000000000",
            nickname="닉네임",
            birthday="2019-08-24T14:15:22Z",
            dormitory_code="testcode",
            dormitory_card='url.com',
            status="ACTIVE"
        )
        self.member.save()
        
    def test_signin(self):
        signin_request_data = {
            "email": "useruser@example.com",
            "password": "!123testtest"
        }
        response = self.client.post(self.signin_url, signin_request_data)
        self.assertEqual(response.status_code, 200)
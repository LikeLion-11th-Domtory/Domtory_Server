from utils.exceptions import SamePasswordError, PasswordWrongError
from django.test import TestCase, Client
from django.urls import reverse
from member.domains import Member
from django.contrib.auth.hashers import make_password, check_password
from .containers import MembersContainer

class MemberTestCase(TestCase):
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
        member_container = MembersContainer
        self._member_serivce = member_container.member_service()
        
    def test_signin(self):
        signin_request_data = {
            "email": "useruser@example.com",
            "password": "!123testtest"
        }
        response = self.client.post(self.signin_url, signin_request_data)
        self.assertEqual(response.status_code, 200)

    def test_can_change_password(self):
        request_data = {
            "oldPassword": "!123testtest",
            "newPassword": "@123testtest"
        }
        self._member_serivce.change_password(request_data, self.member)
        self.assertTrue(check_password('@123testtest', self.member.password))
        
    def test_cant_change_password(self):
        request_data = {
            "oldPassword": "!testtest1234",
            "newPassword": "!testtest1234"
        }
        with self.assertRaises(PasswordWrongError):
            self._member_serivce.change_password(request_data, self.member)

    def test_same_change_password(self):
        request_data = {
            "oldPassword": "!123testtest",
            "newPassword": "!123testtest"
        }
        with self.assertRaises(SamePasswordError):
            self._member_serivce.change_password(request_data, self.member)

    def test_withdrwal_member(self):
        self._member_serivce.withdraw(self.member)
        self.assertEqual(self.member.status, 'WITHDRAWAL')
        self.assertEqual(self.member.name, 'unknown')
import json
import bcrypt
import jwt

from django.test import TestCase, Client

from users.models        import User
from transactions.models import Deposit, Bank
from my_settings         import MY_SECRET_KEY
from core.validation     import algorithm


class SignUpViewTest(TestCase):
    def setUp(self):
        self.cilent = Client()

        Bank.objects.create(id=1, name="NH_BANK")

        Deposit.objects.create(
            id                =1,
            withdrawal_account="111122223333",
            withdrawal_bank_id=1,
            deposit_account   ="444433332222",
            deposit_bank_id   =1,
            balance           =0,
        )

        User.objects.create(
            id      =1,
            name    ="전소민",
            email   ="junsomin@gmail.com",
            password="aa12341234!",
            deposit =Deposit.objects.get(id=1),
        )

    def tearDown(self):
        User.objects.all().delete()
        Deposit.objects.all().delete()
        Bank.objects.all().delete()

    def test_post_signup_success(self):
        data = {
            "name"          : "이광수",
            "email"         : "gwangsu@gmail.com",
            "password"      : "aa12341234!",
            "bank_name"     : "국민은행",
            "account_number": "124239429421",
        }

        response = self.client.post("/users/signup", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "SUCCESS"})

    def test_post_signup_duplicated_email(self):
        data = {
            "name"          : "이광수",
            "email"         : "junsomin@gmail.com",
            "password"      : "aa12341234!",
            "bank_name"     : "국민은행",
            "account_number": "124239429421",
        }

        response = self.client.post("/users/signup", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "DUPLICATED_EMAIL"})

    def test_post_signup_email_format_error(self):
        data = {
            "name"          : "이광수",
            "email"         : "gwangsugmail.com",
            "password"      : "aa12341234!",
            "bank_name"     : "국민은행",
            "account_number": "124239429421",
        }

        response = self.client.post("/users/signup", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "EMIAL_FORMAT_ERROR"})

    def test_post_signup_password_format_error(self):
        data = {
            "name"          : "이광수",
            "email"         : "gwangsu@gmail.com",
            "password"      : "aa12341234",
            "bank_name"     : "국민은행",
            "account_number": "124239429421",
        }

        response = self.client.post("/users/signup", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "PASSWORD_FORMAT_ERROR"})

    def test_post_signup_key_error(self):
        data = {
            "name"     : "이광수",
            "email"    : "gwangsu@gmail.com",
            "password" : "aa12341234!",
            "bank_name": "국민은행",
        }

        response = self.client.post("/users/signup", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})


class SignUpViewTest(TestCase):
    def setUp(self):
        self.cilent = Client()

        password = "aa12341234!"
        hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        Bank.objects.create(id=1, name="NH_BANK")

        Deposit.objects.create(
            id                =1,
            withdrawal_account="111122223333",
            withdrawal_bank_id=1,
            deposit_account   ="444433332222",
            deposit_bank_id   =1,
            balance           =0,
        )

        User.objects.create(
            id      =1,
            name    ="전소민",
            email   ="junsomin@gmail.com",
            password=hash_password.decode("utf-8"),
            deposit =Deposit.objects.get(id=1),
        )

    def tearDown(self):
        User.objects.all().delete()
        Deposit.objects.all().delete()
        Bank.objects.all().delete()

    def test_post_signin_success(self):
        data = {"email": "junsomin@gmail.com", "password": "aa12341234!"}

        user = User.objects.get(email="junsomin@gmail.com")
        access_token = jwt.encode({"user_id": user.id}, MY_SECRET_KEY, algorithm)

        response = self.client.post("/users/signin", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "SUCCESS", "token": access_token})

    def test_post_signin_invalid_user_email(self):
        data = {"email": "junsomi@gmail.com", "password": "aa12341234!"}

        response = self.client.post("/users/signin", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "INVALID_USER"})

    def test_post_signin_invalid_user_password(self):
        data = {"email": "junsomin@gmail.com", "password": "a12341234!"}

        response = self.client.post("/users/signin", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "INVALID_USER"})

    def test_post_signin_key_error(self):
        data = {"mail": "junsomin@gmail.com", "password": "aa12341234!"}

        response = self.client.post("/users/signin", json.dumps(data), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

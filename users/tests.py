import json
import bcrypt
import jwt
import unittest
import re

from django.http         import response
from django.test         import TestCase, Client
from codecs              import encode, decode
from transactions.models import Deposit, Bank
from users.models        import User
from my_settings         import MY_SECRET_KEY
from core.validation     import algorithm

client = Client()

class SignUpViewTest(TestCase):
    
    def setUp(self):
        
        Bank.objects.create(
            id   = 1,
            name = "NH_BANK"
        )
        
        Deposit.objects.create(
            id                 = 1,
            withdrawal_account = "111122223333",
            withdrawal_bank_id = 1,
            deposit_account    = "444433332222",
            deposit_bank_id    = 1,
            balance            = 0
        )
        
        User.objects.create(
            id   = 1,
            name = "전소민",
            email = "junsomin@gmail.com",
            password = "aa12341234!",
            deposit = Deposit.objects.get(id=1)
        )
        
    def tearDown(self):
        User.objects.all().delete()
        Deposit.objects.all().delete()
        Bank.objects.all().delete()
        
    def test_succuss_signup(self):
        
        data = {
            "name"           : "이광수",
            "email"          : "gwangsu@gmail.com",
            "password"       : "aa12341234!",
            "bank_name"      : 2,
            "account_number" : "124239429421"
        }
        
        response = client.post("/users/signup", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message" : "SUCCESS"})
        
    def test_fail_signup_exists_email(self):
        
        data = {
            "name"           : "이광수",
            "email"          : "junsomin@gmail.com",
            "password"       : "aa12341234!",
            "bank_name"      : 2,
            "account_number" : "124239429421"
        }
        
        response = client.post("/users/signup", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'EXIST_EMAIL'})
        
    def test_fail_signup_not_matched_email_from(self):
        
        data = {
            "name"           : "이광수",
            "email"          : "gwangsugmail.com",
            "password"       : "aa12341234!",
            "bank_name"      : 2,
            "account_number" : "124239429421"
        }
        
        response = client.post("/users/signup", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NOT_MATCHED_EMAIL_FORM'})

    def test_fail_signup_not_matched_password_from(self):
        
        data = {
            "name"           : "이광수",
            "email"          : "gwangsu@gmail.com",
            "password"       : "aa12341234",
            "bank_name"      : 2,
            "account_number" : "124239429421"
        }
        
        response = client.post("/users/signup", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NOT_MATCHED_PASSWORD_FORM'})
        
    def test_fail_signup_not_input_account(self):
        
        data = {
            "name"           : "이광수",
            "email"          : "gwangsu@gmail.com",
            "password"       : "aa12341234!",
            "bank_name"      : 2,
            "account_number" : ""
        }
        
        response = client.post("/users/signup", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NOT_INPUT_ACCOUNT'})
        
    def test_fail_signup_not_input_account(self):
        
        data = {
            "name"           : "이광수",
            "email"          : "gwangsu@gmail.com",
            "password"       : "aa12341234!",
            "bank_name"      : 2,
        }
        
        response = client.post("/users/signup", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "KEY_ERROR"})

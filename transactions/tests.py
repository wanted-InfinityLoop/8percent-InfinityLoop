import json
import jwt

from django.test import TestCase, Client

from transactions.models import *
from users.models        import User
from my_settings         import MY_SECRET_KEY


class DepositViewTest(TestCase):
    def setUp(self):
        Bank.objects.create(id=1, name="농협")

        Deposit.objects.create(
            id=1,
            withdrawal_account="914802-01-585494",
            withdrawal_bank_id=1,
            deposit_account="914802-02-333333",
            deposit_bank_id=1,
            balance=1000
        )
        User.objects.create(
            id=1,
            name="홍길동",
            email="dkfkffkf115@naver.com",
            password="@wjddl0616",
            deposit_id=1
        )
        self.user_token = jwt.encode(
            {
                "id": 1,
            },
            MY_SECRET_KEY,
            algorithm="HS256",
        )
        TransactionType.objects.create(id=1, name="DEPOSIT")

    def tearDown(self):
        User.objects.all().delete()
        Deposit.objects.all().delete()
        Bank.objects.all().delete()
        TransactionType.objects.all().delete()

    def test_deposit_post_success(self):
        client = Client()
        header = {"HTTP_Authorization": f"Bearer {self.user_token}"}
        data = {
            "amounts": 1000,
            "information": "입금테스트"
            }
        response = client.post(
            "/transactions/deposit",
            json.dumps(data),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "message"                  : "Success", 
                "user balance"             : 2000, 
                "user transaction type"    : "DEPOSIT",
                "user transaction amounts" : 1000,
                "user transactions balance": 2000
            }
        )

    def test_deposit_post_invalid_amounts(self):
        client = Client()
        header = {"HTTP_Authorization": {"HTTP_Authorization": f"Bearer {self.user_token}"}}
        data = {
                "amounts": -1000,
                "information": "입금테스트"
            }
        response = client.post(
            "/transactions/deposit",
            json.dumps(data),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Invalid Amount"})

    def test_deposit_post_type_error(self):
        client = Client()
        header = {"HTTP_Authorization": f"Bearer {self.user_token}"}
        data = {
                "amounts": "1000",
                "information": "입금테스트"
            }
        response = client.post(
            "/transactions/deposit",
            json.dumps(data),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Type Error"})

    def test_deposit_post_key_error(self):
        client = Client()
        header = {"HTTP_Authorization": f"Bearer {self.user_token}"}
        data = {
            "amount": 3000,
            "information": "입금테스트"
            }
        response = client.post(
            "/transactions/deposit",
            json.dumps(data),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Key Error"})


class WithdrawalTest(TestCase):
    def setUp(self):
        TransactionType.objects.create(id=2, name="출금")
        
        Bank.objects.create(id=1, name="농협은행")
        
        Deposit.objects.create(
            id=1,
            withdrawal_account="111-222-333",
            withdrawal_bank_id=1,
            deposit_account="444-555-666",
            deposit_bank_id=1,
            balance=30000,
        )

        User.objects.create(
            id=2,
            name="지윤",
            email="test@naver.com",
            password="1234!@qw",
            deposit_id=1
        )

        self.access_token1 = jwt.encode(
            {
                "id": 2,
            },
            MY_SECRET_KEY,
            algorithm="HS256",
        )

        self.access_token2 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ"

    def tearDown(self):
        User.objects.all().delete()
        Deposit.objects.all().delete()
        Bank.objects.all().delete()
        TransactionType.objects.all().delete()
    
    def test_withdrawal_post_success(self):
        client = Client()
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}
        data = {
            "amounts"         : 3000,
            "information"     : "출금 테스트"
        }
        response = client.post(
            "/transactions/withdrawal", 
            json.dumps(data), 
            content_type = "application/json",
            **header
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{"message": "Success", "거래 후 잔액": 27000})

    def test_withdrawal_post_invalid_input(self):
        client = Client()
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}
        data = {
            "amounts"         : -3000,
            "information"     : "출금 테스트"
        }
        response = client.post(
            "/transactions/withdrawal",
            json.dumps(data), 
            content_type = "application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Invalid Input"})

    def test_withdrawal_post_no_input(self):
        client = Client()
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}
        data = {
            "amounts"         : 3000,
            "information"     : ""
        }
        response = client.post(
            "/transactions/withdrawal",
            json.dumps(data),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "No Input"})
    
    def test_withdrawal_post_exceed_balance(self):
        client = Client()
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}
        data = {
            "amounts"         : 50000,
            "information"     : "출금 테스트"
        }
        response = client.post(
            "/transactions/withdrawal",
            json.dumps(data),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Wrong Request"})

    def test_withdrawal_post_type_error(self):
        client = Client()
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}
        data = {
            "amounts"         : "50000",
            "information"     : "출금 테스트"
        }
        response = client.post(
            "/transactions/withdrawal",
            json.dumps(data),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Type Error"})
    
    def test_withdrawal_post_key_error(self):
        client = Client()
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}
        data = {
            "amount"          : 50000,
            "information"     : "출금 테스트"
        }
        response = client.post(
            "/transactions/withdrawal",
            json.dumps(data),
            content_type="application/json",
            **header
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "Key Error"})
    
    # def test_withdrawal_user_does_not_exist(self):
    #     client = Client()
    #     header = {"HTTP_Authorization": f"Bearer {self.access_token2}"}
    #     data = {
    #         "amounts"         : 5000,
    #         "information"     : "출금 테스트"
    #     }
    #     response = client.post(
    #         "/transactions/withdrawal",
    #         json.dumps(data),
    #         content_type="application/json",
    #         **header
    #     )
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json(), {"message": "User Does Not Exist"})
    

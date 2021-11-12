import json
import jwt

from django.test import TestCase, Client

from users.models        import User
from transactions.models import *
from my_settings         import MY_SECRET_KEY
from core.validation     import algorithm


class DepositViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        TransactionType.objects.create(id=1, name="DEPOSIT")

        Bank.objects.create(id=1, name="농협은행")

        Deposit.objects.create(
            id                =1,
            withdrawal_account="914802-01-585494",
            withdrawal_bank_id=1,
            deposit_account   ="914802-02-333333",
            deposit_bank_id   =1,
            balance           =1000,
        )

        User.objects.create(
            id        =1,
            name      ="홍길동",
            email     ="dkfkffkf115@naver.com",
            password  ="@wjddl0616",
            deposit_id=1,
        )

        self.user_token = jwt.encode(
            {
                "user_id": 1,
            },
            MY_SECRET_KEY,
            algorithm,
        )

        self.access_token2 = jwt.encode(
            {
                "user_id": 2,
            },
            MY_SECRET_KEY,
            algorithm,
        )

    def tearDown(self):
        User.objects.all().delete()
        Deposit.objects.all().delete()
        Bank.objects.all().delete()
        TransactionType.objects.all().delete()

    def test_post_deposit_success(self):
        header = {"HTTP_Authorization": f"Bearer {self.user_token}"}
        data = {"amounts": 1000, "information": "입금테스트"}

        response = self.client.post(
            "/transactions/deposit",
            json.dumps(data),
            content_type="application/json",
            **header,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "message": "SUCCESS",
                "balance": 2000,
            },
        )

    def test_post_deposit_invalid_input_format_negative_number(self):
        header = {"HTTP_Authorization": f"Bearer {self.user_token}"}
        data = {"amounts": -1000, "information": "입금테스트"}

        response = self.client.post(
            "/transactions/deposit",
            json.dumps(data),
            content_type="application/json",
            **header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_INPUT_FORMAT"})

    def test_post_deposit_invalid_input_format_float_number(self):
        header = {"HTTP_Authorization": f"Bearer {self.user_token}"}
        data = {"amounts": 1000.8, "information": "입금테스트"}

        response = self.client.post(
            "/transactions/deposit",
            json.dumps(data),
            content_type="application/json",
            **header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_INPUT_FORMAT"})

    def test_post_deposit_type_error(self):
        header = {"HTTP_Authorization": f"Bearer {self.user_token}"}
        data = {"amounts": "1000", "information": "입금테스트"}

        response = self.client.post(
            "/transactions/deposit",
            json.dumps(data),
            content_type="application/json",
            **header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "TYPE_ERROR"})

    def test_post_deposit_key_error(self):
        header = {"HTTP_Authorization": f"Bearer {self.user_token}"}
        data = {"amount": 3000, "information": "입금테스트"}

        response = self.client.post(
            "/transactions/deposit",
            json.dumps(data),
            content_type="application/json",
            **header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

    def test_post_deposit_invalid_user(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token2}"}
        data = {"amounts": 5000, "information": "입금 테스트"}

        response = self.client.post(
            "/transactions/deposit",
            json.dumps(data),
            content_type="application/json",
            **header,
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "INVALID_USER"})


class WithdrawalTest(TestCase):
    def setUp(self):
        self.client = Client()

        TransactionType.objects.create(id=2, name="출금")

        Bank.objects.create(id=1, name="농협은행")

        Deposit.objects.create(
            id                =1,
            withdrawal_account="111-222-333",
            withdrawal_bank_id=1,
            deposit_account   ="444-555-666",
            deposit_bank_id   =1,
            balance           =30000,
        )

        User.objects.create(
            id        =1, 
            name      ="지윤", 
            email     ="test@naver.com", 
            password  ="1234!@qw", 
            deposit_id=1
        )

        self.access_token1 = jwt.encode(
            {
                "user_id": 1,
            },
            MY_SECRET_KEY,
            algorithm,
        )

        self.access_token2 = jwt.encode(
            {
                "user_id": 2,
            },
            MY_SECRET_KEY,
            algorithm,
        )

    def tearDown(self):
        User.objects.all().delete()
        Deposit.objects.all().delete()
        Bank.objects.all().delete()
        TransactionType.objects.all().delete()

    def test_post_withdrawal_success(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}
        data = {"amounts": 3000, "information": "출금 테스트"}

        response = self.client.post(
            "/transactions/withdrawal",
            json.dumps(data),
            content_type="application/json",
            **header,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "SUCCESS", "balance": 27000})

    def test_post_withdrawal_invalid_input_negative_number(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}
        data = {"amounts": -3000, "information": "출금 테스트"}

        response = self.client.post(
            "/transactions/withdrawal",
            json.dumps(data),
            content_type="application/json",
            **header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_INPUT_FORMAT"})

    def test_post_withdrawal_invalid_input_float_number(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}
        data = {"amounts": 3000.8, "information": "출금 테스트"}

        response = self.client.post(
            "/transactions/withdrawal",
            json.dumps(data),
            content_type="application/json",
            **header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_INPUT_FORMAT"})

    def test_post_withdrawal_exceed_balance(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}
        data = {"amounts": 50000, "information": "출금 테스트"}

        response = self.client.post(
            "/transactions/withdrawal",
            json.dumps(data),
            content_type="application/json",
            **header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "WRONG_REQUEST"})

    def test_post_withdrawal_type_error(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}
        data = {"amounts": "50000", "information": "출금 테스트"}

        response = self.client.post(
            "/transactions/withdrawal",
            json.dumps(data),
            content_type="application/json",
            **header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "TYPE_ERROR"})

    def test_post_withdrawal_key_error(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}
        data = {"amount": 50000, "information": "출금 테스트"}

        response = self.client.post(
            "/transactions/withdrawal",
            json.dumps(data),
            content_type="application/json",
            **header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})

    def test_withdrawal_user_does_not_exist(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token2}"}
        data = {"amounts": 5000, "information": "출금 테스트"}

        response = self.client.post(
            "/transactions/withdrawal",
            json.dumps(data),
            content_type="application/json",
            **header,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "INVALID_USER"})


class TransactionHistoryTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.client = Client()

        TransactionType.objects.create(id=1, name="입금")

        Bank.objects.create(id=1, name="농협은행")

        deposit = Deposit.objects.create(
            id                =1,
            withdrawal_account="111-222-333",
            withdrawal_bank_id=1,
            deposit_account   ="444-555-666",
            deposit_bank_id   =1,
            balance           =30000,
        )

        User.objects.create(
            id        =1, 
            name      ="지윤", 
            email     ="test@naver.com", 
            password  ="1234!@qw", 
            deposit_id=1
        )

        Transaction.objects.create(
            type_id    =1,
            information="테스트 입금",
            amounts    =8000,
            balance    =38000,
            user_id    =1
        )

        deposit.balance += 8000
        deposit.save()

        self.access_token1 = jwt.encode(
            {
                "user_id": 1,
            },
            MY_SECRET_KEY,
            algorithm,
        )

        self.access_token2 = jwt.encode(
            {
                "user_id": 2,
            },
            MY_SECRET_KEY,
            algorithm,
        )

    def tearDown(self):
        User.objects.all().delete()
        Deposit.objects.all().delete()
        Bank.objects.all().delete()
        TransactionType.objects.all().delete()

    def test_get_transaction_history(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}

        response = self.client.get(
            "/transactions/history",
            **header,
        )

        transaction = Transaction.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "results" :{
                "transactions": [
                    {
                        "created_time": transaction.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "amounts": 8000,
                        "balance": 38000,
                        "information": "테스트 입금",
                        "type": "입금",
                    }
                ],
                "general_information": {
                    "deposit_counts": 1,
                    "deposit_sum_amounts": 8000,
                    "withdrawal_counts": 0,
                    "withdrawal_sum_amounts": 0,
                    "blance": 38000,
                },
            }})

    def test_get_transaction_history_value_error(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}

        response = self.client.get(
            "/transactions/history?type_id=입금",
            **header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "VALUE_ERROR"})

    def test_get_transaction_history_invalid_query_format(self):
        header = {"HTTP_Authorization": f"Bearer {self.access_token1}"}

        response = self.client.get(
            "/transactions/history?start_day=20210112",
            **header,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message": "INVALID_QUERY_FORMAT"})
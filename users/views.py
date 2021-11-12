import json
import bcrypt
import jwt
from uuid import uuid4

from django.db import transaction
from django.views import View
from django.http import JsonResponse

from users.models import User
from transactions.models import Bank, Deposit
from my_settings import MY_SECRET_KEY
from core.validation import email_validation, password_validation, algorithm


class SignUpView(View):
    def post(self, request):
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                password = data["password"]

                if User.objects.filter(email=data["email"]).exists():
                    return JsonResponse({"message": "DUPLICATED_EMAIL"}, status=400)

                if not email_validation.match(data["email"]):
                    return JsonResponse({"message": "EMIAL_FORMAT_ERROR"}, status=400)

                if not password_validation.match(data["password"]):
                    return JsonResponse({"message": "PASSWORD_FORMAT_ERROR"}, status=400)

                bank_created = Bank.objects.get_or_create(name=data["bank_name"])

                deposit_created = Deposit.objects.create(
                    withdrawal_account=data["account_number"],
                    withdrawal_bank   =bank_created[0],
                    deposit_account   =str(uuid4().int)[:14],
                    deposit_bank_id   =Bank.DefaultBank.NH_BANK.value,
                )

                User.objects.create(
                    email   =data["email"],
                    name    =data["name"],
                    password=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                    deposit =deposit_created,
                )

                return JsonResponse({"message": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            user = User.objects.get(email=data["email"])

            if not bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            access_token = jwt.encode({"user_id": user.id}, MY_SECRET_KEY, algorithm)

            return JsonResponse({"message": "SUCCESS", "token": access_token}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

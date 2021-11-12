import json
import bcrypt
import re
from django import views
import jwt

from django.views        import View
from django.http         import HttpResponse, JsonResponse
from users.models        import User
from transactions.models import Bank, Deposit, Transaction
from my_settings         import MY_SECRET_KEY
from core.validation     import email_validation, password_validation, algorithm
from uuid                import uuid4
from django.db           import transaction
from core.utils          import LoginDecorator

class SignUpView(View):
    def post(self, request):
        try:
            with transaction.atomic():
                data               = json.loads(request.body)
            
                email              = data["email"]
                password           = data["password"]
                name               = data["name"]
                withdrawal_account = data["account_number"]
        
                if User.objects.filter(email=email).exists():
                    return JsonResponse({'message' : 'EXIST_EMAIL'}, status=400)
        
                if not email_validation.match(email):
                    return JsonResponse({'message' : 'NOT_MATCHED_EMAIL_FORM'}, status=400)
            
                if not password_validation.match(password):
                    return JsonResponse({'message' : 'NOT_MATCHED_PASSWORD_FORM'}, status=400)
                
                if not withdrawal_account:
                    return JsonResponse({'message' : 'NOT_INPUT_ACCOUNT'}, status=400)
            
                bank_created = Bank.objects.get_or_create(name=data["bank_name"])
            
                deposit_created = Deposit.objects.create(
                    withdrawal_account = withdrawal_account,
                    withdrawal_bank    = bank_created[0],
                    deposit_account    = str(uuid4().int)[:14],
                    deposit_bank_id    = Bank.DefaultBank.NH_BANK.value
                )
    
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                User.objects.create(
                    email    = email,
                    name     = name,
                    password = hashed_password.decode("utf-8"),
                    deposit  = deposit_created
                    )
                
                return JsonResponse({"message" : "SUCCESS"}, status=200)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

class SigninView(View):
    def post(self, request):
        
        try:
            data     = json.loads(request.body)
            
            email    = data["email"]
            password = data["password"]
            
            user_check = User.objects.filter(email=email).first()
            
            if not user_check:
                return JsonResponse({"message" : "INVALED_USER"}, status=400)
            
            if not bcrypt.checkpw(password.encode("utf-8"), user_check.password.encode("utf-8")):
                return JsonResponse({"message" : "INVALID_USER_PASSWORD"}, status=400)
            
            access_token = jwt.encode({"user_id" : user_check.id}, MY_SECRET_KEY, algorithm)
            
            return JsonResponse({"message" : access_token}, status=200)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

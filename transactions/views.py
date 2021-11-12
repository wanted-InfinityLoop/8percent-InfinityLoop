import json

from django.http.response import JsonResponse
from django.views import View
from django.db import transaction

from transactions.models import *
from users.models import *


class DepositView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
            deposit = User.objects.get(id=1).deposit # request.user.deposit
            
            if data["amounts"] <= 0:
                return JsonResponse({"message": "Invalid Amount"}, status=400)

            with transaction.atomic():
                transaction_info = Transaction.objects.create(
                    type_id      = TransactionType.Type.DEPOSIT.value,
                    information  = data["information"],
                    amounts      = data["amounts"],
                    balance      = deposit.balance + data["amounts"],
                    user_id      = 1 # request.user가능
                )

                deposit.balance += data["amounts"]
                deposit.save()

            return JsonResponse({"message"                 : "Success",
                                "user balance"             : deposit.balance,
                                "user transaction type"    : transaction_info.type.name,
                                "user transaction amounts" : transaction_info.amounts,
                                "user transactions balance": transaction_info.balance
                                }, status=201)

        except KeyError:    
            return JsonResponse({"message": "Key Error"}, status=400)

        except TypeError:
            return JsonResponse({"message": "Type Error"}, status=400)

import json

from django.http      import JsonResponse
from django.views     import View
from django.db        import transaction

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


class WithdrawalView(View):

    def post(self, request):
        try:
            data             = json.loads(request.body)
            amounts          = data["amounts"]
            information      = data["information"]
            # user             = request.user
            user = User.objects.get(id=2)   # 추후 삭제할 예정

            if amounts <= 0:
                return JsonResponse({"message": "Invalid Input"}, status=400)
            
            if not amounts or not information:
                return JsonResponse({"message": "No Input"}, status=400)

            # if not user:
            #     return JsonResponse({"message": "User Does Not Exist"}, status=400)

            if amounts > user.deposit.balance:
                return JsonResponse({"message": "Wrong Request"}, status=400)

            with transaction.atomic():
                new_transaction = Transaction.objects.create(
                    type_id    =TransactionType.Type.WITHDRAWAL.value,
                    information=information,
                    amounts    =amounts,
                    balance    =user.deposit.balance - amounts,
                    user       =user
                )
                user.deposit.balance = new_transaction.balance
                user.deposit.save()

            return JsonResponse({"message": "Success", "거래 후 잔액": new_transaction.balance}, status=201)

        except TypeError:
            return JsonResponse({"message": "Type Error"}, status=400)

        except KeyError:
            return JsonResponse({"message": "Key Error"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message":"User Does Not Exist"}, status=400)  # login_decorator 붙이면 삭제하기
            
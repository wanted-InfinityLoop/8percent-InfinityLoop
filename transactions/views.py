import json
from datetime               import date, timedelta

from django.http            import JsonResponse
from django.views           import View
from django.db              import transaction
from django.db.models       import Sum
from django.db.models       import Q
from django.core.exceptions import ValidationError

from transactions.models    import TransactionType, Transaction
from users.models           import User


class DepositView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
            deposit = User.objects.get(id=1).deposit  # request.user.deposit

            if data["amounts"] <= 0:
                return JsonResponse({"message": "Invalid Amount"}, status=400)

            with transaction.atomic():
                transaction_info = Transaction.objects.create(
                    type_id    =TransactionType.Type.DEPOSIT.value,
                    information=data["information"],
                    amounts    =data["amounts"],
                    balance    =deposit.balance + data["amounts"],
                    user_id    =1,  # request.user가능
                )

                deposit.balance += data["amounts"]
                deposit.save()

            return JsonResponse(
                {
                    "message": "Success",
                    "user balance": deposit.balance,
                    "user transaction type": transaction_info.type.name,
                    "user transaction amounts": transaction_info.amounts,
                    "user transactions balance": transaction_info.balance,
                },
                status=201,
            )

        except KeyError:
            return JsonResponse({"message": "Key Error"}, status=400)

        except TypeError:
            return JsonResponse({"message": "Type Error"}, status=400)


class WithdrawalView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            amounts = data["amounts"]
            information = data["information"]
            # user             = request.user
            user = User.objects.get(id=1)  # 추후 삭제할 예정

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
                    type_id=TransactionType.Type.WITHDRAWAL.value,
                    information=information,
                    amounts=amounts,
                    balance=user.deposit.balance - amounts,
                    user=user,
                )
                user.deposit.balance = new_transaction.balance
                user.deposit.save()

            return JsonResponse(
                {"message": "SUCESS", "balance": new_transaction.balance}, status=201
            )

        except TypeError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message": "User Does Not Exist"}, status=400)  # login_decorator 붙이면 삭제하기


class TransactionHistoryView(View):
    # @login_decorator
    def get(self, request):
        try:
            user    = User.objects.get(id=1)
            deposit = user.deposit

            PAGE   = int(request.GET.get("page", 1))
            LIMIT  = 20
            OFFSET = (PAGE - 1) * LIMIT

            TYPE_ID    = request.GET.get("type_id", None)
            START_DATE = request.GET.get("start_day", date.today() - timedelta(days=90))
            END_DATE   = request.GET.get("end_day", date.today())

            elements      = list(map(int, END_DATE.split("-")))
            FULL_END_DATE = date(elements[0], elements[1], elements[2] + 1)

            q = Q()

            if TYPE_ID:
                q = Q(type_id=TYPE_ID)

            q &= Q(created_time__range=(START_DATE, FULL_END_DATE))

            transactions            = Transaction.objects.filter(user=1).filter(q).order_by("-created_time")
            depoist_transactions    = transactions.filter(type_id=TransactionType.Type.DEPOSIT.value)
            withdrawal_transactions = transactions.filter(type_id=TransactionType.Type.WITHDRAWAL.value)

            result = {
                "transactions": [
                    {
                        "created_time": transaction.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "amounts": transaction.amounts,
                        "balance": transaction.balance,
                        "information": transaction.information,
                        "type": transaction.type.name,
                    }
                    for transaction in transactions[OFFSET : OFFSET + LIMIT]
                ],
                "general_information": {
                    "deposit_counts": depoist_transactions.count(),
                    "deposit_sum_amounts": depoist_transactions.aggregate(sum_amount=Sum("amounts")).get("sum_amount") or 0,
                    "withdrawal_counts": withdrawal_transactions.count(),
                    "withdrawal_sum_amounts": withdrawal_transactions.aggregate(sum_amount=Sum("amounts")).get("sum_amount") or 0,
                    "blance": deposit.balance,
                },
            }

            return JsonResponse({"results": result}, status=200)

        except ValidationError:
            return JsonResponse({"message": "INVALID_QUERY_FORMAT"}, status=400)

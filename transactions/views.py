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
from core.utils             import login_decorator


class DepositView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)

            if data["amounts"] <= 0:
                return JsonResponse({"message": "INVALID_INPUT_FORMAT"}, status=400)
            
            if type(data["amounts"]) is float:
                return JsonResponse({"message": "INVALID_INPUT_FORMAT"}, status=400)

            deposit = request.user.deposit

            with transaction.atomic():
                Transaction.objects.create(
                    type_id    =TransactionType.Type.DEPOSIT.value,
                    information=data["information"],
                    amounts    =data["amounts"],
                    balance    =deposit.balance + data["amounts"],
                    user       =request.user,  
                )

                deposit.balance += data["amounts"]
                deposit.save()

            return JsonResponse({"message": "SUCCESS", "balance": deposit.balance}, status=201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except TypeError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)


class WithdrawalView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            deposit = request.user.deposit

            if data["amounts"] <= 0:
                return JsonResponse({"message": "INVALID_INPUT_FORMAT"}, status=400)

            if data["amounts"] > deposit.balance:
                return JsonResponse({"message": "WRONG_REQUEST"}, status=400)

            if type(data["amounts"]) is float:
                return JsonResponse({"message": "INVALID_INPUT_FORMAT"}, status=400)

            with transaction.atomic():
                Transaction.objects.create(
                    type_id=TransactionType.Type.WITHDRAWAL.value,
                    information=data["information"],
                    amounts=data["amounts"],
                    balance=deposit.balance - data["amounts"],
                    user=request.user
                )

                deposit.balance -= data["amounts"]
                deposit.save()

            return JsonResponse(
                {"message": "SUCCESS", "balance": deposit.balance}, status=201
            )

        except TypeError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class TransactionHistoryView(View):
    @login_decorator
    def get(self, request):
        try:
            deposit = request.user.deposit

            PAGE   = int(request.GET.get("page", 1))
            LIMIT  = 20
            OFFSET = (PAGE - 1) * LIMIT

            TYPE_ID    = request.GET.get("type_id", None)
            START_DATE = request.GET.get("start_day", date.today() - timedelta(days=90))
            END_DATE   = request.GET.get("end_day", None)

            if END_DATE:
                elements = list(map(int, END_DATE.split("-")))
                FULL_END_DATE = date(elements[0], elements[1], elements[2] + 1)
            else:
                FULL_END_DATE = date.today() + timedelta(days=1)

            q = Q()

            if TYPE_ID:
                q = Q(type_id=TYPE_ID)

            q &= Q(created_time__range=(START_DATE, FULL_END_DATE))

            transactions            = Transaction.objects.filter(user=request.user).filter(q).order_by("-created_time")
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

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

        except ValidationError:
            return JsonResponse({"message": "INVALID_QUERY_FORMAT"}, status=400)

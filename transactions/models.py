from django.db import models

from core.models import TimeStamp


class Bank(models.Model):
    class DefaultBank(models.IntegerChoices):
        NH_BANK = 1

    name = models.CharField(max_length=32)

    class Meta:
        db_table = "banks"


class Deposit(models.Model):
    withdrawal_account = models.CharField(max_length=32)
    withdrawal_bank = models.ForeignKey(Bank, related_name="deposit_withdrawal", on_delete=models.PROTECT)
    deposit_account = models.CharField(max_length=32, unique=True)
    deposit_bank = models.ForeignKey(Bank, related_name="deposit", on_delete=models.PROTECT)
    balance = models.PositiveBigIntegerField(default=0)

    class Meta:
        db_table = "deposit"


class TransactionType(models.Model):
    class Type(models.IntegerChoices):
        DEPOSIT = 1
        WITHDRAWAL = 2

    name = models.CharField(max_length=16)

    class Meta:
        db_table = "transaction_types"


class Transaction(TimeStamp):
    type = models.ForeignKey(TransactionType, on_delete=models.PROTECT)
    information = models.CharField(max_length=64)
    amounts = models.PositiveIntegerField()
    balance = models.PositiveBigIntegerField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        db_table = "transactions"

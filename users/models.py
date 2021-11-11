from django.db import models


class User(models.Model):
    name     = models.CharField(max_length=32)
    email    = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    deposit  = models.OneToOneField("transactions.Deposit", on_delete=models.PROTECT)

    class Meta:
        db_table = "users"

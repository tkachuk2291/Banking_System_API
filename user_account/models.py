from django.contrib.auth.models import AbstractUser
from django.db import models


class UserAccount(AbstractUser):
    pass


class Account(models.Model):
    account_id = models.AutoField(primary_key=True, db_column="account_id")
    user = models.ForeignKey(UserAccount, models.CASCADE)
    name = models.CharField(max_length=256)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

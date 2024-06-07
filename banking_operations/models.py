from django.db import models


class Deposit(models.Model):
    account_id = models.ForeignKey('user_account.Account', on_delete=models.CASCADE, related_name='account_deposit')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)

    def __str__(self):
        pass


class Withdrawal(models.Model):
    account_id = models.ForeignKey('user_account.Account', on_delete=models.CASCADE, related_name='account_withdrawal')
    amount = models.FloatField(null=False)

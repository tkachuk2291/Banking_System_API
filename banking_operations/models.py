from django.db import models


class Deposit(models.Model):
    account_id = models.AutoField(primary_key=True, db_column='account_id')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)

    def __str__(self):
        return f"{self.amount} | {self.account_id}"


class Withdrawal(models.Model):
    account_id = models.AutoField(primary_key=True, db_column='account_id')
    amount = models.FloatField(null=False)

    def __str__(self):
        return f"{self.account_id} | {self.amount}"



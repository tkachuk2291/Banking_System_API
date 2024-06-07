from django.db import models


class Deposit(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        pass

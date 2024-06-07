from rest_framework import serializers

from banking_operations.models import Deposit


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ('account_id', 'amount')

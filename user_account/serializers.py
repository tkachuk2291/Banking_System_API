from rest_framework import serializers

from user_account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('account_id', 'name', "initial_balance")

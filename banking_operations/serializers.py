from rest_framework import serializers

from banking_operations.models import Deposit


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ('account_id', 'amount')

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()
        return instance

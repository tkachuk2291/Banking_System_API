from django.shortcuts import render
from rest_framework import generics
from banking_operations.models import Deposit
from banking_operations.serializers import DepositSerializer


# Create your views here.
class BankDeposit(generics.CreateAPIView):
    model = Deposit
    serializer_class = DepositSerializer

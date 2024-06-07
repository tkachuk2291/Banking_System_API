from django.shortcuts import render
from rest_framework import generics

from user_account.models import Account
from user_account.serializers import AccountSerializer


class UserAccount(generics.CreateAPIView):
    model = Account
    serializer_class = AccountSerializer

from django.urls import path

from banking_operations.views import BankDeposit

urlpatterns = [
    path("deposit/", BankDeposit.as_view(), name="deposit"),
    # path("withdraw/", BestSellers.as_view(), name="withdraw"),
    # path("transfer/", BestSellers.as_view(), name="transfer"),

]
app_name = "banking_operations"

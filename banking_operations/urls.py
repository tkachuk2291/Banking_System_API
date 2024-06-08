from django.urls import path

from banking_operations.views import deposit, withdraw, transfer

# DepositEndpoint

urlpatterns = [
    path("deposit/", deposit, name="deposit"),
    path("withdraw/", withdraw, name="withdraw"),
    path("transfer/", transfer, name="transfer"),

]
app_name = "banking_operations"

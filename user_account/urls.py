from django.urls import path

from user_account.views import UserAccount

urlpatterns = [
    path("create_account/", UserAccount.as_view(), name="registration"),


]
app_name = "user_account"

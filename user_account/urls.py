from django.urls import path

from banking_operations.views import account, user_profile

urlpatterns = [
    path("create_user_profile/", user_profile, name="registration"),
    path("create_account/", account, name="registration"),


]
app_name = "user_account"

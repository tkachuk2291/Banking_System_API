from django.urls import path

from user_account.views import user_profile, account

urlpatterns = [
    path("create_user_profile/", user_profile, name="registration_user_profile"),
    path("create_account/", account, name="registration_account"),
]
app_name = "user_account"

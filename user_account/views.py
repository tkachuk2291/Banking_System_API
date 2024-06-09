import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging
from user_account.models import Account, UserAccount

logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([AllowAny])
@csrf_exempt
def user_profile(request):
    try:
        data = json.loads(request.body)
        username = data["username"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        password = data["password"]
        repeat_password = data["repeat_password"]

        if not isinstance(username, str):
            logger.error(f"error | Bad request, {username} must be a string")
            return JsonResponse({"error": f"Bad request, {username} must be a string"}, status=400)
        if not isinstance(first_name, str):
            logger.error(f"error | Bad request, {first_name} must be a string")

            return JsonResponse({"error": f"Bad request, {first_name} must be a string"}, status=400)
        if not isinstance(last_name, str):
            logger.error(f"error | Bad request, {last_name} must be a string")

            return JsonResponse({"error": f"Bad request, {last_name} must be a string"}, status=400)
    except KeyError:
        logger.error(
            f"error | Bad request,fields: username,first_name,last_name ,  initial_balance , password , repeat_password are required")

        return JsonResponse(
            {
                "error": "Bad request,fields: username,first_name,last_name ,  initial_balance , password , repeat_password are required"
            },
            status=400,
        )
    if password == repeat_password:
        try:
            user_profile_bank = UserAccount.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, password=password
            )
            return JsonResponse({"profile_created": f"Profile created successfully,"
                                                    f" profile information:username:{username} ,"
                                                    f"first_name: {first_name} ,"
                                                    f"last_name : {last_name}"}, status=201)
        except IntegrityError:
            logger.error(
                f"error |Error username '{username}' is already taken, please select another username and try again")

            return JsonResponse(
                {
                    "error": f"Error username '{username}' is already taken, please select another username and try again"},
                status=400
            )
    logger.error(f"error | Bad request, passwords must be match please check and try again")
    return JsonResponse(
        {"error": "Bad request, passwords must be match please check and try again"}, status=400
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def account(request):
    global user_account
    try:
        data = json.loads(request.body)
        account_name = data["account_name"]
        initial_balance = data["initial_balance"]
        user_id = request.user.id
        if not isinstance(account_name, str):
            logger.error(f"error | Invalid format | error , account_name {account_name} must be a string")
            return JsonResponse({"Invalid format": f"error , account_name {account_name} must be a string"}, status=400)
        if not isinstance(initial_balance, (int, float)):
            logger.error(f"Invalid format | error , account_name {account_name} must be a string")
            return JsonResponse(
                {"Invalid format": f"error, initial_balance {initial_balance} must be a number"}, status=400
            )
    except KeyError:
        logger.error(f"error | Bad request, account_name,initial_balance and user_id are required")

        return JsonResponse(
            {"error": "Bad request, account_name,initial_balance and user_id are required"}, status=400
        )
    user_profile = UserAccount.objects.get(id=user_id)
    try:
        user_account = Account.objects.create(
            name=account_name, user=user_profile, initial_balance=initial_balance
        )
        return JsonResponse(
            {
                "account created success": f"account_id: {user_account.account_id}| account_name: {user_account.name} | initial_balance: {user_account.initial_balance}"
            },
            status=201,
        )

    except IntegrityError:
        user_account = UserAccount.objects.get(id=user_id)
        user_account_name = user_account.related_user_account.name
        user_account_id = user_account.related_user_account.account_id
        user_initial_balance = user_account.related_user_account.initial_balance
        logger.error(
            f"account already created | you have account_id: {user_account_id} | account_name: {user_account_name} | initial_balance: {user_initial_balance}")

        return JsonResponse(
            {
                "account already created": f"you have account_id: {user_account_id} | account_name: {user_account_name} | initial_balance: {user_initial_balance}"
            },
            status=400,
        )

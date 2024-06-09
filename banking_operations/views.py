import json
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
import logging
from user_account.models import Account
logger = logging.getLogger(__name__)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def deposit(request):
    try:
        data = json.loads(request.body)
        account_id = data["account_id"]
        amount = data["amount"]
        if not isinstance(account_id, int):
            logger.error(f"Bad request, {account_id} must be an integer")
            return JsonResponse({"error": f"Bad request, {account_id} must be an integer"}, status=400)
        if not isinstance(amount, (int, float)):
            logger.error(f"Bad request, {amount} must be a number")
            return JsonResponse({"error": f"Bad request, {amount} must be a number"}, status=400)
    except KeyError:
        logger.error(f"Bad request, account_id and amount are required")

        return JsonResponse(
            {"error": "Bad request, account_id and amount are required"}, status=400
        )
    account = get_object_or_404(Account, account_id=account_id)
    account.initial_balance += amount
    account.save()
    logger.info(f"updated_balance to {account_id} | current balance is {account.initial_balance}")

    return JsonResponse({f"updated_balance to {account_id}":  f"current balance is {account.initial_balance}"}, status=201)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def withdraw(request):
    try:
        data = json.loads(request.body)
        account_id = data["account_id"]
        amount = data["amount"]
        if not isinstance(account_id, int):
            logger.error(f"error | Bad request, {account_id} must be an integer")
            return JsonResponse({"error": f"Bad request, {account_id} must be an integer"}, status=400)
        if not isinstance(amount, (int, float)):
            logger.error(f"error |Bad request, {amount} must be a number")
            return JsonResponse({"error": f"Bad request, {amount} must be a number"}, status=400)
    except KeyError:
        logger.error(f"error |Bad request, account_id and amount are required")
        return JsonResponse(
            {"error": "Bad request, account_id and amount are required"}, status=400
        )
    account = get_object_or_404(Account, account_id=account_id)
    if account.initial_balance >= amount:
        account.initial_balance -= amount
        account.save()
        logger.info(f"withdraw |{amount} | current_balance: {account.initial_balance}")
        response_data = {"withdraw": f"{amount}", "current_balance": f"{account.initial_balance}"}
        return JsonResponse(response_data, status=200)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@csrf_exempt
def transfer(request):
    with transaction.atomic():
        try:
            data = json.loads(request.body)
            from_account_id = data["from_account_id"]
            to_account_id = data["to_account_id"]
            amount = data["amount"]
            if not isinstance(from_account_id, int):
                logger.error(f"Bad request, {from_account_id} must be an integer")
                return JsonResponse(
                    {"error": f"Bad request, {from_account_id} must be an integer"}, status=400
                )
            if not isinstance(to_account_id, int):
                logger.error(f"error | Bad request, {to_account_id} must be an integer")
                return JsonResponse(
                    {"error": f"Bad request, {to_account_id} must be an integer"}, status=400
                )
            if not isinstance(amount, int):
                logger.error(f"error | Bad request, {amount} must be a number")

                return JsonResponse({"error": f"Bad request, {amount} must be a number"}, status=400)
        except KeyError:
            logger.error(f"error | Bad request, from_account_id, to_account_id, and amount are required")

            return JsonResponse(
                {"error": "Bad request, from_account_id, to_account_id, and amount are required"},
                status=400,
            )
        try:
            from_account_id_obj = Account.objects.get(account_id=from_account_id)
        except Account.DoesNotExist:
            logger.error(f"error | Source account not found")

            return JsonResponse({"error": "Source account not found"}, status=404)
        try:
            to_account_id_obj = Account.objects.get(account_id=to_account_id)
        except Account.DoesNotExist:
            logger.error(f"error | Destination account not found")

            return JsonResponse({"error": "Destination account not found"}, status=404)

        if from_account_id_obj.initial_balance >= amount:
            from_account_id_obj.initial_balance -= amount
            from_account_id_obj.save()
            to_account_id_obj.initial_balance += amount
            to_account_id_obj.save()
            response_data = {
                "from_account_id_current_balance": from_account_id_obj.initial_balance,
                "to_account_id_balance": to_account_id_obj.initial_balance,
            }
            logger.info(f"success created| {response_data}")

            return JsonResponse(response_data, status=200)
        logger.error(f"not enough money | error not enough money in account {from_account_id_obj.initial_balance} to execute the transfer  need amount  <= {amount}")

        return JsonResponse(
            {
                "not enough money": f"error not enough money in account {from_account_id_obj.initial_balance} to execute the transfer you need amount  <= {amount}"
            },
            status=400,
        )

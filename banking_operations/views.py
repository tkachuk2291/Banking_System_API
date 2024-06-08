import json
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from user_account.models import Account


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def deposit(request):
    try:
        data = json.loads(request.body)
        account_id = data['account_id']
        amount = data['amount']
        if not isinstance(account_id, int):
            return JsonResponse({'error': 'Bad request, account_id must be an integer'}, status=400)
        if not isinstance(amount, (int, float)):
            return JsonResponse({'error': 'Bad request, amount must be a number'}, status=400)
    except KeyError:
        return JsonResponse({'error': 'Bad request, account_id and amount are required'}, status=400)
    account = get_object_or_404(Account, account_id=account_id)
    account.initial_balance += amount
    account.save()
    return JsonResponse({'updated_balance': account.initial_balance}, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def withdraw(request):
    try:
        data = json.loads(request.body)
        account_id = data['account_id']
        amount = data['amount']
        if not isinstance(account_id, int):
            return JsonResponse({'error': 'Bad request, account_id must be an integer'}, status=400)
        if not isinstance(amount, (int, float)):
            return JsonResponse({'error': 'Bad request, amount must be a number'}, status=400)
    except KeyError:
        return JsonResponse({'error': 'Bad request, account_id and amount are required'}, status=400)
    account = get_object_or_404(Account, account_id=account_id)
    if account.initial_balance >= amount:
        account.initial_balance -= amount
        account.save()
        response_data = {
            'withdraw': f"{amount}",
            'current_balance': f"{account.initial_balance}"
        }
        return JsonResponse(response_data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def transfer(request):
    with transaction.atomic():
        try:
            data = json.loads(request.body)
            from_account_id = data['from_account_id']
            to_account_id = data['to_account_id']
            amount = data['amount']
            if not isinstance(from_account_id, int):
                return JsonResponse({'error': 'Bad request, from_account_id must be an integer'}, status=400)
            if not isinstance(to_account_id, int):
                return JsonResponse({'error': 'Bad request, to_account_id must be an integer'}, status=400)
            if not isinstance(amount, int):
                return JsonResponse({'error': 'Bad request, amount must be a number'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Bad request, from_account_id, to_account_id, and amount are required'},
                                status=400)
        try:
            from_account_id_obj = Account.objects.get(account_id=from_account_id)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Source account not found'}, status=404)
        try:
            to_account_id_obj = Account.objects.get(account_id=to_account_id)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Destination account not found'}, status=404)

        if from_account_id_obj.initial_balance >= amount:
            from_account_id_obj.initial_balance -= amount
            from_account_id_obj.save()
            to_account_id_obj.initial_balance += amount
            to_account_id_obj.save()
            response_data = {
                'from_account_id_current_balance': from_account_id_obj.initial_balance,
                'to_account_id_balance': to_account_id_obj.initial_balance,
            }
            return JsonResponse(response_data, status=200)
        return JsonResponse(
            {'not enough': f'not enough money in account current balance is {from_account_id_obj.initial_balance}'},
            status=400)

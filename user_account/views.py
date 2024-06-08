import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from user_account.models import Account, UserAccount


@csrf_exempt
@permission_classes([AllowAny])
@require_POST
def user_profile(request):
    try:
        data = json.loads(request.body)
        username = data['username']
        first_name = data['first_name']
        last_name = data['last_name']
        password = data['password']
        repeat_password = data['repeat_password']

        if not isinstance(username, str):
            return JsonResponse({'error': 'Bad request, username must be a string'}, status=400)
        if not isinstance(first_name, str):
            return JsonResponse({'error': 'Bad request, first_name must be a string'}, status=400)
        if not isinstance(last_name, str):
            return JsonResponse({'error': 'Bad request, last_name must be a string'}, status=400)
    except KeyError:
        return JsonResponse({'error': 'Bad request, account_name and initial_balance are required'}, status=400)
    if password == repeat_password:
        user_profile_bank = UserAccount.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        return JsonResponse({'profile_created': 'created success'}, status=201)

    return JsonResponse({'error': 'Bad request, passwords must be match please check and try again'}, status=400)


@csrf_exempt
@permission_classes([IsAuthenticated])
@require_POST
def account(request):
    try:
        data = json.loads(request.body)
        account_name = data['account_name']
        initial_balance = data['initial_balance']
        user_id = data["user_id"]
        if not isinstance(account_name, str):
            return JsonResponse({'error': 'Bad request, account_name must be a string'}, status=400)
        if not isinstance(initial_balance, (int, float)):
            return JsonResponse({'error': 'Bad request, initial_balance must be a number'}, status=400)
    except KeyError:
        return JsonResponse({'error': 'Bad request, account_name and initial_balance are required'}, status=400)
    user_profile = UserAccount.objects.get(id=user_id)
    account_obj = Account.objects.create(
        name=account_name,
        user=user_profile,
        initial_balance=initial_balance
    )
    return JsonResponse({'account created success': f' account name: {account_name} | initial_balance: {initial_balance}'}, status=201)


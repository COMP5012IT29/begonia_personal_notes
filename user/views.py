from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from django.http import JsonResponse
from django.core import serializers
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.db.utils import IntegrityError
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from user.models import User
from user.utils import get_tokens_for_user


# Register
@csrf_exempt
@require_http_methods(['POST'])
def add_user(request):
    response = {}
    js = json.loads(request.body)
    # 查找
    res_email = User.objects.filter(email=js['email']).count()
    res_phone = User.objects.filter(phone=js['phone']).count()
    if res_email != 0:
        response['msg'] = 'Email number has been registered'
        response['status'] = 321

    elif res_phone != 0:
        response['msg'] = 'Mobile number has been registered'
        response['status'] = 322

    elif res_email == 0 and res_phone == 0:
        user = User(username=js['username'],
                    password=make_password(js["password"]),
                    email=js['email'], phone=js['phone'])
        user.save()
        response['msg'] = 'success'
        response['status'] = 0
    return JsonResponse(response)


# Login
@require_http_methods(['POST'])
@csrf_exempt
def login_user(request):
    response = {}
    js = json.loads(request.body)

    email = js['email']
    # username = js['username']
    try:
        res_email = User.objects.filter(email=js['email']).get()
        username = res_email.username
        password = js['password']
        user = authenticate(username=username, password=password)

        response['token'] = get_tokens_for_user(user)
        response["username"] = username
        response['msg'] = 'Success'
        response['status'] = 0
    except User.DoesNotExist:
        response['msg'] = 'User not exist or wrong password'
        response['status'] = 31

    return JsonResponse(response)


@csrf_exempt
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_user(request):
    response = {}
    js = json.loads(request.body)
    try:
        user = User.objects.filter(username=js['username']).get()

        if 'email' in js:
            if User.objects.filter(email=js['email']).exclude(username=user.username).exists():
                response['msg'] = 'email already exists'
                response['status'] = 321
                return JsonResponse(response)
            user.email = js['email']

        if 'phone' in js:
            if User.objects.filter(phone=js['phone']).exclude(username=user.username).exists():
                response['msg'] = 'phone already exists'
                response['status'] = 322
                return JsonResponse(response)
            user.phone = js['phone']

        if 'new_username' in js:
            if User.objects.filter(username=js['new_username']).exclude(pk=user.pk).exists():
                response['msg'] = 'username already exists'
                response['status'] = 323
                return JsonResponse(response)
            user.username = js['new_username']

        user.save()

    except User.DoesNotExist:
        response['msg'] = 'user not found'
        response['status'] = 31
        return JsonResponse(response)

    response['msg'] = 'success'
    response['status'] = 0

    return JsonResponse(response)


@csrf_exempt
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_user(request):
    response = {}
    js = json.loads(request.body)
    # 查找用户
    try:
        # 查找用户
        user = User.objects.filter(username=js['username']).get()
        # user = get_object_or_404(User, username=username)
        # 删除
        user.delete()
        response['msg'] = 'success'
        response['status'] = 0
    except User.DoesNotExist:
        response['msg'] = 'User not found'
        response['status'] = 31
    except Exception as e:
        response['msg'] = str(e)
        response['status'] = 4

    return JsonResponse(response)

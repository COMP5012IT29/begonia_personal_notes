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
from user.models import User
from user.utils import get_tokens_for_user


# Register
@csrf_exempt
@require_http_methods(['POST'])
def add_user(request):
    response = {}
    js = json.loads(request.body)
    res_email = User.objects.filter(email = js['email']).count()
    res_phone = User.objects.filter(phone = js['phone']).count()
    if res_email != 0:
        response['msg'] = 'Email number has been registered'
        response['status'] = 321

    elif res_phone != 0:
        response['msg'] = 'Mobile number has been registered'
        response['status'] = 322

    elif res_email == 0 and res_phone == 0:
        user = User(username=js['username'],
                    password = make_password(js["password"]),
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
    res_email = User.objects.filter(email=js['email']).get()
    username = res_email.username
    password = js['password']
    user = authenticate(username=username, password=password)
    if user is None:
        response['msg'] = 'User not exist or wrong password'
        response['status'] = 31
    else:
        response['token'] = get_tokens_for_user(user)
        response["username"] = username
        response['msg'] = 'Success'
        response['status'] = 0

    return JsonResponse(response)


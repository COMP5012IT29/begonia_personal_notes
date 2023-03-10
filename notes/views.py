import json
import os
from datetime import datetime, date
from json import JSONDecodeError

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from notes.models import Note
from user.models import User
from notes.utils import *

# Create your views here.
@require_http_methods(['POST'])
@csrf_exempt
def add_note(request):
    response = {}
    js = json.loads(request.body)

    user_obj = User.objects.get(username=js['username'])
    user_id = user_obj.id
    title = js['title']
    password = js['password']
    content = js['content']
    hint = js['hint']
    tag = js['tag']

    salt = generate_random_salt(32)
    iv = os.urandom(16)
    enc_content = encrypt_content(password,salt,iv,content)
    note = Note(
            note_user_id=user_id,
            note_title=title,note_content=enc_content,
            note_salt=salt,note_iv=iv,
            note_date=datetime.now().date(),
            note_pwd_hint=hint,
            note_tag=tag)
    note.save()

    response['msg'] = 'success'
    response['status'] = 0
    return JsonResponse(response)


@require_http_methods(['POST'])
@csrf_exempt
def view_note(request):
    response = {}
    js = json.loads(request.body)
    note_obj = Note.objects.get(note_id=js['note_id'])
    salt = note_obj.note_salt
    iv = note_obj.note_iv
    password = js['password']

    response['msg'] = 'success'
    response['status'] = 0
    try:
        dec_content = decrypt_content(password,salt,iv,note_obj.note_content)
        response['data'] = {
            'title': note_obj.note_title,
            'content': dec_content.decode(),
            'tag':note_obj.note_tag
        }
    except Exception as e:
        if isinstance(e,UnicodeDecodeError):
            response['msg'] = 'Wrong password'
            response['status'] = 31

    return JsonResponse(response)


@require_http_methods(['GET'])
@csrf_exempt
def view_hint(request):
    response = {}
    note_id = request.GET.get('note_id')
    note_obj = Note.objects.get(note_id=note_id)

    response['msg'] = 'Success'
    response['status'] = 0
    response['data'] = note_obj.note_pwd_hint
    return JsonResponse(response)


@require_http_methods(['POST'])
@csrf_exempt
def edit_note(request):
    response = {}
    js = json.loads(request.body)
    note_obj = Note.objects.get(note_id=js['note_id'])
    salt = note_obj.note_salt
    iv = note_obj.note_iv

    title = js['title']
    password = js['password'] # ??????????????????????????????????????????
    content = js['content']
    enc_content = encrypt_content(password,salt,iv,content)

    note_obj.note_title = title
    note_obj.note_content = enc_content
    note_obj.save()

    response['msg'] = 'success'
    response['status'] = 0
    return JsonResponse(response)

@require_http_methods(['GET'])
@csrf_exempt
def show_notes(request):
    response = {}
    username = request.GET.get('username')
    user_obj = User.objects.filter(username=username)
    user_id = user_obj.get().id

    type = int(request.GET.get('type'))
    # type = 1: ????????????????????? (??????star??????star,??????????????????)
    # type = 2: ???????????????
    # type = 3: ???????????????
    res_note_list = []
    if type == 1:
        res_note_list = Note.objects.filter(note_user_id=user_id, note_deleted=False)
    elif type == 2:
        res_note_list = Note.objects.filter(note_user_id=user_id, note_deleted=False, note_stared=True)
    elif type == 3:
        res_note_list = Note.objects.filter(note_user_id=user_id, note_deleted=True)

    res = []
    for note in res_note_list:
        res.append({
            'id':note.note_id,
            'title':note.note_title,
            'date':note.note_date,
            'tag': note.note_tag
        })
    response['status'] = 0
    response['msg'] = 'success'
    response['data'] = res

    return JsonResponse(response)

@require_http_methods(['POST'])
@csrf_exempt
def search_note(request):
    response = {}
    js = json.loads(request.body)
    keyword = js['keyword']

    type = js['type']
    # type = 1: ???????????????
    # type = 2: ???????????????
    # type = 3: ???????????????
    # ??????: ?????????????????? keyword???????????? YYYY-MM-DD,YYYY-MM-DD
    # ?????????date?????????????????????????????????????????????????????????1970-01-01
    # ?????????date?????????????????????????????????????????????????????????2038-01-19
    res_note_list = []
    if type == 1:
        res_note_list = Note.objects.filter(note_title__icontains=keyword)
    elif type == 2:
        res_note_list = Note.objects.filter(note_tag__icontains=keyword)
    elif type == 3:
        start_date,end_date = keyword.split(',')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        query = Q(note_date__gte=start_date) & Q(note_date__lte=end_date)
        res_note_list = Note.objects.filter(query)
    else:
        response['status'] = 301
        response['msg'] = 'type not support'

    if res_note_list.count != 0:
        response['status'] = 0
        response['msg'] = 'Success'

        res = []
        for note in res_note_list:
            res.append({
                'id': note.note_id,
                'title': note.note_title,
                'date': note.note_date,
                'tag': note.note_tag
            })

        response['data'] = res
    else:
        response['status'] = 302
        response['msg'] = 'no result'
    return JsonResponse(response)


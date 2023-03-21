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
            'tag':note_obj.note_tag,
            'date':note_obj.note_date,
            'stared':note_obj.note_stared
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
    password = js['password'] # 这里如果密码错误会覆盖原密码
    content = js['content']
    hint = js['hint']
    tag = js['tag']
    enc_content = encrypt_content(password,salt,iv,content)

    note_obj.note_title = title
    note_obj.note_content = enc_content
    note_obj.note_pwd_hint = hint
    note_obj.note_tag = tag
    note_obj.save()

    response['msg'] = 'success'
    response['status'] = 0
    return JsonResponse(response)


@require_http_methods(['POST'])
@csrf_exempt
def star_note(request):
    response = {}
    js = json.loads(request.body)
    note_obj = Note.objects.get(note_id=js['note_id'])
    note_obj.note_stared = not note_obj.note_stared
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
    # type = 1: 正常状态的文章 (包含star和非star,不包含删除的)
    # type = 2: 收藏的文章
    # type = 3: 删除的文章
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
    # type = 1: 按标题搜索
    # type = 2: 按标签搜索
    # type = 3: 按日期搜索
    # 注意: 按日期搜索时 keyword的格式为 YYYY-MM-DD,YYYY-MM-DD
    # 第一个date是想要找到的最早的时间，如果无请填写为1970-01-01
    # 第二个date是想要找到的最晚的时间，如果无请填写为2038-01-19
    res_note_list = []
    if type == 1:
        res_note_list = Note.objects.filter(note_title__icontains=keyword, note_deleted=False)
    elif type == 2:
        res_note_list = Note.objects.filter(note_tag__icontains=keyword, note_deleted=False)
    elif type == 3:
        start_date,end_date = keyword.split(',')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        query = Q(note_date__gte=start_date) & Q(note_date__lte=end_date, note_deleted=False)
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


@require_http_methods(['POST'])
@csrf_exempt
def recycle_note(request):
    response = {}
    js = json.loads(request.body)

    note_obj = Note.objects.get(note_id=js['note_id'])
    note_obj.note_deleted = True
    note_obj.save()
    response['status'] = 0
    response['msg'] = 'success'
    return JsonResponse(response)

@require_http_methods(['POST'])
@csrf_exempt
def recycle_note(request):
    response = {}
    js = json.loads(request.body)

    note_obj = Note.objects.get(note_id=js['note_id'])
    note_obj.note_deleted = True
    note_obj.save()
    response['status'] = 0
    response['msg'] = 'success'
    return JsonResponse(response)


@csrf_exempt
@require_http_methods('DELETE')
def delete_note(request):
    response = {}
    js = json.loads(request.body)
    try:
        # 查找用户
        note = Note.objects.filter(note_id=js['note_id']).get()
        note.delete()
        response['msg'] = 'success'
        response['status'] = 0
    except Note.DoesNotExist:
        response['msg'] = 'User not found'
        response['status'] = 31
    except Exception as e:
        response['msg'] = str(e)
        response['status'] = 4

    return JsonResponse(response)

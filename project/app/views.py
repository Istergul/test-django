import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from app import models as app_models
from app import forms as app_forms


def index(request):
    return render(request, 'index.html')


def get_users(request):
    users = app_models.Users.objects.all().order_by('id')
    context = {'result': [app_models.user_to_json(u) for u in users]}
    return HttpResponse(json.dumps(context), mimetype='application/json')


def add_user(request):
    data = json.loads(request.body)
    form = app_forms.UserForm(data)
    if form.is_valid():
        user = form.save()
        context = {'result': app_models.user_to_json(user)}
        return HttpResponse(json.dumps(context), mimetype='application/json')
    else:
        return HttpResponseBadRequest(json.dumps(form.errors))


def update_user(request):
    data = json.loads(request.body)
    try:
        user = app_models.Users.objects.get(id=data['id'])
    except app_models.Users.DoesNotExist:
        return HttpResponseBadRequest('User does not exist')
    form = app_forms.UserForm(data, instance=user)
    if form.is_valid():
        user = form.save()
        context = {'result': app_models.user_to_json(user)}
        return HttpResponse(json.dumps(context), mimetype='application/json')
    else:
        return HttpResponseBadRequest(json.dumps(form.errors))


def get_rooms(request):
    rooms = app_models.Rooms.objects.all().order_by('id')
    context = {'result': [app_models.room_to_json(u) for u in rooms]}
    return HttpResponse(json.dumps(context), mimetype='application/json')


def add_room(request):
    data = json.loads(request.body)
    form = app_forms.RoomForm(data)
    if form.is_valid():
        room = form.save()
        context = {'result': app_models.room_to_json(room)}
        return HttpResponse(json.dumps(context), mimetype='application/json')
    else:
        return HttpResponseBadRequest(json.dumps(form.errors))


def update_room(request):
    data = json.loads(request.body)
    try:
        room = app_models.Rooms.objects.get(id=data['id'])
    except app_models.Rooms.DoesNotExist:
        return HttpResponseBadRequest('Room does not exist')
    form = app_forms.RoomForm(data, instance=room)
    if form.is_valid():
        room = form.save()
        context = {'result': app_models.room_to_json(room)}
        return HttpResponse(json.dumps(context), mimetype='application/json')
    else:
        return HttpResponseBadRequest(json.dumps(form.errors))
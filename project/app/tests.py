#coding=utf-8
import datetime
import json

from django.test import Client
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.db import IntegrityError

from app import models as app_models


class TestAppUsers(TestCase):

    def setUp(self):
        self.user_name = 'test name'
        self.user_paycheck = 100500
        self.user_date_joined = datetime.date.today()

    def create_user(self, name=None, paycheck=None, date_joined=None):
        app_models.Users.objects.create(name=name, paycheck=paycheck, date_joined=date_joined)

    def test_create_user_success(self):
        self.create_user(self.user_name, self.user_paycheck, self.user_date_joined)
        users = app_models.Users.objects.filter(name=self.user_name)
        self.assertEqual(len(users), 1)
        user = users[0]
        self.assertEqual(user.name, self.user_name)
        self.assertEqual(user.paycheck, self.user_paycheck)
        self.assertEqual(user.date_joined, self.user_date_joined)

    def test_create_user_failed_paycheck(self):
        with self.assertRaises(ValueError):
            self.create_user(self.user_name, 'test', self.user_date_joined)

    def test_create_user_failed_name(self):
        with self.assertRaises(IntegrityError):
            self.create_user(None, self.user_paycheck, self.user_date_joined)

    def test_create_user_failed_date_joined(self):
        with self.assertRaises(TypeError):
            self.create_user(self.user_name, self.user_paycheck, 100500)

    def test_update_user(self):
        name = 'new name'
        paycheck = 777777
        date_joined = datetime.date.today()
        self.create_user(self.user_name, self.user_paycheck, self.user_date_joined)
        users = app_models.Users.objects.filter(name=self.user_name)
        self.assertEqual(len(users), 1)
        user = users[0]
        user.name = name
        user.paycheck = paycheck
        user.date_joined = date_joined
        user.save()
        users = app_models.Users.objects.filter(name=name)
        user = users[0]
        self.assertEqual(user.name, name)
        self.assertEqual(user.paycheck, paycheck)
        self.assertEqual(user.date_joined, date_joined)

    def test_delete_user(self):
        self.create_user(self.user_name, self.user_paycheck, self.user_date_joined)
        users = app_models.Users.objects.filter(name=self.user_name)
        self.assertEqual(len(users), 1)
        user = users[0]
        user.delete()
        users = app_models.Users.objects.filter(name=self.user_name)
        self.assertEqual(len(users), 0)


class TestAppRooms(TestCase):

    def setUp(self):
        self.room_department = 'department'
        self.room_spots = 10

    def create_room(self, department=None, spots=None):
        app_models.Rooms.objects.create(department=department, spots=spots)

    def test_create_room_success(self):
        self.create_room(self.room_department, self.room_spots)
        rooms = app_models.Rooms.objects.all()
        self.assertEqual(len(rooms), 1)
        room = rooms[0]
        self.assertEqual(room.department, self.room_department)
        self.assertEqual(room.spots, self.room_spots)

    def test_create_room_failed_department(self):
        with self.assertRaises(IntegrityError):
            self.create_room(None, self.room_spots)

    def test_create_room_failed_spots(self):
        with self.assertRaises(ValueError):
            self.create_room(self.room_department, 'test')

    def test_update_room(self):
        department = 'new department'
        spots = 777777
        self.create_room(self.room_department, self.room_spots)
        rooms = app_models.Rooms.objects.all()
        self.assertEqual(len(rooms), 1)
        room = rooms[0]
        room.department = department
        room.spots = spots
        room.save()
        rooms = app_models.Rooms.objects.all()
        room = rooms[0]
        self.assertEqual(room.department, department)
        self.assertEqual(room.spots, spots)

    def test_delete_room(self):
        self.create_room(self.room_department, self.room_spots)
        rooms = app_models.Rooms.objects.all()
        self.assertEqual(len(rooms), 1)
        room = rooms[0]
        room.delete()
        rooms = app_models.Rooms.objects.all()
        self.assertEqual(len(rooms), 0)


class TestViews(TestCase):

    def setUp(self):
        self.c = Client()

    def compare_dicts(self, dict1, dict2):
        for k, v in dict1.iteritems():
            if not dict2.has_key(k) or dict2[k] != dict1[k]:
                return False
        return True

    def add_user(self, data):
        return self.c.post(
            reverse('add_user'),
            json.dumps(data),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

    def add_room(self, data):
        return self.c.post(
            reverse('add_room'),
            json.dumps(data),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

    def test_add_user(self):
        data_user = {'name': "test", "paycheck": 100, "date_joined": "2014.10.10"}
        r = self.add_user(data_user)
        data = json.loads(r.content)
        self.assertTrue(self.compare_dicts(data_user, data['result']))

    def test_get_users(self):
        data_user1 = {'name': "test1", "paycheck": 100, "date_joined": "2014.10.10"}
        data_user2 = {'name': "test2", "paycheck": 100, "date_joined": "2011.11.06"}
        data_user3 = {'name': "test3", "paycheck": 8888, "date_joined": "2011.12.06"}
        self.add_user(data_user1)
        self.add_user(data_user2)
        self.add_user(data_user3)
        r = self.c.get(reverse('get_users'), {}, content_type="application/json", HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(r.content)
        self.assertEqual(len(data['result']), 3)
        user1 = data['result'][0]
        user2 = data['result'][1]
        user3 = data['result'][2]
        self.assertTrue(self.compare_dicts(data_user1, user1))
        self.assertTrue(self.compare_dicts(data_user2, user2))
        self.assertTrue(self.compare_dicts(data_user3, user3))

    def test_update_user(self):
        data_user = {'name': "test", "paycheck": 100, "date_joined": "2014.10.10"}
        r = self.add_user(data_user)
        user = json.loads(r.content)['result']
        new_data = {'id': user['id'], 'name': 'new name', 'paycheck': 999, 'date_joined': '2010.10.10'}
        r = self.c.post(
            reverse('update_user'),
            json.dumps(new_data),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        updated_user = json.loads(r.content)['result']
        self.assertTrue(self.compare_dicts(new_data, updated_user))

    def test_add_room(self):
        data_room = {'department': "test", "spots": 3}
        r = self.add_room(data_room)
        data = json.loads(r.content)
        self.assertTrue(self.compare_dicts(data_room, data['result']))

    def test_get_rooms(self):
        data_room1 = {'department': "test1", "spots": 3}
        data_room2 = {'department': "test2", "spots": 4}
        data_room3 = {'department': "test3", "spots": 6}
        self.add_room(data_room1)
        self.add_room(data_room2)
        self.add_room(data_room3)
        r = self.c.get(reverse('get_rooms'), {}, content_type="application/json", HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(r.content)
        self.assertEqual(len(data['result']), 3)
        room1 = data['result'][0]
        room2 = data['result'][1]
        room3 = data['result'][2]
        self.assertTrue(self.compare_dicts(data_room1, room1))
        self.assertTrue(self.compare_dicts(data_room2, room2))
        self.assertTrue(self.compare_dicts(data_room3, room3))

    def test_update_room(self):
        data_room = {'department': "test", "spots": 3}
        r = self.add_room(data_room)
        room = json.loads(r.content)['result']
        new_data = {'id': room['id'], 'department': 'new test', 'spots': 999}
        r = self.c.post(
            reverse('update_room'),
            json.dumps(new_data),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        updated_room = json.loads(r.content)['result']
        self.assertTrue(self.compare_dicts(new_data, updated_room))
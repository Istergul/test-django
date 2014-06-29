from django import forms

from app import models as app_models


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['date_joined'].input_formats = ('%d.%m.%Y', '%Y.%m.%d')

    class Meta(object):
        model = app_models.Users
        fields = ["name", "paycheck", "date_joined"]


class RoomForm(forms.ModelForm):
    class Meta(object):
        model = app_models.Rooms

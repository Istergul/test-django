#coding=utf-8
import os
import yaml

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


lcs = locals()


def create_meta(title):
    attrs = {
        'verbose_name': title,
        'verbose_name_plural': title,
    }
    return type('Meta', (object, ), attrs)


def get_field(ftitle, ftype):
    field = None
    if ftype == 'char':
        field = models.CharField(_(ftitle), max_length=255, blank=True)
    elif ftype == 'int':
        field = models.IntegerField(_(ftitle), null=True, blank=True)
    elif ftype == 'date':
        field = models.DateField(_(ftitle), null=True, blank=True)
    return field


with open(settings.MODEL_DECLAR_FILE) as f:
    data = yaml.load(f.read())
    # тут по хорошему нужно сделать валидацию данных, прочитанных из файла

    for model, params in data.iteritems():
        model_name = model.title()
        attrs = {
            '__module__': __name__,
            '__doc__': params['title'],
            'objects': models.Manager(),
            'Meta': create_meta(model_name),
        }
        for field_data in params['fields']:
            attrs[field_data['id']] = get_field(field_data['title'], field_data['type'])
        lcs[model_name] = type(model_name, (models.Model, ), attrs)


def user_to_json(obj):
    return {
        'id': obj.id,
        'name': obj.name,
        'paycheck': obj.paycheck,
        'date_joined': obj.date_joined.strftime("%Y.%m.%d") if obj.date_joined else None,
    }


def room_to_json(obj):
    return {
        'id': obj.id,
        'department': obj.department,
        'spots': obj.spots,
    }
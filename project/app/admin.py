#coding=utf-8
import yaml

from django.contrib import admin
from django.conf import settings

from app import models


def create_admin_class(model_name):
    admin_class_name = "{0}Admin".format(model_name)
    return type(admin_class_name, (admin.ModelAdmin, ), {})


def register_models():
    with open(settings.MODEL_DECLAR_FILE) as f:
        data = yaml.load(f.read())
        for model in data.iterkeys():
            model_name = model.title()
            if hasattr(models, model_name):
                model = getattr(models, model_name)
                admin_class = create_admin_class(model_name)
                admin.site.register(model, admin_class)


register_models()

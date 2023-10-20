from django.contrib import admin
from django.apps import apps
from django.db import models


class CustomModelAdmin(admin.ModelAdmin):
    def get_model_fields(self, model):
        return [field.name for field in model._meta.get_fields() if isinstance(field, models.Field)]

    def get_list_display(self, request):
        model_fields = self.get_model_fields(self.model)
        return model_fields[:7]

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = self.get_list_display(None)
        self.search_fields = ["id", ]


def autoregister_admin():
    app_models = apps.get_app_config('file').get_models()

    for model in app_models:
        admin_class_name = model.__name__ + 'Admin'
        admin_class_attrs = {}
        admin_class = type(
            admin_class_name, (CustomModelAdmin,), admin_class_attrs)
        admin.site.register(model, admin_class)


autoregister_admin()

# coding: utf8

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

import models


class SSUserAdmin(admin.StackedInline):
    model = models.SSUser
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (SSUserAdmin,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(models.PayTrans)
class PayTransAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SalesOrder)
class SalesOrder(admin.ModelAdmin):
    pass

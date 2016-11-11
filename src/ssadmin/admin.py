# coding: utf8
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

import models


class SSUserAdmin(admin.StackedInline):
    model = models.SSUser
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (SSUserAdmin,)

    # change_list_template = 'ssadmin/extras/change_list.html'

    def get_urls(self):
        return [
                   url(r'^provision_vpn$',
                       self.admin_site.admin_view(self.provision_vpn),
                       name='provision_vpn'
                       ),

               ] + super(UserAdmin, self).get_urls()

    def provision_vpn(self, request, queryset):
        for user in queryset:
            models.SSUser.provision(user, '111', '1000000000')

    provision_vpn.short_description = u'开通vpn'

    actions = [provision_vpn]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(models.PayTrans)
class PayTransAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SalesOrder)
class SalesOrder(admin.ModelAdmin):
    pass

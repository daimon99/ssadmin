# coding: utf8

from django.db import models
from django.contrib.auth.models import User


class SSUser(models.Model):
    user = models.OneToOneField(User, related_name='ss_user')
    port = models.IntegerField()
    password = models.CharField(max_length=20)
    flow_limit = models.IntegerField(default=0)
    flow_used = models.IntegerField(default=0)
    flow_remaining = models.IntegerField(default=0)
    flow_last_update_time = models.DateTimeField(auto_now=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    up_user = models.ForeignKey(User, related_name='down_user')

    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)


class SalesOrder(models.Model):
    user = models.ForeignKey(User)
    status = models.CharField(default=u'待支付',
                              choices=((u'待支付', u'待支付'), (u'支付成功', u'支付成功'), (u'支付失败', u'支付失败'), (u'已用完', u'已用完')),
                              max_length=20)
    buy_on = models.DateTimeField(blank=True, null=True)
    pay_on = models.DateTimeField(blank=True, null=True)
    qty = models.IntegerField(default=1, help_text=u'购买流量大小。以G为单位')
    amount = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=10)
    remaining = models.IntegerField(blank=True, null=True)


class PayTrans(models.Model):
    pay_method = models.CharField(default=u'微信', choices=((u'微信', u'微信'),), max_length=20)
    pay_id = models.CharField(max_length=200, help_text=u'支付流水')
    pay_amount = models.DecimalField(default=0, decimal_places=4, max_digits=10)
    status = models.CharField(max_length=20, default=u'支付中',
                              choices=((u'支付中', u'支付中'), (u'支付成功', u'支付成功'), (u'支付失败', u'支付失败')))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    pay_for = models.CharField(max_length=100, blank=True, null=True, help_text=u'支付对象的id')
    pay_memo = models.CharField(max_length=500, blank=True, null=True, help_text=u'支付说明',
                                choices=((u'订单', u'订单'), (u'充值', u'充值')))

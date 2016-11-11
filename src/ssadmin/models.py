# coding: utf8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from ssadmin.exceptions import SSError


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

    @classmethod
    def provision(cls, user, password, flow_add, up_user=None):
        # todo 这里有bug，怎么能够锁住记录，确保获取到正确的最大port是个问题。目前的实现在大并发中会有问题
        from .services import change
        try:
            ssuser = cls.objects.get(user=user)
            # 用户非首次开通
            ssuser.password = password
            ssuser.flow_limit += flow_add
            ssuser.flow_remaining += flow_add
            change(ssuser.port, password, ssuser.flow_limit)
            ssuser.save()
        except cls.DoesNotExist:
            # 用户首次开通，创建记录
            current_port = cls.objects.annotate(max_port=models.Func(models.F('port'), function='max')).get()
            ssuser = SSUser()
            ssuser.user = user
            ssuser.port = current_port if current_port else 10000
            ssuser.flow_limit = flow_add
            ssuser.used = 0
            ssuser.flow_remaining = flow_add
            ssuser.up_user = up_user
            change(ssuser.port, password, ssuser.flow_limit)
            ssuser.save()


class flow_use_history(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    port = models.IntegerField()
    limit = models.BigIntegerField()
    remaining = models.BigIntegerField()
    used = models.BigIntegerField()

    @classmethod
    def update_using_info(cls, port, limit, remaining, used):
        from .services import show_port
        using_info_dict = show_port(
            port)  # re.compile('^(?P<port>\d*)\s*(?P<limit>\d*)\(\S*\)\s*(?P<used>\d*)\(\S*\)\s*(?P<remaining>\d*)\(\S*\)')
        if not using_info_dict.get('port'):
            raise SSError('port=%s的用户查询流量失败。注意检查该用户是否非法或者开通有问题。' % port)
        cls.objects.create(port=port,
                           limit=using_info_dict.get('limit'),
                           remaining=using_info_dict.get('remaining'),
                           used=using_info_dict.get('used'))


class flow_add_history(models.Model):
    ssuser = models.ForeignKey(SSUser)
    port = models.IntegerField()


class flow_update_history(models.Model):
    pass


class password_change_history(models.Model):
    pass


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

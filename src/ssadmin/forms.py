# coding:utf-8
from django import forms


class ProvisionForm(forms.Form):
    account = forms.CharField(label=u'帐号')
    vpn_password = forms.PasswordInput()

from django import forms
from django.core.exceptions import ValidationError
import re
from blog import models

class RegForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super(RegForm, self).__init__(*args, **kwargs)
        self.request = request

    username = forms.CharField(min_length=4,max_length=16,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(min_length=4,max_length=16,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    confirm_pwd = forms.CharField(min_length=4,max_length=16,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm_pwd'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    nickname = forms.CharField(max_length=16,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nickname'}))
    verification_code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Verification_code'}))

    def clean_verification_codxe(self):
        if self.request.session.get('verification_code').upper() == self.cleaned_data['verification_code'].upper():
            return self.cleaned_data['verification_code']
        else:
            raise ValidationError('验证码错误!')

    def clean_username(self):
        res = re.search(r'^[a-zA-Z0-9_-]{4,16}$', self.cleaned_data['username'])
        if res:
            #用户名重复验证
            user = models.UserInfo.objects.filter(username=self.cleaned_data['username']).first()
            if not user:
                return self.cleaned_data['username']
            else:
                raise ValidationError('用户名已存在!')
        else:
            raise ValidationError('用户名必须是（字母，数字，下划线，减号）组成的4到16位!')


    def clean(self):
        if self.cleaned_data.get('password') == self.cleaned_data.get('confirm_pwd'):
            return self.cleaned_data
        else:
            raise ValidationError('密码不一致!')
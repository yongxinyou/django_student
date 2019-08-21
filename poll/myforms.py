"""__author__= 雍新有"""
import re

from django import forms
from django.core.exceptions import ValidationError

from poll.utils import to_md5_hex


# def check_username(username):
#     """验证用户名是否有效"""
#     pattern = re.compile(r'\w{4,20}')
#     if not pattern.fullmatch(username):
#         raise ValidationError('用户名由字母、数字、下划线构成并且长度为4-20个字符')
#     return username
#
#
# def check_password(password):
#     if len(password) < 6:
#         raise ValidationError('密码长度不应该小于6个字符')
#     return to_md5_hex(password)


class LoginForm(forms.Form):
    """验证登录表单"""
    username = forms.CharField(min_length=4, max_length=10)
    password = forms.CharField(min_length=6, max_length=20)
    code = forms.CharField(min_length=4, max_length=4)
    #
    # def check_username(self):
    #         return check_username(self.check_data['username'])
    #
    #     def check_password(self):
    #         return check_password(self.check_data['password'])

    def clean_username(self):
        """自动调用，验证username"""
        username = self.cleaned_data['username']
        pattern = re.compile(r'\w{4,20}')
        if not pattern.fullmatch(username):
            raise ValidationError('用户名由字母、数字、下划线构成并且长度为4-20个字符')
        return username

    def clean_password(self):
        """从上到下验证，所有先把密码转成md5，在验证确认密码"""
        password = self.cleaned_data['password']
        return to_md5_hex(password)


class RegisterForm(forms.Form):
    """注册表单验证"""
    username = forms.CharField(min_length=4, max_length=10)
    password = forms.CharField(min_length=6, max_length=20)
    repassword = forms.CharField(min_length=4, max_length=20)

    def clean_username(self):
        """自动调用，验证username"""
        username = self.cleaned_data['username']
        pattern = re.compile(r'\w{4,20}')
        if not pattern.fullmatch(username):
            raise ValidationError('用户名由字母、数字、下划线构成并且长度为4-20个字符')
        return username

    def clean_password(self):
        """从上到下验证，所有先把密码转成md5，在验证确认密码"""
        password = self.cleaned_data['password']
        return to_md5_hex(password)

    # def check_username(self):
    #     return check_username(self.check_data['username'])
    #
    # def check_password(self):
    #     return check_password(self.check_data['password'])

    def clean_repassword(self):
        """验证两次密码是否相同"""
        password = self.cleaned_data['password']
        repassword = self.cleaned_data['repassword']
        if password != to_md5_hex(repassword):
            raise ValidationError('密码和确认密码需要一致')
        return repassword


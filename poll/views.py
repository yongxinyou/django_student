import json

from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from poll.captcha import Captcha
from poll.models import Subject, Teacher, User
from poll.myforms import RegisterForm
from poll.utils import random_captcha_text


def get_captcha(request):
    image_data = Captcha.instance().generate(random_captcha_text())
    return HttpResponse(image_data, content_type='image/png')


def show_subject(request):
    """查看所有学科"""
    subjects = Subject.objects.all()
    return render(request, 'subject.html', {'subjects': subjects})


def login(request):
    """查看登录页面"""
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        pass


def register(request):
    """注册页面"""
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        try:
            # 验证表单填的是否正确.POST取到浏览器的请求。是字典，与表单对象一一检查
            form = RegisterForm(request.POST)
            if form.is_valid():
                # is_valid()验证后才有clean_data. 验证通过就存入数据库，使用数据持久化
                user = User()
                user.username = form.cleaned_data['username']
                user.password = form.cleaned_data['password']
                user.save()
                return render(request, 'login.html', {'hint': '注册成功，请登录'})
            else:
                hint = '请输入有效的注册信息'
        except IntegrityError:
            hint = '用户名已存在'
        return render(request, 'register.html', {'hint': hint})


def show_teachers(request):
    """查看指定学科的老师"""
    # 从GET请求中获取名字为sno的参数值(学科编号)
    try:
        sno = request.GET['sno']
        subject = Subject.objects.filter(no=sno).first()
        # 通过Teacher的对象管理器objects方法筛选数据
        teachers = Teacher.objects.filter(subject__no=sno)
        return render(request,
                      'teachers.html',
                      {'teachers': teachers,
                       'subject': subject})
    except KeyError:
        return redirect('/')


"""
HttpRequest - 封装了浏览器发给服务器的请求
HttpResponse - 封装了浏览器发给服务器的响应
HttpRequest中包含了下面这些信息
请求行 - GET /index.html HTTP /1.1
请求头 - HOST: www.baidu.com
        User-Agent: ...
        Accept-Language:
        \r\n
消息体 - 数据
request.method - 获取请求的方法
request.path  - 获取请求的资源路径
request.path_info - 获取带查询参数的资源路径（/teachers/?sno=）
request.META  - 获取请求头
request.GET / request.POST - 获取请求的参数
request.body / request.FILES - 获取上传的文件

content-type属性用来指定MIME类型 - 告诉浏览器服务器给的是什么类型的数据
MIME - Multipurpose Internet Mail Extension
页面 - text/html text/plain text/xml
图片 - image/png image/jpeg image/gif
声音 - audio/mp3 audio/wav
视频 - video/mpeg
其他 - application/pdf application/json application/msword
"""


def praise_or_criticize(request: HttpRequest):
    """老师好评"""
    try:
        # sno = int(request.GET['sno'])
        tno = int(request.GET['tno'])
        # Teacher.objects.get(no=tno)
        teacher = Teacher.objects.filter(no=tno).first()
        if request.path.startswith('/praise'):
            teacher.good_count += 1
            teacher.save()
        else:
            teacher.bad_count += 1
            teacher.save()
        data = {'code': 200, 'message': '操作成功'}
    except (KeyError, ValueError, Teacher.DoesNotExist):
        data = {'code': 404, 'message': '操作失败'}
    # return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    return JsonResponse(data)

import random

from django.http import HttpResponse
from django.shortcuts import render

sayings = [
    '真理惟一可靠的标准就是永远自相符合',
    '我需要三件东西：爱情友谊和图书',
    '时间是一切财富中最宝贵的财富',
    '这世界要是没有爱情，它在我们心中还会有什么意义！这就如一盏没有亮光的走马灯',
]

all_fruits = ['西瓜', '苹果', '香蕉', '榴莲', '梨子', '葡萄'
              '山竹', '橘子', '火龙果', '荔枝', '草莓', '蓝莓']


# 后端渲染 - 服务器把动态内容渲染到静态的HTML页面上在输出给浏览器
# return render(request, 'index.html', locals())
# 前端渲染 - 服务器只给JSON数据不负责渲染页面，
# 渲染页面的工作交给浏览器的JavaScript来完成(Vue+jQuery) -- 趋势
def home(request):
    context = {'sentence': sayings[random.randrange(len(sayings))],
               'fruits': random.sample(all_fruits, 3)}
    return render(request, 'home.html', context=context)
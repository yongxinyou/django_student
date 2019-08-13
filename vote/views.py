import random

from django.http import HttpResponse

sayings = [
    '真理惟一可靠的标准就是永远自相符合',
    '我需要三件东西：爱情友谊和图书',
    '时间是一切财富中最宝贵的财富',
    '这世界要是没有爱情，它在我们心中还会有什么意义！这就如一盏没有亮光的走马灯',
]

all_fruits = ['西瓜', '苹果', '香蕉', '榴莲', '梨子', '葡萄'
              '山竹', '橘子', '火龙果', '荔枝', '草莓', '蓝莓']


def home(request):
    sentence = sayings[random.randrange(len(sayings))]
    content = f'<h1>{sentence}</h1>'
    content += '<hr>'
    content += '<h2>今天向你推荐的水果</h2>'
    content += '<ul>'
    for fruit in random.sample(all_fruits, 3):
        content += f'<li>{fruit}</li>'
    content += '</ul>'
    return HttpResponse(content)
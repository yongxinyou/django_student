"""__author__= 雍新有"""
import random
import hashlib

ALL_CHARS = '0123456789qwertyuioplkjmnhbgvfcdxszaQAZWSXEDCRFVTGBNHYUJMKIOLP'


def random_captcha_text(length=4):
    """生成随机的验证码"""
    # 随机取出ALL_CHARS中的4字符，并用''链接起来
    # choices是有放回抽样 - 有重复，sample是无放回抽样 - 无重复
    return ''.join(random.choices(ALL_CHARS, k=length))


def to_md5_hex(content):
    return hashlib.md5(content.encode()).hexdigest()


if __name__ == '__main__':
    print(to_md5_hex('123456'))
    print(to_md5_hex('adsrdsd'))
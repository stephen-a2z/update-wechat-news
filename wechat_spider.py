# -*- coding: utf-8 -*-

## 基于搜狗微信
import re
import wechatsogou
from html.parser import HTMLParser
import logging

# loglogging.getLoggerClass()


class Parser(HTMLParser):

    def error(self, message):
        print('error', message)

    def __init__(self):
        HTMLParser.__init__(self)
        self.in_p = []
        self.result_content = []

    def handle_starttag(self, tag, attrs):
        if (tag == 'p'):
            self.in_p.append(tag)

    def handle_endtag(self, tag):
        if (tag == 'p'):
            self.in_p.pop()

    def handle_data(self, data):
        if self.in_p:

            if re.findall('\d+月\d+日', data):
                self.result_content.append(data)
            if any([num_str in data for num_str in ['1、', '2、', '3、', '4、', '5、', '6、', '7、', '8、','9、', '10、', '11、','12、']]):
                self.result_content.append(data)

    def get_result(self):
        return self.result_content

# 可配置参数
# 直连


def get_content_from_gzh():
    ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3, timeout=0.1, )

    # # 验证码输入错误的重试次数，默认为1
    # ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)
    #
    # # 所有requests库的参数都能在这用
    # # 如 配置代理，代理列表中至少需包含1个 HTTPS 协议的代理, 并确保代理可用
    # ws_api = wechatsogou.WechatSogouAPI(proxies={
    #     "http": "127.0.0.1:8888",
    #     "https": "127.0.0.1:8888",
    # })
    # 如 设置超时
    # ws_api = wechatsogou.WechatSogouAPI(timeout=0.1)
    res = ws_api.get_gzh_article_by_history(keyword="weiyunews")
    content_url = res['article'][0]['content_url']
    print(content_url)
    content = ws_api.get_article_content(url=content_url)
    parser = Parser()
    parser.feed(data=content['content_html'])
    # get news
    news = parser.get_result()
    print(news)
    return news


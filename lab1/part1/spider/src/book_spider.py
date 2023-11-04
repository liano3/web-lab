"""
@Description: 爬取豆瓣图书信息, 保存到 book.csv
"""

import requests
import re
from bs4 import BeautifulSoup
import csv
import time
import random
import threading

import get_fake_ip
import get_fake_ua

lock = threading.Lock()
error = []

print('正在获取 ip 和 ua...\n')
ua_list = get_fake_ua.get_ua_pool()
ip_list = get_fake_ip.get_ip_pool()
class BookSpider():
    # 基础 url
    base_url = 'https://book.douban.com/subject/{}/'
    # book 数据结构
    book = {
        'id': '',
        'name': '',
        'author': '',
        'date': '',
        'score': (),
        'intro': '',
        'author_intro': '',
        'recommend': []
    }
    # id_list
    id_list = []
    ip = ''

    # 初始化 id_list
    def __init__(self, book_id_list):
        self.id_list = book_id_list
    
    # 构造随机请求头
    def create_headers(self):
        ua = random.choice(ua_list)
        headers = {
            'User-Agent': ua
        }
        return headers
    
    def create_proxies(self):
        self.ip = random.choice(ip_list)
        proxies = {
            'http': 'http://' + self.ip
        }
        return proxies

    # 构造 url
    def create_url(self, book_id):
        url = self.base_url.format(book_id)
        return url

    # 获取网页源代码
    def get_html(self, url):
        headers = self.create_headers()
        proxies = self.create_proxies()
        try:
            response = requests.get(url, headers=headers, proxies=proxies)
        except:
            return None
        return [response.text, response.status_code]

    # 解析网页源代码并保存
    def parse_html(self, html, book_id):
        # beautifulsoup 解析
        soup = BeautifulSoup(html, 'html.parser')
        # 书名
        self.book['id'] = book_id
        name = soup.find('span', attrs={'property': 'v:itemreviewed'})
        if not name:
            return
        self.book['name'] = name.text
        # info
        info = soup.find('div', attrs={'id': 'info'}).text
        # print(info)
        # 从 info 中匹配出作者和出版年份
        # 可能没有
        content = re.findall('作者:(.*?)出', info, re.S)
        if not content:
            author = ' '
        else:
            author = content[0].replace('\n', ' ')
        self.book['author'] = ' '.join(author.split()) # 去除多余空格
        content = re.findall('出版年:(.*?)\n', info, re.S)
        if not content:
            date = ' '
        else:
            date = content[0]
        self.book['date'] = date.strip()
        # 评分
        score = soup.find('strong', attrs={'property': 'v:average'}).text.strip()
        # 评分人数
        score_num = soup.find('span', attrs={'property': 'v:votes'}).text.strip()
        self.book['score'] = (score, score_num)
        # 内容简介
        content = soup.find('div', attrs={'class': 'intro'})
        # 可能没有
        if not content:
            intro = ' '
        else:
            intro = content.text.replace('\n', ' ').replace('\r', ' ').strip()
        if intro.find('展开全部') != -1:
            # 获取完整内容简介
            self.book['intro'] = soup.find_all('div', attrs={'class': 'intro'})[1].text.replace('\n', ' ').replace('\r', ' ').strip()
        else:
            self.book['intro'] = intro

        # 作者简介
        content = soup.find_all('div', attrs={'class': 'intro'})
        if not content:
            self.book['author_intro'] = ' '
        else:
            self.book['author_intro'] = content[-1].text.replace('\n', ' ').replace('\r', ' ').strip()
        # 推荐书籍，找 dd 标签
        other = soup.find_all('dd')
        # 从 other 中匹配出推荐书籍名称和链接，以列表形式保存
        self.book['recommend'] = []
        for i in other:
            # 推荐书籍名称
            recommend_name = i.find('a').text.strip()
            # 推荐书籍id
            recommend_id = i.find('a')['href'].split('/')[-2]
            # 保存到列表
            self.book['recommend'].append((recommend_name, recommend_id))
        
    # 保存到文件
    def save_book(self):
        # 保存到 book.csv, 需要加锁保证原子性
        with open('./part1/spider/res/book.csv', 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.book.values())
        # print('保存成功！')

    # 主函数
    def main(self):        
        for book_id in self.id_list:
            print('正在爬取 book_id 为 {} 的书籍信息...\n'.format(book_id))
            url = self.create_url(book_id)
            [html, status_code] = self.get_html(url)
            if status_code == 404:
                print('链接失效！\n'.format(book_id))
                error.append(book_id)
                continue
            while status_code == 403:
                print('请求失败，正在重试...\n')
                [html, status_code] = self.get_html(url)
            with lock:
                self.parse_html(html, book_id)
                self.save_book()
            # 随机休眠 0-2s
            time.sleep(random.uniform(0, 2))

# 读取 book_id
with open('./part1/spider/data/Book_id.csv', 'r') as f:
    list = f.read().splitlines()
# 多线程执行
spider = []
threads = []
for i in range(0, 12):
    spider.append(BookSpider(list[100*i : 100*i + 100]))
    threads.append(threading.Thread(target=spider[i].main))
for t in threads:
    t.start()
for t in threads:
    t.join()
print('\nCongratulations!\n')
# 把error的id保存到文件
with open('./part1/spider/res/error.txt', 'a+') as f:
    f.write(str(error))

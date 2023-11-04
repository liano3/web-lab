"""
@Descripttion: 爬取电影信息
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
class MovieSpider():
    # 基础 url
    base_url = 'https://movie.douban.com/subject/{}/'
    #movie 数据结构
    movie = {
        'id': '',
        'name':'',
        'director':'',
        'writer':'',
        'actor':'',
        'type':'',
        'region':'',
        'language':'',
        'date':'',
        'runtime':'',
        'alias':'',
        'IMDb':'',
        'intro':'',
    }

    # id_list
    id_list = []
    ip = ''

    # 初始化 id_list
    def __init__(self, movie_id_list):
        self.id_list = movie_id_list
    
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
    def create_url(self, movie_id):
        url = self.base_url.format(movie_id)
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
    def parse_html(self, html, movie_id):
        # beautifulsoup 解析
        soup = BeautifulSoup(html, 'html.parser')
        # 电影名
        self.movie['id'] = movie_id
        name = soup.find('span', attrs={'property': 'v:itemreviewed'})
        if not name:
            return
        self.movie['name'] = name.text
        # info
        info = soup.find('div', attrs={'id': 'info'}).text
        # print(info)
        # 从 info 中匹配
        # 可能没有
        content = re.findall('导演:(.*?)编', info, re.S)
        if not content:
            director = ' '
        else:
            director = content[0].replace('\n', ' ')
        self.movie['director'] = ' '.join(director.split()) # 去除多余空格
        content = re.findall('编剧:(.*?)主', info, re.S)
        if not content:
            writer = ' '
        else:
            writer = content[0].replace('\n', ' ')
        self.movie['writer'] = ' '.join(writer.split())
        content = re.findall('主演:(.*?)类', info, re.S)
        if not content:
            actor = ' '
        else:
            actor = content[0].replace('\n', ' ')
        self.movie['actor'] = ' '.join(actor.split())
        content = re.findall('类型:(.*?)制', info, re.S)
        if not content:
            type = ' '
        else:
            type = content[0].replace('\n', ' ')
        self.movie['type'] = ' '.join(type.split())
        content = re.findall('制片国家/地区:(.*?)语', info, re.S)
        if not content:
            region = ' '
        else:
            region = content[0].replace('\n', ' ')
        self.movie['region'] = ' '.join(region.split())
        content = re.findall('语言:(.*?)上', info, re.S)
        if not content:
            language = ' '
        else:
            language = content[0].replace('\n', ' ')
        self.movie['language'] = ' '.join(language.split())
        content = re.findall('上映日期:(.*?)片', info, re.S)
        if not content:
            date = ' '
        else:
            date = content[0].replace('\n', ' ')
        self.movie['date'] = ' '.join(date.split())
        content = re.findall('片长:(.*?)又', info, re.S)
        if not content:
            content = re.findall('片长:(.*?)I', info, re.S)
            if not content:
                runtime = ' '
            else:
                runtime = content[0].replace('\n', ' ')
        else:
            runtime = content[0].replace('\n', ' ')
        self.movie['runtime'] = ' '.join(runtime.split())
        content = re.findall('又名:(.*?)I', info, re.S)
        if not content:
            alias = ' '
        else:
            alias = content[0].replace('\n', ' ')
        self.movie['alias'] = ' '.join(alias.split())
        content = re.findall('IMDb:(.*?)\n', info, re.S)
        if not content:
            IMDb = ' '
        else:
            IMDb = content[0].replace('\n', ' ')
        self.movie['IMDb'] = ' '.join(IMDb.split())
        # 内容简介
        content = soup.find('div', attrs={'class': 'indent' , 'id': 'link-report-intra'})
        # 可能没有
        if not content:
            intro = ' '
        else:
            intro = content.text.replace('\n', ' ').replace('\r', ' ').strip()
            if intro.find('展开全部') != -1:
                # 获取完整内容简介
                self.movie['intro'] = soup.find('span', attrs={'class': 'all hidden'}).text.replace('\n', ' ').replace('\r', ' ').strip()
            else:
                self.movie['intro'] = soup.find('span', attrs={'property': 'v:summary'}).text.replace('\n', ' ').replace('\r', ' ').strip()

    # 保存到文件
    def save_movie(self):
        # 保存到 ./result/movie.csv, 需要加锁保证原子性
        with open('./part1/spider/res/movie.csv', 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.movie.values())
        # print('保存成功！')

    # 主函数
    def main(self):        
        for movie_id in self.id_list:
            print('正在爬取 movie_id 为 {} 的电影信息...\n'.format(movie_id))
            url = self.create_url(movie_id)
            [html, status_code] = self.get_html(url)
            if status_code == 404:
                print('链接失效！\n'.format(movie_id))
                error.append(movie_id)
                continue
            while status_code == 403:
                print('请求失败，正在重试...\n')
                [html, status_code] = self.get_html(url)
            with lock:
                self.parse_html(html, movie_id)
                self.save_movie()
            # 随机休眠 0-2s
            time.sleep(random.uniform(0, 2))

# 读取 movie_id
with open('./part1/spider/data/Movie_id.csv', 'r') as f:
    list = f.read().splitlines()
# 多线程执行
spider = []
threads = []
for i in range(0, 12):
    spider.append(MovieSpider(list[100*i : 100*i + 100]))
    threads.append(threading.Thread(target=spider[i].main))
for t in threads:
    t.start()
for t in threads:
    t.join()
print('\nCongratulations!\n')
# 把error的id保存到文件
with open('./part1/spider/res/error.txt', 'a+') as f:
    f.write(str(error))

"""
@Description: 爬取免费代理IP, 构造代理IP池
"""

import requests
from bs4 import BeautifulSoup

# 获取免费代理IP
def get_fake_ip(index=1):
    url = 'https://www.beesproxy.com/free/page/' + str(index)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    ip_list = soup.select('tbody > tr > td:nth-child(1)')
    port_list = soup.select('tbody > tr > td:nth-child(2)')
    fake_ip_list = []
    for index in range(len(ip_list)):
        fake_ip_list.append(ip_list[index].text + ':' + port_list[index].text)
    return fake_ip_list

# 测试 ip 是否可用
def test_ip(ip):
    print('测试 ip: {}...\n'.format(ip))
    url = 'https://douban.com'
    proxies = {
        'http': 'http://' + ip
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    try:
        response = requests.get(url, proxies=proxies, headers=headers, timeout=2)
        if response.status_code == 200:
            print('测试成功！\n')
            return True
        else:
            return False
    except:
        return False

# 获取可用的代理IP
def get_valid_ip(fake_ip_list):
    valid_ip_list = []
    for ip in fake_ip_list:
        if test_ip(ip):
            valid_ip_list.append(ip)
    return valid_ip_list

# 生成代理IP池
def get_ip_pool(start=1, end=10):
    valid_ip_list = []
    for index in range(start, end):
        fake_ip_list = get_fake_ip(index)
        valid_ip_list.extend(get_valid_ip(fake_ip_list))
    # 保存到文件
    with open('./part1/spider/src/ip_info.txt', 'w') as f:
        f.write('ip_list = [\n')
        for ip in valid_ip_list:
            f.write('    "{}",\n'.format(ip))
        f.write(']\n')
    return valid_ip_list

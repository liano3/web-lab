"""
@Descripttion: 生成 UA
"""

#模块随机获取UA
from fake_useragent import UserAgent

# 获取UA池
def get_ua_pool(index=10):
    ua = UserAgent()
    ua_list = []
    for i in range(index):
        ua_list.append(ua.random)
    # 保存到文件
    with open('./part1/spider/src/ua_info.txt', 'w') as f:
        f.write('ua_list = [\n')
        for i in range(10):
            f.write('    "{}",\n'.format(ua.random))
        f.write(']\n')
    return ua_list

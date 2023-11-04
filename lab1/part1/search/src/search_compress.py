"""
@Description: 压缩后的搜索
"""

import csv
import time
# 获取索引
index = {}
with open('./part1/search/res/index.txt', 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()
    for line in lines:
        index[line.split(' ')[0]] = line.split(' ')[1:]
    # print(index)

# 获取倒排索引
compress = {}
keywords = ''
with open('./part1/search/res/inverted_index_compress.txt', 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()
    keywords = lines[0]
    # print(keywords)
    lines = lines[1:]
    for line in lines:
        compress[int(line.split(' ')[0])] = line.split(' ')[1:]
    # print(inverted_index)

# 解压缩
inverted_index = {}
# keywords[key1:key2] 为关键词
# 累加之后才是真正的value
for key1, key2 in zip(list(compress.keys()), list(compress.keys())[1:]):
    tag = keywords[key1:key2]
    # print(tag)
    inverted_index[tag] = []
    sum = 0
    for i in compress[key1]:
        sum += int(i)
        inverted_index[tag].append(str(sum))
# print(inverted_index)

# 处理 and 和 not
def search_and(query):
    tags = query.split('and')
    not_list = []
    for tag in tags:
        if 'not' in tag:
            not_list.append(tag.split('not')[1].strip())
            tags.remove(tag)
    # 可能不存在
    try:
        result = set(inverted_index[tags[0].strip()])
    except:
        return set()
    for tag in tags:
        try:
            result = result & set(inverted_index[tag.strip()])
        except:
            return set()
    for tag in not_list:
        try:
            result = result - set(inverted_index[tag.strip()])
        except:
            return set()
    return result

# 处理 or
def search(query):
    tags = query.split('or')
    result = set()
    for tag in tags:
        result = result | search_and(tag)
    # print(result)
    return result

while True:
    query = input('请输入查询语句：(q 退出)\n')
    if query == 'exit':
        break
    t1 = time.time()
    result = search(query)
    t2 = time.time()
    print('查询耗时：{}s'.format(t2 - t1))
    id_list = []
    print('查询结果：')
    count = 0
    for item in result:
        count += 1
        if count > 50:
            break
        id_list.append(index[item][0])
    # 根据 id 在 movie.csv 或 book.csv 中找到对应的电影或书籍
    with open('./part1/spider/res/book.csv', 'r', encoding='utf-8') as f:
        # 读取 book.csv 中第一列值为 id 的行
        book_list = csv.reader(f)
        for book in book_list:
            # 打印书籍名称和简介
            if book[0] in id_list:
                print("书籍：{}".format(book[1]))
                print("简介：{}\n".format(book[5]))

    with open('./part1/spider/res/movie.csv', 'r', encoding='utf-8') as f:
        movie_list = csv.reader(f)
        for movie in movie_list:
            if movie[0] in id_list:
                pass
                print("电影：{}".format(movie[1]))
                print("简介：{}\n".format(' '.join(movie[12].replace('\n', ' ').replace('\r', ' ').split())))
    print('----------------------------------------')

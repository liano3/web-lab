"""
@Description: 建立索引并压缩
"""

with open('./part1/search/res/tags.txt', 'r', encoding='utf-8') as f:
    list = f.read().splitlines()

# 生成索引
index = {}
i = 1
for item in list:
    index[i] = item
    i += 1
with open('./part1/search/res/index.txt', 'w', encoding='utf-8') as f:
    for key, value in index.items():
        f.write(str(key) + ' ' + value + '\n')

# 生成倒排索引
# 将关键词压缩为一个字符串，倒排表中存储的是关键词在压缩字符串中的位置
# 编号只记录差值，减少存储空间
keywords = ''
pos = {}
inverted_index = {}
last_key = {}
for key,value in index.items():
    for tag in value.split(' '):
        if tag == '':
            continue
        if tag not in pos:
            last_key[tag] = 0
            pos[tag] = len(keywords)
            inverted_index[pos[tag]] = []
            keywords += tag
        # 去除重复的
        temp = key - last_key[tag]
        if temp != 0:
            inverted_index[pos[tag]].append(key - last_key[tag])
        last_key[tag] = key
keywords += '\n'
with open('./part1/search/res/inverted_index_compress.txt', 'w', encoding='utf-8') as f:
    f.write(keywords)
    for key, value in inverted_index.items():
        f.write(str(key) + ' ' + ' '.join(str(x) for x in value) + '\n')

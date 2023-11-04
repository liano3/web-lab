"""
@Description: 生成倒排索引
"""

with open('./part1/search/res/tags.txt', 'r', encoding='utf-8') as f:
    list = f.read().splitlines()

# 生成索引
index = {}
i = 1
for item in list:
    index[str(i)] = item
    i += 1
with open('./part1/search/res/index.txt', 'w', encoding='utf-8') as f:
    for key, value in index.items():
        f.write(key + ' ' + value + '\n')

# 生成倒排索引
inverted_index = {}
# 将值作为 key，将 key 作为值
for key, value in index.items():
    for tag in value.split(' '):
        if tag == '':
            continue
        if tag not in inverted_index:
            inverted_index[tag] = []
        inverted_index[tag].append(key)
with open('./part1/search/res/inverted_index.txt', 'w', encoding='utf-8') as f:
    for key, value in inverted_index.items():
        f.write(key + ' ' + ' '.join(value) + '\n')

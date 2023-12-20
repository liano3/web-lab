'''
根据映射关系，将电影实体的ID 映射到[0, num of movies)范围内。
将图谱中的其余实体映射到[num of movies, num of entities)范围内，
将关系映射到[0, num of relations)范围内。
再根据这些映射关系，将第一阶段获得的电影图谱映射为由索引值组成的三元组。
并保存到 \data\Douban\kg_final.txt 文件中。
'''

# 先获得电影 ID 到实体 ID 的映射关系
movie_entity_map = {}
with open('data/douban2fb.txt', 'r') as f:
    for line in f:
        # 格式不统一，有的 \t 有的空格
        # 将 \t 替换成空格
        line = line.replace('\t', ' ')
        line = line.strip().split(' ')
        movie_entity_map[line[0]] = line[1]

# print('movie_entity_map: ', list(movie_entity_map.items())[:5])

entity_id_map = {}
# 打开 movie_id_map.txt
with open('data/movie_id_map.txt', 'r') as f:
    # 读取每一行
    lines = f.readlines()
    for line in lines:
        # 将每一行按照空格分割
        line = line.strip().split()
        # 将电影实体的ID 映射到[0, num of movies)范围内
        entity_id_map[movie_entity_map[line[0]]] = int(line[1])

print('entity_id_map: ', list(entity_id_map.items())[:5])

# 打开 FinalGraph.gz，读取所有三元组
import gzip
triples = []
with gzip.open('data/FinalGraph.gz', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        triplet = line.decode().split('\t')[:3]
        triples.append(triplet)

# print('triples: ', triples[:5])

# 将图谱中的其余实体映射到[num of movies, num of entities)范围内
entity_id = len(entity_id_map)
for triplet in triples:
    if triplet[0] not in entity_id_map:
        entity_id_map[triplet[0]] = entity_id
        entity_id += 1
    if triplet[2] not in entity_id_map:
        entity_id_map[triplet[2]] = entity_id
        entity_id += 1

# 打印最后 5 项
print('entity_id_map: ', list(entity_id_map.items())[-5:])

# 将关系映射到[0, num of relations)范围内
relation_id_map = {}
relation_id = 0
for triplet in triples:
    if triplet[1] not in relation_id_map:
        relation_id_map[triplet[1]] = relation_id
        relation_id += 1

# 打印最后 5 项
print('relation_id_map: ', list(relation_id_map.items())[-5:])

# 将第一阶段获得的电影图谱映射为由索引值组成的三元组
triples_id = []
for triplet in triples:
    triplet_id = [entity_id_map[triplet[0]], relation_id_map[triplet[1]], entity_id_map[triplet[2]]]
    triples_id.append(triplet_id)

# 保存到 \data\kg_final.txt 文件中
with open('data/Douban/kg_final.txt', 'w') as f:
    for triplet_id in triples_id:
        # 用空格分割，不然后面读取的时候会出错
        f.write(str(triplet_id[0]) + ' ' + str(triplet_id[1]) + ' ' + str(triplet_id[2]) + '\n')
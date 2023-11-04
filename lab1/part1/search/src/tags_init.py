"""
@Descripttion: 生成tags.txt
"""

import jieba

#jieba需要将全角转换为半角 下面是转换函数
def strQ2B(ustring):    
    rstring = ""    
    for uchar in ustring:        
        inside_code = ord(uchar)        
        if inside_code == 12288: # 全角空格直接转换            
            inside_code = 32        
        elif 65281 <= inside_code <= 65374: #全角字符除空格根据关系转化            
            inside_code -= 65248        
        rstring += chr(inside_code)    
    return rstring

#预处理停用词
stopwords = []
stopwords_path = './part1/search/data/cn_stopwords.txt'
with open (stopwords_path, 'r', encoding='utf-8') as f:
    stopwords = [line.strip() for line in f.readlines()]

#预处理同义词近义词
combine_dict = {}
for line in open("./part1/search/data/dict_synonym.txt", "r", encoding='utf-8'):
    seperate_word = line.strip().split(" ")
    num = len(seperate_word)
    for i in range(2, num):
        combine_dict[seperate_word[i]] = seperate_word[1]

#获取sentence的tag
def get_tag(sentence):
    sentence = strQ2B(sentence)
    text = jieba.lcut(sentence)   
    clean_text = [word for word in text if word not in stopwords]

    combined_text = []

    for word in clean_text:
        if word in combine_dict:
            word = combine_dict[word]
        combined_text.append(word)

    exist_dict = []
    final_tags = []

    for word in combined_text:
        if not (word in exist_dict):
            exist_dict.append(word)
            final_tags.append(word) 
    
    return final_tags

#处理movie
with open('./part1/spider/res/movie.csv', 'r', encoding='utf-8') as f:
    movie_list = f.read().splitlines()
for line in movie_list:
    members = line.split(',')
    tags = ""
    tags += members[0] + ' '
    sep = members[1].split(' ')
    for tag in sep:
        tags += tag.strip() + ' '
    for i in range(2,8):
        sep = members[i].split('/')
        for tag in sep:
            tags += tag.strip() + ' '
    sep = members[10].split('/')
    for tag in sep:
        tags += tag.strip() + ' '
    tags += members[11] + ' '
    final_tags = get_tag(members[12])
    for tag in final_tags:
        tags += tag + ' '
    with open('./part1/search/res/tags.txt', 'a+', encoding='utf-8', newline='') as f2:
        f2.write(tags + '\n')

#处理book
with open('./part1/spider/res/book.csv', 'r', encoding='utf-8') as f:
    book_list = f.read().splitlines()
for line in book_list:
    members = line.split(',')
    tags = ""
    tags += members[0] + ' '
    tags += members[1] + ' '
    sep = members[2].split('/')
    for tag in sep:
        tags += tag.strip() + ' '
    final_tags = get_tag(members[6])
    for tag in final_tags:
        tags += tag + ' '
    final_tags = get_tag(members[7])
    for tag in final_tags:
        tags += tag + ' '
    with open('./part1/search/res/tags.txt', 'a+', encoding='utf-8', newline='') as f2:
        f2.write(tags + '\n')

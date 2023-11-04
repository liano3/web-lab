#pip install hanlp
#pip install jieba

import hanlp 
import jieba
import time
sentence = u'''
《青鸟》是梅特林克的最著名的代表作。原作是直到今天仍在舞台上演出的六幕梦幻剧，
后经梅特林克同意，他的妻子乔治特·莱勃伦克将剧本改写成童话故事，以便更适合小读者阅读。
改编成的中篇童话《青鸟》在1908年发表。 故事讲述两个伐木工人的孩子，代表人类寻找青鸟的过程。
青鸟在这里是幸福的象征。通过他们一路上的经历，象征性地再现了迄今为止，人类为了寻找幸福所经历过的全部苦难。
作品中提出了一个对人类具有永恒意义的问题：什么是幸福？但是作品所得出的结论却是出乎意料的：
其实幸福并不那么难找，幸福就在我们身边。
'''
t1 = time.time()
HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH) # 世界最大中文语料库
dic = HanLP(sentence)
res = dic.setdefault('tok/coarse')
t2 = time.time()
print("HanLP分词时间：",t2-t1)
print("HanLP分词结果：")
print("/ ".join(res))
print("=====================================")

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
t3 = time.time()
sentence = strQ2B(sentence)
text = jieba.lcut(sentence)
t4 = time.time()
print("jieba分词时间：",t4-t3)
print("jieba分词结果：")
print("/ ".join(text))

#-*- coding: utf-8 -*-
import pandas as pd #导入pandas，用于操作excel文件
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud as WordCloud_Python 
from wordcloud import STOPWORDS
import jieba
from pyecharts import WordCloud
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
df=pd.read_excel('2018-04-26 (2)(已自动还原).xls',sheet_name='sheet1')#打开excel文件
cn_text=[]
for i,j in enumerate(df['公开（公告）号']):
    if 'CN' in j or 'TW' in j:
        continue
    else:
        cn_text.append(df['摘要'][i])

cn_str=''
for i in cn_text:
    if type(i)==str:
        cn_str+=i

seg_list = jieba.cut(cn_str, cut_all=False)
seg_str = ' '.join(jieba.cut(cn_str,cut_all = False))
text = nltk.word_tokenize(seg_str)
n_list=nltk.pos_tag(text)
add_list=[]
for text,name in n_list:
    if name == 'N' or name=='NN' or name=='NNP' or name=='NNS' or name=='NNPS':
        add_list.append(text)
cn_dic={}
for i in seg_list:
    if i not in cn_dic:
        cn_dic[i]=0
        cn_dic[i]+=1
    else:
        cn_dic[i]+=1
word_list=sorted(cn_dic.items(), key=lambda d: d[1],reverse=True)

#读入用户指定的过滤词汇
with open('stopword.txt','r',encoding='utf8') as f:
    txt=f.read()
stopword_list=txt.split(',')

#以下使用pyecharts绘制词云
name=[]
value=[]
for i in word_list:
    if i[0] in stopword_list:
        continue
    else:
        if i[0] in add_list and len(i[0])>1:
            name.append(i[0])
            value.append(i[1])

wordcloud = WordCloud(width=1300, height=620)
wordcloud.add("", name[:1000], value[:1000], word_size_range=[10, 200])
wordcloud.render('wordcloud.html')


#以下使用wordcloud绘图
stopwords = set(STOPWORDS)
for i in stopword_list:
    stopwords.add(i)

wc = WordCloud_Python(width=800,height=600,max_words=1000,stopwords=stopwords, margin=10,colormap='Accent',
               random_state=1).generate(seg_str)
# store default colored image
default_colors = wc.to_array()
plt.figure()
plt.title("XXX领域核心技术词云")
plt.imshow(default_colors)
plt.axis("off")
plt.savefig('cloud.png')
plt.show()





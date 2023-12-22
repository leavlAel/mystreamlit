import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import jieba
from collections import Counter
from wordcloud import WordCloud
import base64
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import matplotlib  
matplotlib.rc('font', family='SimHei')



url = st.text_input("请输入url")
# 筛选图形的侧边栏
st.sidebar.subheader('图形筛选')
graph_type = st.sidebar.selectbox('请选择图形类型', ['词云', '条形图', '饼图', '直方图', '散点图', '线图', '雷达图'])
response = requests.get(url)
# 解析HTML并提取body标签中的内容和标签  
soup = BeautifulSoup(response.content, 'html.parser')  
div = soup.find('div', {'id': 'UCAP-CONTENT'})
#获取文本内容
content = div.text
#st.write(content)
#去除标点
new_content = re.sub(r'[^\w\s]', '', content)
#去除换行符
new_content = new_content.replace("\n","")
#st.write(new_content)
#对文本分词，统计词频
words_list = jieba.cut(new_content)
word_count = Counter(word for word in words_list if word)

# 按照值大小排序，并获取前20个键值对  
sorted_items = sorted(word_count.items(), key=lambda x: x[1],reverse=True)[:20]
#新字典
sorted_dict = dict(sorted(word_count.items(),key=lambda item:item[1],reverse=True))
#取出前20个键值对生成新字典
keys = list(sorted_dict.keys())[:20]
values = [sorted_dict[key] for key in keys]
words_count = dict(zip(keys,values))


if graph_type == '词云':
    #将词频字典转换为列表，以便wordcloud可以处理
    words = list(words_count.keys())
    counts = list(words_count.values())
    #创建词云
    wordcloud = WordCloud(font_path='SimHei.ttf',width=800,height=800,background_color='white').generate_from_frequencies(dict(zip(words,counts)))
    #在matplotlib中显示词云
    fig = plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    #在streamlit中显示图像
    st.subheader('绘制词云图')
    st.pyplot(fig)
elif graph_type == '条形图':
    # 将字典转换为列表，以便条形图可以处理
    words = list(words_count.keys())
    counts = list(words_count.values())
    # 在matplotlib中创建条形图
    fig = plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Counts')
    plt.title('Word Count')
    # 在streamlit中显示图像
    st.subheader('绘制条形图')
    st.pyplot(fig)
elif graph_type == '饼图':
    # 将字典转换为列表，以便饼图可以处理
    words = list(words_count.keys())
    counts = list(words_count.values())
    # 在matplotlib中创建饼图
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(counts, labels=words, autopct='%1.1f%%', startangle=90)
    # 设置中心文本
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # 在streamlit中显示图像
    st.subheader('绘制饼图')
    st.pyplot(fig)
elif graph_type == '直方图':
    # 将字典转换为列表，以便直方图可以处理
    bins = list(words_count.keys())
    counts = list(words_count.values())

    # 在matplotlib中创建直方图
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(bins, bins=bins, weights=counts)
    # 设置轴标签和标题
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram of Data')
    # 在streamlit中显示图像
    st.subheader('绘制直方图')
    st.pyplot(fig)
elif graph_type == '散点图':
    # 将字典转换为列表，以便散点图可以处理
    keys = list(words_count.keys())
    values = list(words_count.values())

    # 在matplotlib中创建散点图
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(keys, values)
    # 设置轴标签和标题
    ax.set_xlabel('Variable 1')
    ax.set_ylabel('Variable 2')
    ax.set_title('Scatter Plot of Data')
    # 在streamlit中显示图像
    st.subheader('绘制散点图')
    st.pyplot(fig)
elif graph_type == '线图':
    # 将字典转换为列表，以便线图可以处理
    keys = list(words_count.keys())
    values = list(words_count.values())
    # 在matplotlib中创建线图
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(keys, values)
    # 设置轴标签和标题
    ax.set_xticks(range(len(keys)))
    ax.set_xticklabels(keys)
    ax.set_xticks(keys)
    ax.set_xlabel('Time or Sequence')
    ax.set_ylabel('Data Value')
    ax.set_title('Line Plot of Data')
    # 在streamlit中显示图像
    st.subheader('绘制线图')
    st.pyplot(fig)
elif graph_type == '雷达图':
    # 将字典转换为列表和数组，以便雷达图可以处理
    categories = list(words_count.keys())
    values = np.array(list(words_count.values()))

    # 在matplotlib中创建雷达图
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(values.T, color='blue', alpha=0.3)
    ax.set_yticklabels(categories)
    # 设置轴标签和标题
    ax.set_xlabel('Word Count')
    ax.set_title('Radar Plot of Word Frequencies')
    # 在streamlit中显示图像
    st.subheader('绘制雷达图')
    st.pyplot(fig)
st.subheader('词频排名前20的词汇')
st.write('', ', '.join(words_count.keys()))

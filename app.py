import streamlit as st  
from pyecharts import options as opts  
from pyecharts.charts import Bar  
import jieba
import requests
from collections import Counter
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import re 
from pyecharts.charts import WordCloud
from pyecharts.charts import Pie  
from pyecharts.charts import Scatter
from pyecharts.charts import Line    
from pyecharts.charts import Radar 
from pyecharts.charts import Funnel

# 筛选图形的侧边栏
st.sidebar.subheader('图形筛选')
graph_type = st.sidebar.selectbox('请选择图形类型', ['词云', '条形图', '饼图', '横向柱状图', '散点图', '线图', '漏斗图'])
url = st.text_input("请输入url")
if url:
    response = requests.get(url)
    response.encoding=response.apparent_encoding
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
        wordcloud = WordCloud()  
        wordcloud.add("", list(words_count.items()), word_size_range=[20, 100], shape='triangle')  
        wordcloud.set_global_opts(title_opts=opts.TitleOpts(title="词云图"))  
        wordcloud.render("wordcloud.html")  
        # 在Streamlit应用中显示词云图
        st.components.v1.html(open('wordcloud.html', 'r', encoding='utf-8').read(), height=600,width=850)
    elif graph_type == '条形图':
        bar = Bar()  
        bar.add_xaxis(list(words_count.keys()))  
        bar.add_yaxis("频次", list(words_count.values()))  
        bar.set_global_opts(title_opts=opts.TitleOpts(title="条形图"),xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)))  
        bar.render("bar_chart.html") 
        # 在Streamlit应用中显示条形图  
        st.components.v1.html(open('bar_chart.html', 'r', encoding='utf-8').read(), height=600,width=850) 
    elif graph_type == '饼图':
        pie = Pie()  
        pie.add("", [list(z) for z in zip(words_count.keys(), words_count.values())])  
        pie.set_global_opts(title_opts=opts.TitleOpts(title="饼图"))  
        pie.render("pie_chart.html")  
        # 在Streamlit应用中显示饼图  
        st.components.v1.html(open('pie_chart.html', 'r', encoding='utf-8').read(), height=600,width=850)
    elif graph_type == '散点图':
        scatter = Scatter()  
        scatter.add_xaxis(list(words_count.keys()))  
        scatter.add_yaxis('频次',list(words_count.values()))  
        scatter.set_global_opts(title_opts=opts.TitleOpts(title="散点图"),xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)))  
        scatter.render("scatter_chart.html")   
        # 在Streamlit应用中显示散点图  
        st.components.v1.html(open('scatter_chart.html', 'r', encoding='utf-8').read(), height=600,width=850) 
    elif graph_type == '横向柱状图':
        bar = Bar()
        bar.add_xaxis(list(words_count.keys()))
        bar.add_yaxis("", list(words_count.values()))
        bar.reversal_axis()
        # 生成HTML文件
        bar.render('histogram_chart.html')
        # 在Streamlit应用中显示直方图  
        st.components.v1.html(open('histogram_chart.html', 'r', encoding='utf-8').read(), height=600,width=850)
    elif graph_type == '线图':
        # 将数据转化为两个列表，一个为x轴，一个为y轴  
        x_data = list(words_count.keys())  
        y_data = list(words_count.values())  
        # 创建一个线图对象  
        line_chart = Line()  
        # 添加x轴和y轴的数据，以及线的类型  
        line_chart.add_xaxis(x_data)  
        line_chart.add_yaxis("数值", y_data, is_smooth=True)  # is_smooth=True 表示曲线平滑  
        # 设置图的全局配置项，例如标题和图例等  
        line_chart.set_global_opts(title_opts=opts.TitleOpts(title="线图"),xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)))
        line_chart.render("line_chart.html")
        # 在Streamlit应用中显示线图  
        st.components.v1.html(open('line_chart.html', 'r', encoding='utf-8').read(), height=600,width=850)
    elif graph_type == '漏斗图': 
        funnel = Funnel()
        funnel.add("", list(words_count.items()))
        funnel.render('funnel.html')
        # 在Streamlit应用中显示线图  
        st.components.v1.html(open('funnel.html', 'r', encoding='utf-8').read(), height=600,width=850)
st.subheader('词频排名前20的词汇')
st.write('', ', '.join(words_count.keys()))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 14:27:57 2019

@author: owlting
"""
import pyspark 
from pyspark import SparkContext as sc
from pyspark import SparkConf
from pyspark.sql import SparkSession
from sklearn.utils import shuffle
import numpy as np 
import pandas as pd 
import string
import matplotlib.pyplot as plt
from pyspark.sql import SQLContext
from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
"""
0 讀取資料並根據需要的欄位進行merge
"""
geo = pd.read_csv('/Users/owlting/Downloads/brazilian-ecommerce/olist_geolocation_dataset.csv',header=None)  # 讀取訓練數據
geo.columns = ['customer_zip_code_prefix',geo[1][0],geo[2][0],geo[3][0],geo[4][0]] #更改attribute
geo=geo.drop(index=[0])
customer = pd.read_csv('/Users/owlting/Downloads/brazilian-ecommerce/olist_customers_dataset.csv')  # 讀取訓練數據
product = pd.read_csv('/Users/owlting/Downloads/brazilian-ecommerce/olist_products_dataset.csv')  # 讀取訓練數據
order_item = pd.read_csv('/Users/owlting/Downloads/brazilian-ecommerce/olist_order_items_dataset.csv',header=None)  # 讀取訓練數據
order_payment = pd.read_csv('/Users/owlting/Downloads/brazilian-ecommerce/olist_order_payments_dataset.csv',header=None)  # 讀取訓練數據
order_review = pd.read_csv('/Users/owlting/Downloads/brazilian-ecommerce/olist_order_reviews_dataset.csv',header=None)  # 讀取訓練數據
order = pd.read_csv('/Users/owlting/Downloads/brazilian-ecommerce/olist_orders_dataset.csv',header=None)  # 讀取訓練數據
seller = pd.read_csv('/Users/owlting/Downloads/brazilian-ecommerce/olist_sellers_dataset.csv',header=None)  # 讀取訓練數據
category = pd.read_csv('/Users/owlting/Downloads/brazilian-ecommerce/product_category_name_translation.csv',header=None)  # 讀取訓練數據
agg = pd.merge(order,customer, on='customer_id')
agg2 = pd.merge(order_item,agg, on='order_id')
agg3 = pd.merge(product,agg2, on='product_id')
agg4 = pd.merge(category,agg3, on='product_category_name')
agg5 = pd.merge(order_review,agg4, on='order_id')
#customer_zip_code_prefix不唯一 同個碼會有不同的經緯度 導致merge後資料量暴增
geo=geo.drop_duplicates(subset=['customer_zip_code_prefix'], keep='first')
agg6 = pd.merge(geo,agg5, on='customer_zip_code_prefix')
agg7 = pd.merge(seller,agg5, on='seller_id')

"""
1-1 統計法：巴西各地區商品類別推薦
"""
cgst = agg4[['product_category_name_english','customer_state']]
cgst = cgst.dropna(subset=['product_category_name_english']) #把nan值去掉
customer_state_data=cgst['customer_state'].value_counts() #counts計數
print('各州訂單數量：')
customer_state_data.plot.bar()
cg_set=list(set(cgst["product_category_name_english"]))
st_set=list(set(cgst["customer_state"]))
def graph(series,state):
    plt.figure(figsize=(20,16))
    plt.title('favorite category top 10 in '+state)
    index = list(series.index)
    count = list(category_total[:])
    plt.bar(index,count,width = 0.35,facecolor = 'dodgerblue',edgecolor = 'white')
    plt.xticks(rotation='vertical')
    plt.savefig('favorite_category_'+state+'.png')
    plt.show()
    return 0;
for st in st_set:
    mask1 = cgst["customer_state"] == st
    state_total=cgst[mask1] 
    category_total = state_total.groupby("product_category_name_english")
    category_total = category_total.size()
    category_total = category_total.sort_values(ascending = False).head(10)
    graph(category_total,st)
    category_output = category_total.sort_values(ascending = False).head(3)
    recommend_list=list(category_output.index)
    print('recommend list for people in '+st+':')
    print(recommend_list)
    #a = category_total.plot.bar(title='favorite category top 10 in '+st)

"""
2-1 pysparkml實作：用運費(f)、耗時(d)、地區(g)當作feature以MLP判斷評價(r)
"""
conf=SparkConf().setAppName("miniProject").setMaster("local[*]")
sc=sc.getOrCreate(conf) #可以視情況新建session或使用已有的session
sc = SQLContext(sc)
gr = agg6[['review_score','geolocation_lat','geolocation_lng','price','freight_value','order_purchase_timestamp','order_delivered_customer_date']]
gr = shuffle(gr)

def dayd(a,b):
    return (pd.Timestamp(a)-pd.Timestamp(b)).days

gr['dd'] = gr.apply(lambda row: dayd(row['order_delivered_customer_date'], row['order_purchase_timestamp']), axis=1)
gr = gr.dropna(subset=['dd']) #把nan值去掉
#評價簡化
gr1 = gr
gr1 = gr1.replace('1','0')
gr1 = gr1.replace('2','1')
gr1 = gr1.replace('3','1')
gr1 = gr1.replace('4','2')
gr1 = gr1.replace('5','2')
gr1_final = gr1[['review_score','geolocation_lat','geolocation_lng','freight_value','dd']]
gr1_final = gr1_final.values.tolist()
###

f=open('/Users/owlting/Downloads/brazilian-ecommerce/myg1.txt','w')
for ot in range(len(gr1_final)):
    #k=' '.join([str(j) for j in i])
    k=str(int(gr1_final[ot][0]))+' 1:'+gr1_final[ot][1][1:8]+' 2:'+gr1_final[ot][2][1:8]+' 3:'+gr1_final[ot][3]+' 4:'+str(gr1_final[ot][4])
    f.write(k+"\n")
f.close()

data = sc.read.format("libsvm")\
    .load("/Users/owlting/Downloads/brazilian-ecommerce/myg1.txt")
splits = data.randomSplit([0.7, 0.3], 1234)
train = splits[0]
test = splits[1]
# specify layers for the neural network:
# input layer of size 4 (features), two intermediate of size 5 and 4
# and output of size 3 (classes)
layers = [4, 5, 4, 4, 3]
# create the trainer and set its parameters
trainer = MultilayerPerceptronClassifier(maxIter=100, layers=layers, blockSize=128, seed=1234)
# train the model
model = trainer.fit(train)
# compute accuracy on the test set
myg1_result = model.transform(test)
predictionAndLabels = myg1_result.select("prediction", "label")
evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
print("Accuracy: " + str(evaluator.evaluate(predictionAndLabels)))
myg1_result.show()

pandas_myg1_result = myg1_result.toPandas()
pandas_myg1_result.to_pickle('/Users/owlting/Downloads/brazilian-ecommerce/myg1')
#myg1_df0715 = pd.read_pickle('/Users/owlting/Downloads/brazilian-ecommerce/myg1')

"""
2-2 pysparkml實作：用運費(f)、價格(p)、地區(g)當作feature以MLP判斷評價(r)
"""
conf=SparkConf().setAppName("miniProject").setMaster("local[*]")
sc=sc.getOrCreate(conf) #可以視情況新建session或使用已有的session
sc = SQLContext(sc)
gr = agg6[['review_score','geolocation_lat','geolocation_lng','price','freight_value','order_purchase_timestamp','order_delivered_customer_date']]
gr = gr.dropna(subset=['freight_value']) #把nan值去掉
gr2 = gr
gr2 = gr2.replace('1','0')
gr2 = gr2.replace('2','1')
gr2 = gr2.replace('3','1')
gr2 = gr2.replace('4','2')
gr2 = gr2.replace('5','2')
gr2 = shuffle(gr2)
gr2 = gr2.values.tolist()

f=open('/Users/owlting/Downloads/brazilian-ecommerce/myg2.txt','w')
for ot in  range(len(gr2)):
    #k=' '.join([str(j) for j in i])
    k=str(int(gr2[ot][0]))+' 1:'+gr2[ot][1][1:8]+' 2:'+gr2[ot][2][1:8]+' 3:'+gr2[ot][3]+' 4:'+gr2[ot][4]
    f.write(k+"\n")
f.close()

data = sc.read.format("libsvm")\
    .load("/Users/owlting/Downloads/brazilian-ecommerce/myg2.txt")
splits = data.randomSplit([0.6, 0.4], 1234)
train = splits[0]
test = splits[1]
# specify layers for the neural network:
# input layer of size 4 (features), two intermediate of size 5 and 4
# and output of size 3 (classes)
layers = [4, 5, 4, 3]
# create the trainer and set its parameters
trainer = MultilayerPerceptronClassifier(maxIter=100, layers=layers, blockSize=128, seed=1234)
# train the model
model = trainer.fit(train)
# compute accuracy on the test set
myg2_result = model.transform(test)
predictionAndLabels = myg2_result.select("prediction", "label")
evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
print("Accuracy: " + str(evaluator.evaluate(predictionAndLabels)))
myg2_result.show()
pandas_myg2_result = myg2_result.toPandas()
pandas_myg2_result.to_pickle('/Users/owlting/Downloads/brazilian-ecommerce/myg2')
#myg2_df0715 = pd.read_pickle('/Users/owlting/Downloads/brazilian-ecommerce/myg2')

"""
3-1 銷售額成長趨勢時間序列(ts)和平均評價趨勢時間序列(ts2)之研究
"""
ts = agg7[['order_purchase_timestamp','price','freight_value','customer_state','seller_state']] 
ts['year_month'] = ts['order_purchase_timestamp'].map(lambda x:x[0:7])
ts=ts.sort_values(by=['year_month'])
ts['price'] = ts['price'].astype(float)
ts_price = ts[['year_month','price']]
group1=ts_price.groupby('year_month')
print(group1.sum())
ts2 = agg7[['order_purchase_timestamp','review_score','freight_value','customer_state','seller_state']] 
ts2['year_month'] = ts2['order_purchase_timestamp'].map(lambda x:x[0:7])
ts2=ts2.sort_values(by=['year_month'])
ts2['review_score'] = ts2['review_score'].astype(int)
ts2_score = ts2[['year_month','review_score']]
group2=ts2_score.groupby('year_month')
print(group2.mean())
#合併至一個表格觀看
ts3 = pd.merge(group1.sum(),group2.mean(), on='year_month')
print(ts3)
#pandas的畫圖功能算是蠻齊全的
ts3.plot(y=['price','review_score'],secondary_y=['review_score'])
#secondary_y為雙座標
#由於最前面三個月後最後一個月資料不夠多，去掉後再畫一次圖
ts3[3:23].plot(y=['price','review_score'],secondary_y=['review_score'])

"""
4-1 評價(r)與字詞(w)分析
"""
rw = agg7[['review_score','review_comment_message']]
rw = rw.dropna(subset=['review_comment_message']) #把nan值去掉
remove=string.punctuation #string.punctuation可得到所有的英文標點符號
table=str.maketrans('','',remove)
rw['review_comment_message_no_punctuation'] = rw['review_comment_message'].map(lambda x:x.translate(table))
rw['review_comment_message_no_punctuation'] = rw['review_comment_message_no_punctuation'].map(lambda x:x.lower())
rw['review_word'] = rw['review_comment_message_no_punctuation'].map(lambda x:x.split(' '))
rw2 = rw[['review_score','review_word']]
rw_group = rw2.groupby('review_score').sum() #把所有word串在一個review_word(list)
bad_review=pd.value_counts(rw_group['review_word'][0])
good_review=pd.value_counts(rw_group['review_word'][4])


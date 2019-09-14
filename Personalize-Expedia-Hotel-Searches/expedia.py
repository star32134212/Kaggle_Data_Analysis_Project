#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 12:48:07 2019

@author: owlting
"""
import pyspark 
from pyspark.sql.functions import pandas_udf

from pyspark import SparkContext as sc
from pyspark import SparkConf
from pyspark.sql import SparkSession
from sklearn.utils import shuffle
import numpy as np 
import pandas as pd 
import seaborn as sb
import random
import matplotlib.pyplot as plt
import sys
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StringIndexer
from pyspark.ml.classification import (DecisionTreeClassifier, RandomForestClassifier, 
                                      GBTClassifier)
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

"""
goal = position, click_bool, gross_bookings_usd, booking_bool
"""
train_data = pd.read_csv('/Users/owlting/Downloads/expedia-personalized-sort/train.csv')  # 讀取訓練數據
test_data = pd.read_csv('/Users/owlting/Downloads/expedia-personalized-sort/test.csv')  # 讀取訓練數據
conf=SparkConf().setAppName("miniProject").setMaster("local[*]")
sc=sc.getOrCreate(conf) #可以視情況新建session或使用已有的session
sc = SQLContext(sc)
"""
一次想訂幾房的分佈
"""
train_data.srch_room_count.unique()
plt.figure(figsize=(8,4))
sb.countplot(x='srch_room_count', data = train_data)
plt.xlabel('room number')
plt.ylabel('count')
plt.show()
"""
是否為連鎖的比例
"""
plt.figure(figsize=(8,4))
sb.countplot(x='prop_brand_bool', data = train_data)
plt.xlabel('brand:1')
plt.ylabel('count')
plt.show()
"""
包含週六的比例
"""
plt.figure(figsize=(8,4))
sb.countplot(x='srch_saturday_night_bool', data = train_data)
plt.xlabel('saturday:1')
plt.ylabel('count')
plt.show()

"""
待幾晚分佈圖
"""
plt.figure(figsize=(8,4))
sb.countplot(x='srch_length_of_stay', data = train_data)
plt.xlabel('night')
plt.ylabel('count')
plt.show()

"""
成人數分佈圖
"""
plt.figure(figsize=(8,4))
sb.countplot(x='srch_adults_count', data = train_data)
plt.xlabel('adults')
plt.ylabel('count')
plt.show()

"""
兒童數分佈圖
"""
plt.figure(figsize=(8,4))
sb.countplot(x='srch_children_count', data = train_data)
plt.xlabel('children')
plt.ylabel('count')
plt.show()

"""
飯店星級分佈圖
"""
plt.figure(figsize=(8,4))
sb.countplot(x='prop_starrating', data = train_data)
plt.xlabel('start rating')
plt.ylabel('count')
plt.show()

"""
各國家飯店數
"""
n, bins, patches = plt.hist(train_data.prop_country_id, 100, density = 1, facecolor='blue', alpha=0.75)
plt.xlabel('Property country Id')
plt.title('Histogram of prop_country_id')
plt.show();

train_data.groupby('prop_country_id').size().nlargest(50).values
train_data.groupby('prop_country_id').size().nsmallest(50).values
#數量差太多

train_data.groupby('visitor_location_country_id').size().nlargest(5)
train_data.groupby('prop_country_id').size().nlargest(1)
#決定除掉這個變因 全用219資料集
train_data_2 = train_data.loc[train_data['visitor_location_country_id'] == 219]


us_visitor = train_data.loc[train_data['visitor_location_country_id'] == 219]
us_visitor['month'] = us_visitor['date_time'].map(lambda x: pd.Timestamp(x).month)
us_visitor['hour'] = us_visitor['date_time'].map(lambda x: pd.Timestamp(x).hour)
us_visitor = us_visitor.sample(frac=0.03, random_state=135)
#random_state 設置種子碼，可以藉由相同種子碼得到相同的抽樣結果
del us_visitor['visitor_location_country_id']
#檢查各行的null值數量
#把null值太多的行刪掉，缺太多對訓練比較沒影響力，還很佔空間
num_count = us_visitor.isnull().sum()
num_count = num_count.sort_values(ascending=False)
print(num_count) #把缺最多值的列找出來
cols_to_drop = ['comp6_rate_percent_diff', 'comp7_rate_percent_diff',\
                'comp1_rate_percent_diff', 'comp4_rate_percent_diff',\
                'comp1_rate', 'comp1_inv', 'comp6_rate', 'comp6_inv',\
                'comp7_rate', 'comp7_inv', 'comp4_rate', 'gross_bookings_usd',\
                'comp4_inv', 'visitor_hist_starrating', 'visitor_hist_adr_usd',\
                'srch_query_affinity_score', 'comp3_rate_percent_diff',\
                'comp2_rate_percent_diff', 'comp8_rate_percent_diff',\
                'comp5_rate_percent_diff', 'comp3_rate', 'comp5_rate',\
                'comp3_inv', 'comp5_inv', 'comp2_rate', 'comp8_rate',\
                'comp2_inv', 'comp8_inv', 'srch_id', 'prop_id' ,'date_time']
#drop srch_id是因為這段數字沒有意義，只是為了分辨每個搜尋結果
#drop prop_id是因為雖然這段數字代表不同飯店，可能有意義，但飯店太多導致數字太多，使這個數字的分布很廣怕影響結果 
us_visitor.drop(cols_to_drop, axis=1, inplace=True)
us_visitor.isnull().sum()


"""
填nan值第一招：隨機填
"""
def randomizeMissingData(df2,col_name): #補隨機值
    "randomize missing data for DataFrame (within a column)"
    df = df2.copy()
    for col in df.columns:
        data = df[col_name]
        mask = data.isnull()
        samples = random.choices( data[~mask].values , k = mask.sum() )
        data[mask] = samples
    return df
#data[~mask]:不看nan值把剩下的值列出
#nan值數量
#samples = random.choices就是把有存在的值中隨機選k個值塞滿所有的nan值(已知nan值有k個 隨機分配)
us_visitor = randomizeMissingData(us_visitor,'prop_review_score')
#us_visitor = randomizeMissingData(us_visitor,'prop_location_score2')

"""
填nan值第二招：填mean值
"""
us_visitor['prop_location_score2'].fillna((us_visitor['prop_location_score2'].mean()), inplace=True)

"""
填nan值第三招：填median值
"""
us_visitor['orig_destination_distance'].fillna((us_visitor['orig_destination_distance'].median()), inplace=True)


bb = us_visitor['booking_bool'].value_counts()
booking_rate = bb[1]/(bb[0]+bb[1])
print('訂房率： '+str(booking_rate*100)[0:4]+'%')
cb = us_visitor['click_bool'].value_counts()
clicking_rate = cb[1]/(cb[0]+cb[1])
print('點擊率： '+str(clicking_rate*100)[0:4]+'%')


box = us_visitor.groupby('click_bool')['price_usd'].describe()
box2 = us_visitor.groupby('booking_bool')['price_usd'].describe()
#相關係數熱度圖
correlation = us_visitor.corr()
plt.figure(figsize=(20, 20))
sb.heatmap(correlation, vmax=1, square=True,annot=True,cmap='viridis')
plt.title('Correlation between different fearures');

us_visitor_df = sc.createDataFrame(us_visitor)
us_visitor_df.printSchema()




assembler = VectorAssembler(inputCols = ['site_id','prop_country_id','prop_starrating',\
                                         'prop_review_score','prop_brand_bool','prop_location_score1',\
                                         'prop_location_score2','prop_log_historical_price',\
                                         'price_usd','promotion_flag','srch_destination_id',\
                                         'srch_length_of_stay','srch_booking_window','srch_adults_count',\
                                         'srch_children_count','srch_room_count','srch_saturday_night_bool',\
                                         'orig_destination_distance','random_bool','month','hour'], outputCol = 'features')

#assembler可以把特徵值拼成一個向量
output = assembler.transform(us_visitor_df)
"""
 |-- features: vector (nullable = true) #多了一個feature vector
"""

"""
model
"""
def train_model(x,y):
    final_traindata = output.select(x, y)
    train, test = final_traindata.randomSplit([0.7, 0.3])
    dt = DecisionTreeClassifier(labelCol = y, featuresCol = x)
    rf = RandomForestClassifier(labelCol = y, featuresCol = x)
    gb = GBTClassifier(labelCol = y, featuresCol = x)      
    dt_model = dt.fit(train)
    rf_model = rf.fit(train)
    gb_model = gb.fit(train)
    dt_predictions = dt_model.transform(test)
    rf_predictions = rf_model.transform(test)
    gb_predictions = gb_model.transform(test)
    
    binary_evaluator = BinaryClassificationEvaluator(labelCol = y)
    print('BinaryClassificationEvaluator')
    print('Decision Tree:', binary_evaluator.evaluate(dt_predictions))
    print('Random Forest:' , binary_evaluator.evaluate(rf_predictions))
    print('Gradient-boosted Trees:', binary_evaluator.evaluate(gb_predictions))
    #multiclass效果好很多
    multi_evaluator = MulticlassClassificationEvaluator(labelCol = y, metricName = 'accuracy')
    print('MulticlassClassificationEvaluator')
    print('Decision Tree Accu:', multi_evaluator.evaluate(dt_predictions))
    print('Random Forest Accu:', multi_evaluator.evaluate(rf_predictions))
    print('Gradient-boosted Trees Accu:', multi_evaluator.evaluate(gb_predictions))

"""
clicking
"""
train_model('features', 'click_bool')

"""
booking
"""
train_model('features', 'booking_bool')

"""
position
"""
def train_model_2(x,y):
    final_traindata = output.select(x, y)
    train, test = final_traindata.randomSplit([0.7, 0.3])
    dt = DecisionTreeClassifier(labelCol = y, featuresCol = x)
    rf = RandomForestClassifier(labelCol = y, featuresCol = x)
    dt_model = dt.fit(train)
    rf_model = rf.fit(train)
    dt_predictions = dt_model.transform(test)
    rf_predictions = rf_model.transform(test)
    
    multi_evaluator = MulticlassClassificationEvaluator(labelCol = y, metricName = 'accuracy')
    print('MulticlassClassificationEvaluator')
    print('Decision Tree Accu:', multi_evaluator.evaluate(dt_predictions))
    print('Random Forest Accu:', multi_evaluator.evaluate(rf_predictions))


train_model_2('features', 'position')
    
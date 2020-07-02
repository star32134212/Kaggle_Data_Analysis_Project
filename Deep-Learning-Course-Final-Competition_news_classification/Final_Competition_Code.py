# -*- coding: utf-8 -*-
"""Kaggle.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A47efUNVTsrXKHvo_PKOSWl3kd1y5qd7
"""

#!pip3 install opencc-python-reimplemented

# check device driver
#!nvidia-smi

import numpy as np
import pandas as pd
from opencc import OpenCC
from collections import defaultdict
import jieba
import jieba.posseg as pseg
import jieba.analyse



cc = OpenCC('t2s')
data_train = pd.read_csv('./train_data.csv')  
data_test = pd.read_csv('./test_data.csv')  
data_train = data_train[['label','title','keyword']]

"""娛樂 news_entertainment 0  
體育 news_sports 1  
房產 news_house 2  
汽車 news_car 3  
教育 news_edu 4   
科技 news_tech 5  
軍事 news_military 6  
國際 news_world 7  
農業 news_agriculture 8  
電競 news_game 9
"""

def class2word(label):
  class_list = ['娛樂','體育','房產','汽車','教育','科技','軍事','國際','農業','電競']
  return class_list[label]

def get_keyword_and_insert(sentence,classpool):    
    ws = jieba.analyse.extract_tags(sentence, topK=5)
    for i in ws:
      classpool[i] = classpool[i] + 1
            
def insert_pool(keyword_string,classpool):
    #else:
    #print(keyword_string)
    try :
      keyword_list = keyword_string.split(',')
      for word in keyword_list:
        classpool[word] = classpool[word] + 1
    except AttributeError:
      pass
  
def make_class_pool(data,label_num,classpool):
    given_data = data[data.label == label_num]
    given_data.keyword = given_data.keyword.apply(lambda x: insert_pool(x,classpool)) 
    given_data.title = given_data.title.apply(lambda x: get_keyword_and_insert(x,classpool)) 
    #return classpool

def acc_cal(label,predict):
  if(label == predict):
    return 1
  else:
    return 0

"""```
# This is formatted as code
```

predict version 2 有做normalization
"""

def predict(news, w1, w2, analysis, top):
  #print(news.title)
  ws = jieba.analyse.extract_tags(news.title, topK=top)
  count0 = 0
  count1 = 0
  count2 = 0
  count3 = 0
  count4 = 0
  count5 = 0
  count6 = 0
  count7 = 0
  count8 = 0  
  count9 = 0  
  weight_ws = w1 
  weight_kw = w2
  for word in ws:
    word_dis = distribution_return_2(word)
    word_dis_act = normalization(word_dis)
    count0 = count0 + word_dis_act[0] * weight_ws
    count1 = count1 + word_dis_act[1] * weight_ws
    count2 = count2 + word_dis_act[2] * weight_ws
    count3 = count3 + word_dis_act[3] * weight_ws
    count4 = count4 + word_dis_act[4] * weight_ws
    count5 = count5 + word_dis_act[5] * weight_ws
    count6 = count6 + word_dis_act[6] * weight_ws
    count7 = count7 + word_dis_act[7] * weight_ws
    count8 = count8 + word_dis_act[8] * weight_ws
    count9 = count9 + word_dis_act[9] * weight_ws
  try :
      kw_list = news.keyword.split(',')
      for word in kw_list:
        word_dis = distribution_return_2(word)
        if(sum(word_dis) != 0):
          word_dis_act = normalization(word_dis)
        else:
          word_dis_act = word_dis
        count0 = count0 + word_dis_act[0] * weight_kw
        count1 = count1 + word_dis_act[1] * weight_kw
        count2 = count2 + word_dis_act[2] * weight_kw
        count3 = count3 + word_dis_act[3] * weight_kw
        count4 = count4 + word_dis_act[4] * weight_kw
        count5 = count5 + word_dis_act[5] * weight_kw
        count6 = count6 + word_dis_act[6] * weight_kw
        count7 = count7 + word_dis_act[7] * weight_kw
        count8 = count8 + word_dis_act[8] * weight_kw
        count9 = count9 + word_dis_act[9] * weight_kw
  except AttributeError:
    result = [count0,count1,count2,count3,count4,count5,count6,count7,count8,count9]
    if(analysis == 0):
      return result.index(max(result))
    else:
      return result
  result = [count0,count1,count2,count3,count4,count5,count6,count7,count8,count9]
  if(analysis == 0):
    return result.index(max(result))
  else:
    return result

"""建分類文本字典"""

classpool0 = defaultdict(lambda: 0.0)
classpool1 = defaultdict(lambda: 0.0)
classpool2 = defaultdict(lambda: 0.0)
classpool3 = defaultdict(lambda: 0.0)
classpool4 = defaultdict(lambda: 0.0)
classpool5 = defaultdict(lambda: 0.0)
classpool6 = defaultdict(lambda: 0.0)
classpool7 = defaultdict(lambda: 0.0)
classpool8 = defaultdict(lambda: 0.0)
classpool9 = defaultdict(lambda: 0.0)
make_class_pool(data_train,0,classpool0)
make_class_pool(data_train,1,classpool1)
make_class_pool(data_train,2,classpool2)
make_class_pool(data_train,3,classpool3)
make_class_pool(data_train,4,classpool4)
make_class_pool(data_train,5,classpool5)
make_class_pool(data_train,6,classpool6)
make_class_pool(data_train,7,classpool7)
make_class_pool(data_train,8,classpool8)
make_class_pool(data_train,9,classpool9)

total_value0 = sum(classpool0.values())
total_value1 = sum(classpool1.values())
total_value2 = sum(classpool2.values())
total_value3 = sum(classpool3.values())
total_value4 = sum(classpool4.values())
total_value5 = sum(classpool5.values())
total_value6 = sum(classpool6.values())
total_value7 = sum(classpool7.values())
total_value8 = sum(classpool8.values())
total_value9 = sum(classpool9.values())
print("total_value0",total_value0)
print("total_value1",total_value1)
print("total_value2",total_value2)
print("total_value3",total_value3)
print("total_value4",total_value4)
print("total_value5",total_value5)
print("total_value6",total_value6)
print("total_value7",total_value7)
print("total_value8",total_value8)
print("total_value9",total_value9)

def distribution(word): #查看各分類次數分佈
  print (classpool0[word],classpool1[word],classpool2[word],classpool3[word],classpool4[word],classpool5[word],classpool6[word],classpool7[word],classpool8[word],classpool9[word])

def distribution_return(word): #交給後面的normalization
  distribution_list = []
  distribution_list.append(classpool0[word])
  distribution_list.append(classpool1[word])
  distribution_list.append(classpool2[word])
  distribution_list.append(classpool3[word])
  distribution_list.append(classpool4[word])
  distribution_list.append(classpool5[word])
  distribution_list.append(classpool6[word])
  distribution_list.append(classpool7[word])
  distribution_list.append(classpool8[word])
  distribution_list.append(classpool9[word])
  return distribution_list

def distribution_return_2(word): #除以pool的value total
  distribution_list = []
  distribution_list.append(classpool0[word]/total_value0)
  distribution_list.append(classpool1[word]/total_value1)
  distribution_list.append(classpool2[word]/total_value2)
  distribution_list.append(classpool3[word]/total_value3)
  distribution_list.append(classpool4[word]/total_value4)
  distribution_list.append(classpool5[word]/total_value5)
  distribution_list.append(classpool6[word]/total_value6)
  distribution_list.append(classpool7[word]/total_value7)
  distribution_list.append(classpool8[word]/total_value8)
  distribution_list.append(classpool9[word]/total_value9)
  return distribution_list

def news_analysis(news): #分析單篇新聞模型的推理過程
  confused_list = predict(news,1,10,1,5)
  predict_label = predict(news,1,10,0,5)
  ws_2 = jieba.analyse.extract_tags(news.title, topK=5)
  print('title:',news.title)
  print(ws_2)
  for w in ws_2:
    word_dis = distribution_return(w)
    if(sum(word_dis) != 0):
      word_dis_act = normalization(word_dis)
    else:
      word_dis_act = word_dis
    print(word_dis_act)
  print('keyword:',news.keyword)
  try:
    kw_list = news.keyword.split(',')
    for w in kw_list:
      word_dis = distribution_return(w)
      if(sum(word_dis) != 0):
        word_dis_act = normalization(word_dis)
      else:
        word_dis_act = word_dis
      print(word_dis_act) 
  except AttributeError:
    pass
  print('label:',news.label, class2word(news.label))
  print('predict:',predict_label, class2word(predict_label))
  print(confused_list)

def normalization(distribution_list):
  if(sum(distribution_list)==0):
    return distribution_list
  else:
    total = sum(distribution_list)
    normal = [round(x / total,3) for x in distribution_list]
    return normal

"""拿train_data 測試"""

acc_count = 0
samp = 5000
test = data_train.sample(samp)
test['predict'] = test.apply(lambda x: predict(x,w1=1,w2=1,analysis=0,top=10), axis=1)
test['true'] = test.apply(lambda x: acc_cal(x.label,x.predict), axis=1)
data_f = test[test.true == 0]
#n=88
#print(test.iloc[n])
#print(predict(test.iloc[n]))
acc = list(test.true)
print('accuracy:',sum(acc)/samp)
data_f["true"] = 1

"""分析答錯的新聞"""

for i in range(31,80):
  news_analysis(data_f.iloc[i])

recorrect_matrix = np.zeros((10,10))
for i in range(len(data_f)):
  recorrect_matrix[int(data_f.iloc[i].label),int(data_f.iloc[i].predict)] = recorrect_matrix[int(data_f.iloc[i].label),int(data_f.iloc[i].predict)] + 1
print("confused_matrix")
print(recorrect_matrix)
#label=row predict=column
#6 7容易搞混

"""testing data and save result"""

data_test['label'] = data_test.apply(lambda x: predict(x, w1=1, w2=1, analysis=0, top=10), axis=1)
data_test_final = data_test[['id','label']]
data_test_final.to_csv('answer.csv',header=1,index=0)

"""text data 59908 筆  
娛樂 0 / 體育 1  
房產 2 / 汽車 3  
教育 4 / 科技 5  
軍事 6 / 國際 7  
農業 8 / 電競 9
"""
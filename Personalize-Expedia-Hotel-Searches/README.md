# Personalize-Expedia-Hotel-Searches
Expedia訂房資料分析，由於是ICDM 2013，網路上有許多大佬的實作，學到了很多技巧。  
這份Expedia資料只算Train_data就有九百多萬筆，資料清洗上有蠻多東西可以學的，算是將一些新學到的東西整理成一份筆記。  
# Dataset
Kaggle : https://www.kaggle.com/c/expedia-personalized-sort/overview    
這份資料集將資料分成Train與test兩部份，希望Train_data預測使用者：  
想去的地點(position),是否會點擊飯店(click_bool), 訂房的花費(gross_bookings_usd),是否會訂房(booking_bool)  
# Data Description
srh_id 使用者的搜尋動作 應該可以判斷人  
date_time 搜尋的時間點  
site_id 使用者所用的site  (i.e. Expedia.com, Expedia.co.uk, Expedia.co.jp, ..)  
visitor_location_country_id 客戶所在國家  
visitor_hist_starrating  使用者以往選的飯店星級 沒有則為0  
visitor_hist_adr_usd 使用者以往選的飯店平均價格 沒有則為0  
prop_country_id 飯店所在國家id  
prop_id 飯店id  
prop_starrating 飯店星級  
prop_review_score 飯店平均評價  
prop_brand_bool 飯店是否有品牌(1為連鎖 0為單獨 )  
prop_location_score1 飯店位置的評分  
prop_location_score2 飯店位置的評分ver 2  
prop_log_historical_price 過去某一段時間的某飯店平均價格的對數 (0代表沒在訂單)  
Position 搜尋頁上飯店所在位置代碼 只有train有 test沒有  
Price_usd 某個搜尋結果的顯示價格，可能因不同城市的稅或所選的時間長短有異  
promotion_flag 有無促銷 1/0  
gross_booking_usd 總共所花的金額，會受税或其他條件影響  
srch_destination_id 使用者搜尋的目的地id  
srch_length_of_stay 待多少晚  
srch_booking_window  -Number of days in the future the hotel stay started from the search date  
srch_adults_count 成人數量  
srch_children_count 兒童數量  
srch_room_count 使用者搜尋房間數  
srch_saturday_night_bool 是否包含週六晚上     
srch_query_affinity_score 飯店會在搜尋頁被點擊的機率曲log  
orig_destination_distance 客戶到飯店的物理距離  
random_bool  1代表隨機排序 	0代表有sort  
comp1_rate 1代表Expedia 比其他競爭者便宜 0一樣 -1比較貴  
comp1_inv 1代表競爭者沒有房間存貨 0代表競爭者和E都有存貨  
comp1_rate_percent_diff E和競爭者各自提供價格之差距百分比  
# Statistical Data
客戶訂的房間類型分佈：  
<img width="600" height="350" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Personalize-Expedia-Hotel-Searches/img/room_type.png"/>  
單人房數量最多，其次是雙人房。  
  
飯店是否為有品牌的連鎖飯店：  
<img width="600" height="350" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Personalize-Expedia-Hotel-Searches/img/brand.png"/>   
  
住宿是否包含週六晚上：  
<img width="600" height="350" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Personalize-Expedia-Hotel-Searches/img/saturday.png"/>  
  
住宿天數分佈：  
<img width="600" height="350" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Personalize-Expedia-Hotel-Searches/img/night.png"/>
  
成人與小孩數量：  
<img width="400" height="240" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Personalize-Expedia-Hotel-Searches/img/adults.png"/>
<img width="400" height="240" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Personalize-Expedia-Hotel-Searches/img/children.png"/>   
  
飯店星級分佈：  
<img width="600" height="350" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Personalize-Expedia-Hotel-Searches/img/star_rating.png"/>   


點擊/訂房與價格的關係：
   
|              | mean          |  min          | max           | 25%           |        50%    | 75%           |
| :----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: | :-----------: |
| **click**    | 136.336       |17             |1945           |82             |112            |161            |
| **booking**  | 124.914       | 22            |1051           |80             |109            |151            |  

訂房率:2.90%   
點擊率:4.40%  
  
# Data Preprocessing
這份資料集的資料非常多，因此需要篩選和清洗比較好分析。
下圖為各飯店所在國家分佈：  
<img width="600" height="350" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Personalize-Expedia-Hotel-Searches/img/property_country_id.png"/>   
由圖可知編號219的國家遠超過其他國家，雖然只有代碼沒有國家名，但可以合理猜測219是指美國，如果將研究客群鎖定在美國就可以少一個變數了。  
因此決定只取編號為219的資料。即使只取219，還是有570多萬筆資料，因此先從中隨機抽樣5%做研究比較好操控：  
  
```
us_visitor = train_data.loc[train_data['visitor_location_country_id'] == 219]
us_visitor = us_visitor.sample(frac=0.05, random_state=123)
```  
這裡的random_state是指種子，可以指定一數字，下次若想得到相同的sample結果可以用同樣的random_state得到。  
接著將各column的nan值數量列出來，將nan值太多(超過9成)的column直接刪掉，這些column相對沒有參考性。   

```
cols_to_drop = ['comp6_rate_percent_diff', 'comp7_rate_percent_diff',\  
                'comp1_rate_percent_diff', 'comp4_rate_percent_diff',\  
                'comp1_rate', 'comp1_inv', 'comp6_rate', 'comp6_inv',\  
                'comp7_rate', 'comp7_inv', 'comp4_rate', 'gross_bookings_usd',\  
                'comp4_inv', 'visitor_hist_starrating', 'visitor_hist_adr_usd',\  
                'srch_query_affinity_score', 'comp3_rate_percent_diff',\  
                'comp2_rate_percent_diff', 'comp8_rate_percent_diff',\  
                'comp5_rate_percent_diff', 'comp3_rate', 'comp5_rate',\  
                'comp3_inv', 'comp5_inv', 'comp2_rate', 'comp8_rate',\  
                'comp2_inv', 'comp8_inv', 'srch_id', 'prop_id']  
us_visitor.drop(cols_to_drop, axis=1, inplace=True)  
```

剩下的column還是有nan值，網路上有三種主要的處理nan值方法。  

#### 第一種：補隨機值  
```
def randomizeMissingData(df2,col_name): 
    "randomize missing data for DataFrame (within a column)"
    df = df2.copy()
    for col in df.columns:
        data = df[col_name]
        mask = data.isnull()
        samples = random.choices( data[~mask].values , k = mask.sum() )
        data[mask] = samples
    return df
    
us_visitor = randomizeMissingData(us_visitor,'prop_review_score')
```
將評價分數補隨機值，[random.choices](https://docs.python.org/zh-cn/3/library/random.html "random.choices")會從同columns有存在的值隨機選一個補到空值，每個nan值都做一次這樣的動作，因此每個nan值補的也不一樣。  
  
#### 第二種：統一補平均值  
```
us_visitor['prop_location_score2'].fillna((us_visitor['prop_location_score2'].mean()), inplace=True)
```
將飯店位置分數補平均值，fillna這個方法可以統一幫所有nan值補上一特定值。
   
#### 第三種：統一補中值  

```
us_visitor['orig_destination_distance'].fillna((us_visitor['orig_destination_distance'].median()), inplace=True)
```

將使用者與飯店物理距離的nan值補中值。 
使用下面這段code可以看到目前所有feature互相的相關係數，藉由這個方式可以先初步知道哪些特徵較重要。  

```
correlation = us_visitor.corr()
plt.figure(figsize=(18, 18))
sb.heatmap(correlation, vmax=1, square=True,annot=True,cmap='viridis')
plt.title('Correlation between different fearures');
```

<img width="1200" height="700" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Personalize-Expedia-Hotel-Searches/img/correlation.png"/>   
然後直接將pandas處理好的dataframe轉成RDD

```
us_visitor_df = sc.createDataFrame(us_visitor)
us_visitor_df.printSchema()
```

<img width="600" height="350" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Personalize-Expedia-Hotel-Searches/img/printSchema.png"/>   
以上這些是用來預測的特徵。  
  
 ```
from pyspark.ml.feature import VectorAssembler  
assembler = VectorAssembler(inputCols = ['site_id','prop_country_id','prop_starrating',\
                                         'prop_review_score','prop_brand_bool','prop_location_score1',\
                                         'prop_location_score2','prop_log_historical_price',\
                                         'price_usd','promotion_flag','srch_destination_id',\
                                         'srch_length_of_stay','srch_booking_window','srch_adults_count',\
                                         'srch_children_count','srch_room_count','srch_saturday_night_bool',\
                                         'orig_destination_distance','random_bool'], outputCol = 'features')
output = assembler.transform(us_visitor_df)
```
[VectorAssembler](https://www.bookstack.cn/read/spark-ml-source-analysis/%E7%89%B9%E5%BE%81%E6%8A%BD%E5%8F%96%E5%92%8C%E8%BD%AC%E6%8D%A2-VectorAssembler.md "VectorAssembler"):可以把選定的column每行組合成一個vector，建一個'vector'的column來存它。  

# Decision tree
### Decision Tree
可以看成一個包含多個is-else規則的樹，每次分割時將空間一分為二，每個子結點都是在空間中一個符合特定條件的區域，藉由分類這些子節點的類別來進行分類，因此可將新進來的特徵分到某個空間已得到他的分類。  
### Random Forest
隨機森林是由多個決策樹組成，比起深度學習去訓練出一個聰明的模型，隨機森林更像是許多不特別聰明的樹(弱分類器)藉由投票的方式來組成一個聰明的模型，前者算是聰明的領導，後者算是眾人的智慧。  
隨機森林有許多優點(列出幾種 from wiki)：  
  (1)對於很多種不同資料，它可以產生高準確度的分類器。  
  (2)它可以處理大量的輸入變數。  
  (3)它可以在決定類別時，評估該變數的重要性。  
  (4)對於不平衡的分類資料集來說，它可以平衡誤差。  
### Gradient Boosting Tree
Boosting的宗旨是對於一份數據，想建立M個模型來預測，每個模型都會將上一個模型分類錯的樣本權重增加，因此越往後的模型，就會越在意那些容易分錯的點，最終跑出第M個模型就會是集前(M-1)個模型的經驗得到一個最不容易出錯的模型。Gradient Boosting是指每次新建立的模型都會在前一個模型的梯度下降方向上，確保新的模型正在往理想模型的方向上前進。  
<img width="600" height="350" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Personalize-Expedia-Hotel-Searches/img/GBT.png"/>  
# Experimental Result
```
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
    multi_evaluator = MulticlassClassificationEvaluator(labelCol = y, metricName = 'accuracy')
    print('MulticlassClassificationEvaluator')
    print('Decision Tree Accu:', multi_evaluator.evaluate(dt_predictions))
    print('Random Forest Accu:', multi_evaluator.evaluate(rf_predictions))
    print('Gradient-boosted Trees Accu:', multi_evaluator.evaluate(gb_predictions))
```
  
## 加入時間特徵
每筆搜尋紀錄都有時間，因此也可以拿到點擊與訂房時間，將時間處理成月份和小時加入特徵。  
EX: 2013-01-02 22:19:08可以變成 'month'=1,'hour'=22  
<img width="1200" height="700" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Personalize-Expedia-Hotel-Searches/img/correlation2.png"/>   
  
## click_bool預測
#### BinaryClassificationEvaluator
Decision Tree: 0.3944454794484771  
Random Forest: 0.6434133684320116  
Gradient-boosted Trees: 0.6860335396253086  
#### MulticlassClassificationEvaluator
Decision Tree Accu: 0.9567206057577737  
Random Forest Accu: 0.9567206057577737  
Gradient-boosted Trees Accu: 0.9567590421647384  
  
## booking_bool預測  
#### BinaryClassificationEvaluator
Decision Tree: 0.6138461037007714  
Random Forest: 0.7104042384060483  
Gradient-boosted Trees: 0.7527170635842483  
#### MulticlassClassificationEvaluator
Decision Tree Accu: 0.9717008429946565  
Random Forest Accu: 0.9717201334902293  
Gradient-boosted Trees Accu: 0.9717394239858022  
  
## position預測  
  
position分佈：  
<img width="600" height="350" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Personalize-Expedia-Hotel-Searches/img/position.png"/>  

#### MulticlassClassificationEvaluator
Decision Tree Accu: 0.05192013478707128  
Random Forest Accu: 0.05075817727598427  
  

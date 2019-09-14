# Brazilian-ECommerce-Analysis
Brazilian-ECommerce-Analysis by pyspark and pandas
# Dataset
先到Kaggle上把"Brazilian E-Commerce Public Dataset by Olist"這份dataset載下來並放到同個資料夾中，這是一份來自巴西的公開電商資料。  
Kaggle：https://www.kaggle.com/olistbr/brazilian-ecommerce
# section 0-讀取資料
使用pd.merge把需要的數據整合到同個表格中，將合併前的表格也留下來，因為不是每次都會用到最大的表格(agg7)。  
要特別注意的是在"olist_geolocation_dataset"這個資料集裡，並沒有primary key，同一個prefix可能有多個經緯度，是一對多的關係，因此使用drop_duplicates(subset=['customer_zip_code_prefix'], keep='first')，只保留最先得到的prefix數據，將同個prefix碼的經緯度統一。
# section 1-統計法:巴西各地區商品類別推薦
依據巴西的27州分類，統計每州的訂單數量和購買哪一種類商品的訂單最多。  
各州的訂單數量：  
<img width="490" height="350" src="https://github.com/star32134212/Brazilian-ECommerce-Analysis/blob/master/img/customer_state_data.png"/>  
前三名分別為  
SP:聖保羅  
RJ:里約熱內盧  
MG:美景  
聖保羅最常購買的種類：  
<img width="490" height="350" src="https://github.com/star32134212/Brazilian-ECommerce-Analysis/blob/master/img/favorate_category_SP.png"/>  

前三名分別為bed_bath_table,health_beauty,sport_leisure  
# section 2-1-sparkml實作：以運費(f)、耗時(d)、地區(g)當作feature用MLP判斷評價(r)
主要有三個筆記：  
(1)pandas有Timestamp可以處理時間資料，將客戶下訂單到收到貨物的時間算出(d)，詳細操作可以參考這篇：https://ek21.com/news/tech/28706/  
(2)因為希望可以把處理好的訓練資料保留，將資料處理好後寫入txt檔再用read.format("libsvm")的形式讀取，它會把資料讀成適合訓練的形式。  
(3)spark的MLP分類器是從0開始的，因此必須有一類的label是0，原本的label是評價1~5分，但由於1和5的評分特別多筆，因此合併剩下的評價，將1視為class 0，將2,3視為class 1，，將4,5視為class 2，分成三類，acc為0.8073。0和2的比例佔大多數，因此模型不會考慮class 1。  
<img width="490" height="350" src="https://github.com/star32134212/Brazilian-ECommerce-Analysis/blob/master/img/train_outcome.png"/> 
# section 2-2-sparkml實作：以運費(f)、價格(p)、地區(g)當作feature用MLP判斷評價(r)
基本上操作同2-1。  
由於這份dataset的評分大多都是1或5，因此即使調整層數或其他參數，對acc幾乎沒有影響，他只會預測class 0或class 1的答案。
# section 3-銷售額成長趨勢時間序列(ts)和平均評價趨勢時間序列(ts2)之研究
將每個月的銷售額和平均評價列出來。  
<img width="490" height="350" src="https://github.com/star32134212/Brazilian-ECommerce-Analysis/blob/master/img/price_review.png"/>  
由於頭尾月的統計資料不夠多，上圖是去掉頭三個月和尾一個月的結果，時間為2017-01~2018-08。
# section 4-評價(r)與字詞(w)分析
希望統計評分為1和評分為5的回饋中，字詞出現的次數。  
扣掉單純的稱讚和批評詞後，發現運送時間是決定評價的一大因素。  
# conclusion
(1)資料量不多且過於集中某幾類，其實不太需要用到MLP，統計資料比較直觀。  
(2)巴西的城鄉差距大，大部分的訂單集中在大都市，不同州較熱門的種類其實差不多。  
(3)整體來看營業額是越來越多，且跟評價的關係不大。  
(4)從字詞分析中可以發現，影響使用者評分的最大因素是運送時間，回饋中字詞扣掉純正反面和連接詞等，最常出現的是運送時間、送出、收到等詞。

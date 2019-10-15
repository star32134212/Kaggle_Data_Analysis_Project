# Airbnb-Bookings-Data-Analysis
最近接觸訂房資料集，跟網路零售比較大的差別是資料比較不是著重在商品的描述(房間)，對於客戶的個人資料會比零售商多一點，但畢竟是公開資料，所以也沒有到很詳細，需要一些想像力從有限的資料中挖掘出有用的特徵。
# Dataset  
這是一份airbnb的公開訂房資料，下載到與python檔同個資料夾就可以跑了。  
Kaggle：https://www.kaggle.com/c/airbnb-recruiting-new-user-bookings  
這份資料集將資料分成Train與test兩部份，Train的部分有客戶將要去的目的地，test資料則沒有，放到Kaggle上讓大家試著從新客戶的資料去預測新客戶想要去的國家。
# Data Description
date_account_created:客戶創帳號的時間點。  
timestamp_first_active:帳號第一次使用的時間點。(幾乎與創帳號同時，除非創完帳號直接關掉不登入)  
data_first_booking:客戶第一次訂房的時間點。  
gender:客戶性別('-unknown-','other','MALE','FEMALE')  
age:客戶年齡。   
signup_method:客戶登入帳號的方式。  
language:客戶使用語言，幾乎都是英語。  
signup_app:客戶使用的平台。 
signup_flow:客戶在第幾頁訂房。  
first_device_type:客戶使用的設備。  
first_browser:客戶使用的瀏覽器。  
country_destination:客戶的目的地，也就是要預測的lebal。(其中NDF為沒有紀錄)  
另外還有一個Sessions資料表，我覺得資料很雜所以沒用。  
# Statistical Data
這次使用了python的[[seaborn]](https://seaborn.pydata.org "seaborn")函式庫覺得還不錯用，是畫圖表的好工具。


### 各國旅客數統計  
美國的旅客遠遠超過其他國家  
<img width="490" height="350" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Airbnb-Bookings-Data-Analysis/image/destination%20.png"/>  
### 登入方式統計  
大部分的客戶還是以直接登入為主，有部分靠Facebook,Google登入  
<img width="490" height="350" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Airbnb-Bookings-Data-Analysis/image/signup_method.png"/>  
### 各國使用裝置統計  
可以看到用網路訂房的人遠遠超過用手機來訂，可以知道大家比較傾向於在家用電腦規劃行程，而不是用手機。  
<img width="490" height="350" src="https://github.com/star32134212/Airbnb-Bookings-Data-Analysis/blob/master/image/signup_app.png"/>
### 年齡分佈
先使用 users['age'].describe() 看看一些基本的統計資料。  
count：158681.00  
mean：47.14  
std：142.62  
min：1.00  
25%：28.00  
50%：33.00  
75%：42.00  
max：2014.00  
很明顯2014和1歲是不可能的，2014應該是把年份填錯格，1可能是少打一個位數就送出。  
將統計範圍設定在15-100歲可得到下面的分佈圖，由圖可知使用airbnb訂房的人大都落在20-40歲的區間。   
<img width="490" height="350" src="https://github.com/star32134212/Kaggle_Data_Analysis_Project/blob/master/Airbnb-Bookings-Data-Analysis/image/age.png"/>  
### 進階數據
前面的部分是從資料表中的資料去做統計，接著我從上面有的資料算出一些可能有用的進階數據。  
#### 對airbnb的搜尋結果滿意程度
此數據是統計有辦帳號的客戶最後有訂房的比率有多少，我們可以將客戶辦airbnb帳戶的行為視為客戶有出去玩的動機，因此開始做旅遊規劃，客戶不會只看airbnb這個訂房網站，還有如booking,agoda,trivago等訂房比價網站可以使用，此數據我覺得可以視為客戶看了airbnb的搜尋結果後發現滿意的房間而訂房的一個指標。  
  
註冊完會訂房的比率 = 67.73%    
#### 旅遊規劃平均天數
此數據是算出客戶註冊完帳號到訂房所差的天數，在決定要去旅遊後，使用者辦了訂房網站的帳號打算找到適合的房間，等到確定行程後他會把之前由查到的房間訂下來，這兩個時間點的差也許可以視為客戶旅遊規劃的天數。  
   
註冊完到訂房時間平均天數 = 44.41天  
####  參考頁數
在設定好搜尋條件後，可以看到符合條件的房間，於是我統計了使用者會在第幾頁看到滿意的房間，可作為airbnb搜尋系統是否完善的參考。也可以當作是現在使用者對房間的考慮程度大概有多少，會看多少頁的結果才下決定。
  
找到滿意的房間平均看的頁數 = 4.29頁  
4.29頁算還蠻多的，後來發現由於有很多使用者使用的是手機訂房，手機一頁能顯示的房間數較少，所以頁數會比較多，於是只統計Web的結果，得到了平均0.32頁的結果，代表使用者通常可以在前兩頁就找到滿意的房間(第一頁的搜尋結果算是0)
  
使用Web平均在第幾頁找到想要的房間 = 0.32頁
#### 旅遊旺季
由於訂房的客戶剛好都是北半球，於是我以1到3月當冬季、4到6月當春季、7到9月當夏季、10到12月當冬季統計每個季節的旅客人數。  
由下表可知，春季和冬季出去旅遊的人數較多。  
<img width="490" height="350" src="https://github.com/star32134212/Airbnb-Bookings-Data-Analysis/blob/master/image/season.png"/>
# Data Preprocessing
看了所有的資料，決定用性別、年齡、訂房季節來預測目的地，其他的資料不是太偏某個值就是跟目的地搭不上關係。  
性別把女性當作2、男性當作1、其他當作0做前處理。
年齡扣掉極端值只用15~100算，超過範圍的用15或100補。
季節春夏秋冬依序用2341替換。
# Experimental Result
使用pyspark.ml的MLP來進行分類：  
layers=<3,5,4,6,12>  
epochs=200  
blocksize=256  
<img width="360" height="240" src="https://github.com/star32134212/Airbnb-Bookings-Data-Analysis/blob/master/image/label_encoder.png"/>
<img width="360" height="240" src="https://github.com/star32134212/Airbnb-Bookings-Data-Analysis/blob/master/image/result_1.png"/>  
由於NDF和US佔大多數導致模型幾乎都猜這兩個也能得到比較低的loss，這樣的預測其實幫助不大。  
# Experimental Result ver 2.0
已知US佔大多數，DNF和other沒有用，把這些去除掉後可以得到剩下國家的分佈。  
<img width="490" height="350" src="https://github.com/star32134212/Airbnb-Bookings-Data-Analysis/blob/master/image/destination_ver2.png"/>  
layers=<3,5,4,4,4,6,9>  
epochs=200  
blocksize=256  
expect USA,NDF,other  
<img width="360" height="240" src="https://github.com/star32134212/Airbnb-Bookings-Data-Analysis/blob/master/image/label_encoder2.png"/>
<img width="360" height="240" src="https://github.com/star32134212/Airbnb-Bookings-Data-Analysis/blob/master/image/result_2.png"/>  
這次換幾乎都猜法國了...資料數量差距太大加上能拿來預測的feature過少都是問題。  
# Conclusion
(1)訂房資料對帳戶的特徵有比較多feature，但這分資料即能用來判斷的特徵仍然不夠，統計法可以得到更直觀的結果。  
(2)可以嘗試用更好的演算法或是將一些過多資料的label刪減掉一些讓每個label數目較接近。  
(3)進階數據可以得到一些蠻有趣的指標。





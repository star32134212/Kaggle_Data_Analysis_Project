數據棒球(3)-Money Ball
===
Money Ball一書於2003年出版，講述的是運動家隊的總經理Billy Beane於1999年挖角了印地安人隊的總經理助理Paul DePodesta，兩人用統計數據分析球員，打造出一支讓當時球探無法理解的球隊，例如以上壘率取代當時主流判定打擊者好壞的打擊率，或是選擇雖然常投出保送，但也很多三振的投手，這類有明顯缺點的球員在市場上普遍不貴，是當時球探比較不會看好的球員，只要搭配得宜，也能有意想不到的效果，而這支以數據分析打造出的運動家隊在2002年打出了破美聯紀錄的20連勝。  
![](https://i.imgur.com/zARJEom.jpg)

在電影中，Billy Beane在去印地安人隊談球員交易的過程中，認識了喜歡用數據分析球員的Peter Brand，當時他是印地安人隊的一個小助理，
Billy Beane馬上把他挖角來運動家隊，並給予他很大的信任，讓他以數據分析取代原本的球探們，電影中的設定，Peter Brand是一個從耶魯大學經濟學系畢業的胖子，而這個角色其實是以Paul DePodesta為原型，真實故事中，Paul DePodesta是哈佛大學經濟系畢業的，而且他一點也不胖，他在大學有練過棒球和美式足球。  

電影中，兩人用數據分析組出的運動家隊，是那年的黑馬，打出破紀錄的20連勝並且進入季後賽，將數據科學帶入棒球領域，實際上運動家隊至2000年開始連續四年拿下分區冠軍晉級季後賽，直到2004年在最後一個系列賽輸給天使才中斷連續紀錄，可惜的是連續四年都在季後賽第一輪就被淘汰。Paul DePodesta在2003年被挖角到道奇隊，2004年，也就是Paul DePodesta到道奇隊的第一年，道奇隊拿到西區冠軍。  

就像電影中Billy Beane說的一樣，小市場球隊往往是大市場球隊的農場，小市場球隊好不容易培養出的棒球明星很快就會被大市場球隊買走，大聯盟的團隊薪資差距非常大，下表是2018年最貴和最便宜的三支球隊，可以發現組一支紅襪隊的錢竟然可以組三支運動家隊。  

| 薪資排名 | 球隊 | 25人名單薪資 | 總薪資 |
| -------- | -------- | -------- | -------- |
| 1 | Boston Red Sox | $172,670,000 | $235,145,428 |
| 2 | San Francisco Giants | $145,659,777 | $208,004,777 |
| 3 | Los Angeles Dodgers | $140,369,045 | $185,590,711 |
| 28| Tampa Bay Rays | $67,254,132 | $78,219,329 |
| 29| Chicago White Sox | $68,357,000 | $72,202,000 |
| 30| Oakland Athletics | $58,873,333 | $67,475,833 |

那小市場球隊就沒有勝算嗎？還是可以的，通常是買下有潛力的球員自己培養，趁這些球員還沒打出身價時簽約比較便宜，然後等到某一批球員開始打出成績時再花一大筆錢All in拚冠軍，對小市場球隊來說，每筆交易都是非常重要的，容錯空間非常小，若簽到的球員突然退化或受傷，可能球隊的奪冠之路又要延後好幾年，因此靠數據分析球員就顯得特別重要。  

最近把Ｒ的官方文件看完，這次試試看用R來分析團隊薪資，順便紀錄一些R處理資料的方法，程式碼放在這裡。  
## 資料前處理
```
library(dplyr)
library(ggplot2)

team_data <- read.csv("/Users/owlting/Desktop/baseball/the-history-of-baseball/team.csv")
salary_data <- read.csv("/Users/owlting/Desktop/baseball/the-history-of-baseball/salary.csv")
salary_data <- filter(salary_data, salary > 0) 
salary_data$salary <- salary_data$salary/10000 
team_salary<-group_by(salary_data, year ,team_id)
mlb_salary<-group_by(salary_data, year)
team_salary_trend <- summarise(team_salary,
                   count = n(),                
                   max_mon = max(salary),       
                   min_mon = min(salary),       
                   avg_sales = mean(salary),    
                   sum_sales = sum(salary))     
mlb_salary_trend <- summarise(mlb_salary,
                     count = n(),                
                     max_mon = max(salary),       
                     min_mon = min(salary),       
                     avg_sales = mean(salary),    
                     sum_sales = sum(salary)) 
team_data <- filter(team_data, year > 1984)
team_data = team_data %>% select(year, team_id, w, ws_win) 
mlb_salary_win = merge(team_salary_trend, team_data, by =c("year","team_id"))
mlb_salary_win["one_win_price"] <- mlb_salary_win$sum_sales / mlb_salary_win$w 

mlb_salary_win<-group_by(mlb_salary_win, year)
onewin_price <- summarise(mlb_salary_win,
                          onewin_sd = sd(one_win_price),
                          onewin_mean = mean(one_win_price)) 
mlb_salary_win = merge(mlb_salary_win, onewin_price, by ="year")
mlb_salary_win["z_score"] <- round((mlb_salary_win$one_win_price 
                            - mlb_salary_win$onewin_mean)/mlb_salary_win$onewin_sd,2)
```
### 資料前處理筆記  
```
salary_data <- filter(salary_data, salary > 0) 
```
`filter`可以對特定column的數據做篩選。  

```
salary_data$salary <- salary_data$salary/10000 
```
可以直接對特定column進行處理再傳回去。  

```
team_salary<-group_by(salary_data, year ,team_id)
```
`group_by`可以用特定column當作分類進行統計。  

```
team_salary_trend <- summarise(team_salary,
                   count = n(),                
                   max_mon = max(salary),       
                   min_mon = min(salary),       
                   avg_sales = mean(salary),    
                   sum_sales = sum(salary))  
```
`summarise`可以對特定table中的特定column做一些基本的統計分析。  

```
team_data = team_data %>% select(year, team_id, w, ws_win) #select needed columns
```
`%>%`是pipeline概念，直接將前面的變數當作後面function的第一個參數使用。  
`select`可以選擇特定column。  

```
mlb_salary_win = merge(team_salary_trend, team_data, by =c("year","team_id"))
```
`merge`可以合併兩個table，如果要用兩個column來合需要`by = c("","")`，只用一個只要`by = ""`。
## 單一球隊團隊薪資與聯盟平均比較
輸入球隊名稱，回傳該球隊自1985年團隊薪資與每年聯盟平均團隊薪資的變化。  
```
function(team){
  salary_team<-subset(mlb_salary_win,team_id==team) 
  salary_team = salary_team %>% rename(avg_team = avg_sales)  
  salary_team = salary_team %>% select(year,avg_team) 
  mlb_salary_trend = merge(mlb_salary_trend, salary_team, by ="year")
  lineplot<-ggplot(mlb_salary_trend, aes(x = year))
  lineplot+geom_line(aes(y = avg_sales),size = 1.5,color = 2)+ 
    geom_line(aes(y = avg_team),size = 1.5,color = 4)
  #size粗度
  #color:1black 2red 3green 4blue 5lightblue
  path = paste("/baseball/",as.character(team), "_salary.png", sep='')
  ggsave(path) 
}
```
`ggplot`用來劃出各式統計圖。  
`paste`可以連接兩字串。  

先來看看豪門球隊的薪資是怎麼走的。  
(紅色是聯盟平均，藍色是該球隊平均)  
NYA洋基隊：  
![](https://i.imgur.com/IRyaHq6.png)  

BOS紅襪隊：  
![](https://i.imgur.com/JCFwdDF.png)  

接著看看小市場的球隊。  
KCA皇家隊：  
![](https://i.imgur.com/2rssUos.png) 很可惜在最後世界大賽遇到偶數年巨人軍，以4:3輸給巨人，2015還有再拼一年的本錢，於是有投入了一筆錢最終終於在冠軍系列賽以4:1擊敗大都會隊獲得冠軍，這時他們所花的薪資還不到聯盟平均。奪冠後，冠軍隊球員幾乎都被別隊買走了，當年的冠軍陣容成員幾乎都不在了，皇家隊又進入了重建，標準的小市場球隊奪冠劇本。

OAK運動家隊：  
![](https://i.imgur.com/2sgPlZ5.png)  
Billy Beane是1997年開始當GM，一直讓運動家隊的團隊薪資保持在聯盟平均以下，2007年算是運動家隊相對比較慘的球季，那年陣中主力相繼受傷，最後運動家以勝率不到五成結束2007年賽季，是自1998後第一次不到五成。

剩下球隊可以用上面提供的程式碼試試看。  

## 單一球隊單場勝場花費
輸入球隊名稱，回傳該球隊自1985年每場勝場花費的[z-score](https://zh.wikipedia.org/wiki/%E6%A8%99%E6%BA%96%E5%88%86%E6%95%B8)，這裡用z-score是因為聯盟平均薪資是逐年上升的，也就是養一支球隊的花費是逐年增加的，所以用z-score來比較相對比較不花錢的球隊比較合理。  
```
function(team){
  onewin<-subset(mlb_salary_win,team_id==team) 
  lineplot<-ggplot(onewin, aes(x = year))
  lineplot+geom_line(aes(y = z_score),size = 1.5,color = 4) 
  path = paste("/Users/Owlting/Desktop/baseball/",
               as.character(team), "_onewin_zscore.png", sep='') #字串相接
  ggsave(path) 
}
```
NYA洋基隊：  
![](https://i.imgur.com/Cnf773h.png)  
基本上都是正的，也就是比其他隊花更多錢在每場勝利上，甚至z-score能超過3。  

OAK運動家隊：  
![](https://i.imgur.com/pLuTmke.png)  
自Billy Beane接手後都維持在負，也就是相對其他球隊每場勝場的花費較少，只有一次稍微超過0，也就是令人失望的2007年賽季，從這張圖可以看到貫徹Billy Beane魔球理念的運動家隊。  

剩下球隊可以用上面提供的程式碼試試看。  

## 奪冠球隊花費
不管用多划算的價錢組出一隻多有競爭力的球隊，能不能拿到冠軍還是球迷們最關注的問題，以下取出1985~2015年所有獲得世界冠軍的30支球隊(1994因為罷工沒有世界賽)
```
champion_team<-subset(mlb_salary_win,ws_win=='Y') 
```

以下為使用最划算的價格得到世界冠軍的球隊(前六名)  

| Team | year | z-score |
| -------- | -------- | -------- |
| MIN 雙城    | 1987 | -1.06 |
| CIN 紅人    | 1990 | -1.05 |
| FLO 馬林魚  | 2003 | -1.04 |
| ANA 天使    | 2002 | -0.81 |
| KCA 皇家    | 1985 | -0.73 |
| KCA 皇家    | 2015 | -0.57 |

以下為使用最貴的價格得到世界冠軍的球隊(前六名)  

| Team | year | z-score |
| -------- | -------- | -------- |
| NYA 洋基    | 2009 | 2.41 |
| NYA 洋基    | 1996 | 1.55 |
| NYA 洋基    | 2000 | 1.49 |
| BOS 紅襪    | 2004 | 1.34 |
| BOS 紅襪    | 2007 | 1.32 |
| NYA 洋基    | 1999 | 1.24 |

誰是土豪很明顯了吧！洋基前六名佔了四個，可見預算足夠，要拿冠軍是沒有問題的，但用有限的預算拿到冠軍的GM就厲害了，他們可以把每一塊錢都發揮到最大的效用，因此我們可以用z-score來評估一個球隊的管理團隊的理念，球團老闆也可以用這個指標來評估球隊GM的績效。  

數據棒球(1)-1987的雙城隊
===
###### tags: `棒球`
---
layout: post
title: 1987的雙城隊
tags: 
  - "baseball"
---
MLB冠軍是所有棒球員的最終目標，原本是想看看拿到世界冠軍的隊伍都具有哪些特徵，意外發現在這些冠軍隊伍中有一個非常特別的outlier，那就是1987年的明尼蘇達雙城隊，那年的雙城隊淨得分值為-20，也就是失分比得分多了20分，勝敗場為85-77，先在美聯冠軍賽以4-1擊敗當年美聯最強的底特律老虎(98-64)，然後在世界冠軍系列賽以4-3在第七場淘汰了傳統強隊聖路易紅雀(95-67)，攤開所有數據來看，那年的雙城不像是可以拿下世界冠軍的隊伍，於是我開始尋找那年雙城為何可以拿下冠軍的原因。  

## DataSet
本篇使用Kaggle上的[資料](https://www.kaggle.com/seanlahman/the-history-of-baseball#player.csv)來進行分析，這是一份1871~2015年MLB各球隊與球員的數據，有蠻多主題值得去探討的。  

讀取資料，這裡我只保留1900年後的，比較符合現代棒球的數據。  
```
data = pd.read_csv('dataset/team.csv')
data = data[data.year > 1900]
```
  
## 從團隊打擊和團隊防禦切入分析
由於20世紀初的資料有些進階數據缺值比較多，這邊就只以最直觀的avg和era來看1900~2015年得到世界冠軍的隊伍。  
`avg`:團隊打擊率  
`era`:團隊防禦率  
```
x = champion['era']
y = champion['avg']
plt.axis([x.min() - 1,x.max() + 1, y.min() - 0.01, y.max() + 0.01])
plt.xlabel('era')
plt.ylabel('avg')
plt.scatter(x,y)
plt.annotate('1906 CHW', xy=(2.13,0.2301),\
xycoords='data', xytext=(1, 0.235), size=10,\
arrowprops=dict(arrowstyle="simple",fc="0.6",\
ec="none"))
plt.show()
```
基本上可以看出era越高的隊伍打擊率也越高，因為當球隊經理把錢集中在補強打者上，那能花在補強投手的錢就少了，那就看是想走靠打擊還是靠投手哪個方向，不過也有可能是每年聯盟的環境不同，有時是打高投低的打擊聯盟，反之亦然。  
特別點出打擊率不到0.24的1906年白襪隊為例，0.2301的打擊率真的蠻差的，不過靠著團隊防禦率只有2.13的投手陣容，一樣可以奪冠。  
![](https://i.imgur.com/gl3oCwS.png)  

## 從淨得分差和勝率切入分析
接著我使用rd和勝率去分析  
`rd`:run difference，總得分減總失分  
```
x = champion['rd']
y = champion['winrate']
plt.axis([x.min() - 10,x.max() + 10, y.min() - 10, y.max() + 10])
plt.xlabel('rd')
plt.ylabel('win-rate %')
plt.scatter(x,y)

min_rd = champion.nsmallest(5,'rd')
max_rd = champion.nlargest(5,'rd')
min_winrate = champion.nsmallest(5,'winrate')

plt.annotate('1987 MIN', xy=(-20,52), xycoords='data', xytext=(-20, 63), size=10, arrowprops=dict(arrowstyle="simple",fc="0.6", ec="none"))
plt.annotate('2006 STL', xy=(19,51.5), xycoords='data', xytext=(50, 45), size=10, arrowprops=dict(arrowstyle="simple",fc="0.6", ec="none"))
plt.annotate('1939 NYY', xy=(411,70.2), xycoords='data', xytext=(340, 80), size=10, arrowprops=dict(arrowstyle="simple",fc="0.6", ec="none"))
plt.annotate('1927 NYY', xy=(376,71.43), xycoords='data', xytext=(300, 57), size=10, arrowprops=dict(arrowstyle="simple",fc="0.6", ec="none"))
plt.show()
```
看到這張圖馬上可以看到rd各有兩個極端值，先講右邊有著超高rd的兩點，兩個都是紐約洋基隊，事實上rd最高的五支球隊都是洋基隊，而得分洋基隊則包辦了前7名，可見洋基的組隊理念很明確，就組出一個超級打擊隊，把對手打爆冠軍自然就進來了，反正洋基有錢嘛XD  
![](https://i.imgur.com/u4KAEyF.png)  
接著看左邊兩個極端值，2006年紅雀隊之後再研究，比較讓我驚訝的是1987年的雙城隊，這球隊的rd竟然小於0，也就是失分比得分多，這樣都能拿冠軍到底是怎麼辦到的。  

## 1987年的雙城隊
我將1900~2015年的數據做統計取平均，做了一個比較，想找出1987的雙城到底優勢在哪裡。  
```
data_1987 =data[data.year == 1987]
des_1987 = only_data(data_1987).mean()
des_all = only_data(data).mean()
des_champion = only_data(champion).mean()
twin = champion[champion.year == 1987]
twin_1987 = only_data(twin).mean()
comparison = pd.concat([twin_1987, des_all, des_1987, des_champion], axis=1)
comparison.columns = ['1987_twin','all','1987','champion']
```
以下為比較表格：  

|  | 1987的雙城隊 | 1900~2015所有球隊 | 1987年的所有球隊 | 所有冠軍隊|
| -------- | -------- | -------- | -------- |-------- |
| 勝場     | 85     |78.14     | 80.96     |96.81 |
| 敗場     | 77     |78.14     | 80.96     |59.43 |
| 得分     | 786     |689.99     | 764.73 |771.91 |
| 安打     | 1422     |1397.19     | 1457.5 |1451.48|
| 二壘安打     | 258     |240.66     | 261.27|248.41|
| 三壘安打     | 35     |44.93     | 34.46    |53.34 |
| 全壘打     | 196     |113.35  | 171.46     |124.74 |
| 保送     | 523     |504.59    | 553.42     |542.87   |
| 打擊率   | 0.2613     |0.2613  | 0.2629     |0.2702  |
| 三振     | 898     |807.67     | 965.35     |747.66   |
| 盜壘    | 113     |100.36  | 137.88     |104.5  |
| 被得分     | 806     |689.99  | 764.73     |604.97  |
| 自責分     | 734     |600.74  | 687.46     |526.69 |
| 防禦率     | 4.63     |3.85  | 4.28     |3.35  |
| 救援點     | 39     |27.19  | 37.35     |30.41  |
| 被安打     | 1465     |1396.98  | 1457.5     |1322.15  |
| 被全壘打    | 210     |113.35  | 171.46     |97.58  |
| 投出保送   | 564     |505  | 553.42     |488.2  |
| 被三振     | 990     |796.36  | 965.35     |797.39  |
| 失誤     | 98     |152.44  | 126.38     |142  |
| 雙殺     | 147     |142.55  | 148.85     |144.27  |
| 淨得分  | -20     |0  | 0     |166.94  |
| 勝率     | 52.47%     | 0  | 0     |62.02% |

其中雙城隊比較突出的是196支全壘打，不過從1987年所有球隊平均打了171.46支全壘打跟全部年分的113.35比起來，可以看出1987年是打擊聯盟，但那年的雙城的確特別會轟。不過從被全壘打來看雙城的投手也是特別會被轟。  
另一個值得注意的是失誤，雙城的98次失誤遠低於當年全聯盟平均的126.38次以及一般冠軍隊的142次，所以穩定的守備和特別會打全壘打的野手補足了投手的弱點。  

## 數據外的因素
以下是從[MLB官網](https://www.mlb.com/standings/advanced-splits/1987)找到的資料，1987年雙城所在分區的戰績，可以發現那年雙城所在的美西分區比美東分區弱很多，如果雙城在美東，那年只能拿到第五名。  
![](https://i.imgur.com/TXXdXDs.jpg)  
![](https://i.imgur.com/oqUd8yr.jpg)  
還有一點值得注意的是雙城在人工草地可以拿下60-33的成績，在自然草地卻只能拿下25-44的成績，這也差太多了吧！那雙城主場是甚麼草地呢？胡伯特·哈姆佛里圓頂體育場（使用時間1982年－2009年），是個室內球場，所以是人工草皮。  
[photo source 
](https://ballparkdigest.com/201204124721/college-baseball/visits/hubert-h-humphrey-metrodome-minnesota-gophers)  
![](https://i.imgur.com/EHcuhrr.jpg)  

以下是[Wiki](https://en.wikipedia.org/wiki/1987_Minnesota_Twins_season)的資料，雙城主場的戰績為56-25，客場戰績為29-52，三分之二的勝場是靠主場贏的，所以當年雙城的主場靈氣特別大，球員一回主場就會爆發。  
![](https://i.imgur.com/fcjJI0T.jpg)  
那最關鍵的季後賽又如何呢？以4-1擊敗老虎，其中的三場勝場是主場拿到的，最後的世界冠系列戰先在主場贏兩場，然後到紅雀主場就連敗三場，最後回到雙城主場又連贏兩場，這主場根本有神保佑阿，太厲害了吧！所以當年要是明星賽是國聯拿下，世界大賽就會是紅雀拿到四場主場機會，那雙城可能就不會拿到冠軍了。  

話說1987年的雙城是打擊比較厲害的球隊，那投手到底多慘，以下是從wiki找到的資料，當年的五位先發。  
![](https://i.imgur.com/xLRVaz1.jpg)  
前兩號先發的成績還算不錯，一號先發[Bert Blyleven](https://en.wikipedia.org/wiki/Bert_Blyleven)當年36歲已經算是老將了，但投得還算可以，他的累積三振是史上第五，後來有進名人堂，雙城還退休他的背號(28)，二號先發[Frank Viola](https://en.wikipedia.org/wiki/Frank_Viola)的防禦率2.9很厲害，在季後賽變成王牌，且都投出不錯的成績，最後獲得世界冠軍系列賽的MVP，隔年還拿到賽揚獎。  

## 結論
1987年的雙城隊靠著全壘打和穩定的守備，還有很強的主場靈氣，賽季的前兩號先發到季後表現還不錯，最後拿下世界冠軍。  


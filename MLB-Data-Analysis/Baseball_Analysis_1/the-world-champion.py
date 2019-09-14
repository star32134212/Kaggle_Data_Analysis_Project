# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('dataset/team.csv')
data = data[data.year > 1900]
"""
只拿取需要的資料
"""
def rd(r,ra):
    return r-ra

def winrate(win,lose):
    winr=(win/(win+lose))*100
    return round(winr,2)

def avg(ab,hit):
    avg = hit / ab
    return round(avg,4)

def only_data(df):
    df2 = df[['w', 'l', 'r', 'ab', 'h', 'double', 'triple',\
              'hr', 'bb', 'so', 'sb', 'ra', 'er', 'era',\
              'sv', 'ha', 'hra', 'bba','soa', 'e', 'dp',\
              'rd', 'winrate', 'avg']] 
    return df2
#cg 不看 以前太多可以投滿整場的神獸了xd 現代棒球講求分工
data['rd'] = data.apply(lambda row: rd(row['r'], row['ra']), axis = 1)
data['winrate'] = data.apply(lambda row: winrate(row['w'], row['l']), axis = 1)
data['avg'] = data.apply(lambda row: avg(row['ab'], row['h']), axis = 1)
champion = data[data.ws_win == 'Y']

"""
era avg
"""
#由於SF(犧牲打)的nan直蠻多的，這裡就不用攻擊指數來做比較 改用打擊率
x = champion['era']
y = champion['avg']
plt.axis([x.min() - 1,x.max() + 1, y.min() - 0.01, y.max() + 0.01])
plt.xlabel('era')
plt.ylabel('avg')
plt.scatter(x,y)
plt.annotate('1906 CHW', xy=(2.13,0.2301), xycoords='data', xytext=(1, 0.235), size=10, arrowprops=dict(arrowstyle="simple",fc="0.6", ec="none"))
#大致可看出era和avg很難兼顧，只能往某部份去補強
plt.savefig('avg_era')
plt.show()
plt.close()
#從淨得分和勝率去看冠軍隊
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
plt.savefig('wr_rd')
plt.show()
plt.close()

data_1987 =data[data.year == 1987]
des_1987 = only_data(data_1987).mean()
des_all = only_data(data).mean()
des_champion = only_data(champion).mean()
twin = champion[champion.year == 1987]
twin_1987 = only_data(twin).mean()
comparison = pd.concat([twin_1987, des_all, des_1987, des_champion], axis=1)
comparison.columns = ['1987_twin','all','1987','champion']
print(twin)

comparison.to_csv('comparison.txt,',sep='\t')
library(dplyr)
library(ggplot2)

team_data <- read.csv(".../the-history-of-baseball/team.csv")
salary_data <- read.csv(".../baseball/the-history-of-baseball/salary.csv")
salary_data <- filter(salary_data, salary > 0) #去除column salary為0的row
salary_data$salary <- salary_data$salary/10000 #改用萬來呈現 
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
team_data <- filter(team_data, year > 1984)#因為salary是從1985才開始有資料
team_data = team_data %>% select(year, team_id, w, ws_win) #select needed columns
mlb_salary_win = merge(team_salary_trend, team_data, by =c("year","team_id"))
mlb_salary_win["one_win_price"] <- mlb_salary_win$sum_sales / mlb_salary_win$w 
#兩列相除放到新的一個column

#改用標準差處理
mlb_salary_win<-group_by(mlb_salary_win, year)
onewin_price <- summarise(mlb_salary_win,
                          onewin_sd = sd(one_win_price),
                          onewin_mean = mean(one_win_price)) 
mlb_salary_win = merge(mlb_salary_win, onewin_price, by ="year")
mlb_salary_win["z_score"] <- round((mlb_salary_win$one_win_price 
                            - mlb_salary_win$onewin_mean)/mlb_salary_win$onewin_sd,2)

#用每場勝場代價z-score來看經理好壞(用z-score撇除薪資逐年上升因素)          
#Zscore高代表每場勝場花費相對較高
onewin_zscore <- function(team){
  onewin<-subset(mlb_salary_win,team_id==team) 
  lineplot<-ggplot(onewin, aes(x = year))
  lineplot+geom_line(aes(y = z_score),size = 1.5,color = 4) #可以直接換行
  path = paste("/Users/Owlting/Desktop/baseball/",
               as.character(team), "_onewin_zscore.png", sep='') #字串相接
  ggsave(path) 
}

#某一球隊隨著年份團隊薪資變化(與聯盟平均作比較)
team_salary <- function(team){
  salary_team<-subset(mlb_salary_win,team_id==team) 
  salary_team = salary_team %>% rename(avg_team = avg_sales) #%>%可以直接傳入第一個參數 
  salary_team = salary_team %>% select(year,avg_team) 
  mlb_salary_trend = merge(mlb_salary_trend, salary_team, by ="year")
  lineplot<-ggplot(mlb_salary_trend, aes(x = year))
  lineplot+geom_line(aes(y = avg_sales),size = 1.5,color = 2)+ #可以直接換行
    geom_line(aes(y = avg_team),size = 1.5,color = 4)
  #size粗度
  #color:1black 2red 3green 4blue 5lightblue
  path = paste("/Users/Owlting/Desktop/baseball/",
               as.character(team), "_salary.png", sep='') #字串相接
  ggsave(path) 
}

#分析冠軍隊花費
champion_team<-subset(mlb_salary_win,ws_win=='Y') 


team_salary("BOS")
onewin_zscore("BOS")

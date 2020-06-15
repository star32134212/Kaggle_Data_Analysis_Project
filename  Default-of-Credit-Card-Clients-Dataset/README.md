# Default of Credit Card Clients Dataset
2020 Deep Learning final project  
[dataset](https://www.kaggle.com/uciml/default-of-credit-card-clients-dataset)  
### Data
`ID`: ID of each client  
`LIMIT_BAL`: Amount of given credit in NT dollars (includes individual and family/supplementary credit
`SEX`: Gender (1=male, 2=female)  
`EDUCATION`: (1=graduate school, 2=university, 3=high school, 4=others, 5=unknown, 6=unknown)  
`MARRIAGE`: Marital status (1=married, 2=single, 3=others)  
`AGE`: Age in years  
`PAY_0`: Repayment status in September, 2005 (-1=pay duly, 1=payment delay for one month, 2=payment delay for two months, … 8=payment delay for eight months, 9=payment delay for nine months and above)  
`PAY_2`: Repayment status in August, 2005 (scale same as above)  
`PAY_3`: Repayment status in July, 2005 (scale same as above)  
`PAY_4`: Repayment status in June, 2005 (scale same as above)  
`PAY_5`: Repayment status in May, 2005 (scale same as above)  
`PAY_6`: Repayment status in April, 2005 (scale same as above)  
`BILL_AMT1`: Amount of bill statement in September, 2005 (NT dollar)  
`BILL_AMT2`: Amount of bill statement in August, 2005 (NT dollar)  
`BILL_AMT3`: Amount of bill statement in July, 2005 (NT dollar)  
`BILL_AMT4`: Amount of bill statement in June, 2005 (NT dollar)  
`BILL_AMT5`: Amount of bill statement in May, 2005 (NT dollar)  
`BILL_AMT6`: Amount of bill statement in April, 2005 (NT dollar)  
`PAY_AMT1`: Amount of previous payment in September, 2005 (NT dollar)  
`PAY_AMT2`: Amount of previous payment in August, 2005 (NT dollar)  
`PAY_AMT3`: Amount of previous payment in July, 2005 (NT dollar)  
`PAY_AMT4`: Amount of previous payment in June, 2005 (NT dollar)  
`PAY_AMT5`: Amount of previous payment in May, 2005 (NT dollar)  
`PAY_AMT6`: Amount of previous payment in April, 2005 (NT dollar)  
`default.payment.next.month`: Default payment (1=yes, 0=no)  
### Model
```
DNN(
  (dnn1): Sequential(
    (0): Linear(in_features=9, out_features=36, bias=True)
    (1): ReLU()
  )
  (dnn2): Sequential(
    (0): Linear(in_features=36, out_features=108, bias=True)
    (1): Dropout(p=0.8, inplace=False)
    (2): ReLU()
  )
  (dnn3): Sequential(
    (0): Linear(in_features=108, out_features=2, bias=True)
  )
)
```

### Result
**Imbalanced data processing: False**  
#### train
PP 0  
PN 653  
NP 0  
NN 2347  
acc 0.77452  
precision 0.2857142857142857  
recall 0.0010660980810234541  
f1_score 0.002124269782262347  
auc 0.6275074545947411  
#### test
PP 0  
PN 653  
NP 0  
NN 2347  
acc 0.77452  
precision 0.2857142857142857  
recall 0.0010660980810234541  
f1_score 0.002124269782262347  
auc 0.6275074545947411  
**Imbalanced data processing: True**  
#### train
PP 626  
PN 799  
NP 433  
NN 1142  
acc 0.5959  
precision 0.5938281901584654  
recall 0.4529262086513995  
f1_score 0.5138939011187297  
auc 0.6144589053307185  
#### test
PP 626  
PN 799  
NP 433  
NN 1142  
acc 0.5893333333333334  
precision 0.591123701605288  
recall 0.4392982456140351  
f1_score 0.5040257648953301  
auc 0.6144589053307185  



#### Link
[slide](https://www.overleaf.com/project/5edf7f6245fbdc00014c61e0)  
[notion](https://www.notion.so/Group40-Report-e90145527717498381951c12f4cf33cb)  
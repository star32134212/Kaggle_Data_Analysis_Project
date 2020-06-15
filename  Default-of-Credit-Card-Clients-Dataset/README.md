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
**Imbalanced data processing: True**  
#### train

#### test
PP 608  
PN 817  
NP 401  
NN 1174  
acc 0.594  
precision 0.6025768087215064  
recall 0.4266666666666667  
f1_score 0.49958915365653245  
auc 0.6081689011625317  

**Imbalanced data processing: False**  
#### train

#### test


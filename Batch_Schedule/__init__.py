import pandas  as pd

Lis={'姓名':['zhangsan','lisi'],'性别':['nan','nv']}
data=pd.DataFrame(Lis)
data.to_csv('output_data.csv')
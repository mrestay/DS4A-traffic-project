
import pandas as pd

b = pd.DataFrame()
for i in ['2014','2015','2016', '2017', '2018', '2019']:
  a = pd.read_csv('out-'+i+'.csv')
  print(a)
  b = pd.concat([b,a])

print(b)
b.to_csv('./total.csv')
  
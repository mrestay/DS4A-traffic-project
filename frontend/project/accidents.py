import pandas as pd

accidents_2015=pd.read_csv('../../data/dataset_2015_with_negatives.csv',sep=',')
accidents_2016=pd.read_csv('../../data/dataset_2016_with_negatives.csv',sep=',')
accidents_2017=pd.read_csv('../../data/dataset_2017_with_negatives.csv',sep=',')
accidents_2018=pd.read_csv('../../data/dataset_2018_with_negatives.csv',sep=',')
accidents_2019=pd.read_csv('../../data/dataset_2019_with_negatives.csv',sep=',')

accidents_All=pd.concat([accidents_2015, accidents_2016,accidents_2017,
                        accidents_2018,accidents_2019], ignore_index=True)

accidents_All1=accidents_All[accidents_All['sample_type']==1]


agg = ['mean','min','median','max']
t_year=accidents_All1[['year','temperature']].groupby('year').agg(agg)

temperature = t_year.temperature.transpose()


p_year=accidents_All1[['year','precipIntensity']].groupby('year').agg(agg)

precipitation = p_year.precipIntensity.transpose()

# mt_2015=round(t_year.temperature['mean'][2015],2)
# mt_2016=round(t_year.temperature['mean'][2016],2)
# mt_2017=round(t_year.temperature['mean'][2017],2)
# mt_2018=round(t_year.temperature['mean'][2018],2)
# mt_2019=round(t_year.temperature['mean'][2019],2)
# print(mt_2015,mt_2016,mt_2017,mt_2018,mt_2019)
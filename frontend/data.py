import pandas as pd
import os

data_folder = '../data'

# accidents
# accidents_2015=pd.read_csv(os.path.join(data_folder, 'dataset_2015_with_negatives.csv'),sep=',')
# accidents_2016=pd.read_csv(os.path.join(data_folder, 'dataset_2016_with_negatives.csv'),sep=',')
# accidents_2017=pd.read_csv(os.path.join(data_folder, 'dataset_2017_with_negatives.csv'),sep=',')
# accidents_2018=pd.read_csv(os.path.join(data_folder, 'dataset_2018_with_negatives.csv'),sep=',')
# accidents_2019=pd.read_csv(os.path.join(data_folder, 'dataset_2019_with_negatives.csv'),sep=',')


accidents_file = os.path.join(data_folder, 'accident_clean.csv')
accidents = pd.read_csv(accidents_file, sep=',')

accidents_All = pd.read_csv(os.path.join(data_folder, 'dataset_clean.csv'),sep=',')

# accidents_All1 = accidents_All[accidents_All['sample_type'] == 1]

# temperature
agg = ['mean', 'min', 'median', 'max']
t_year = accidents_All[['year', 'temperature']].groupby('year').agg(agg)

temperature = t_year.temperature.transpose()

# presipitation
p_year = accidents_All[['year', 'precipIntensity']].groupby('year').agg(agg)

precipitation = p_year.precipIntensity.transpose()

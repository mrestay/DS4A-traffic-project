import os
import pandas as pd
import sys

year = sys.argv[1]
path = '../../data/datasets/weather/'
# path = '../data/darksky/output_data/'
directory = os.fsencode(path)

out = pd.DataFrame()
for file in os.listdir(directory):
  filename = os.fsdecode(file)
  if filename.startswith("weather_"+year):
    print(file)
    df = pd.read_csv(path + filename)
    df['location'] = filename.split('_')[4].split('.')[0]
    out = pd.concat([out, df])
  else:
    continue


print(out)
out.to_csv('./out-'+year+'.csv')
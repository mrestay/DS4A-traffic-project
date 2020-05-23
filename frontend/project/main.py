import streamlit as st
import pandas as pd
import numpy as np
import os
import altair as alt
# from vega_datasets import data
import pydeck as pdk


from .sidebar import *

# read dataset
data_folder = '../data'
accidents_file = os.path.join(data_folder, 'accident_clean.csv')
accidents = pd.read_csv(accidents_file,sep=',')
# accidents.head()


accidents = accidents[accidents['year'] <= year[1]][accidents['year'] >= year[0]]

# by date
by_date = accidents[['date','accident_id',  'year']].groupby(['year','date']).count().reset_index().sort_values(by='date')
by_date = by_date.reset_index(drop=True)

# by hour
# by_hour_g = accidents[['hour','accident_id', 'year', 'severity']].groupby(['year','hour']).count().reset_index().sort_values(by='year')
# by_hour_g = by_hour_g.reset_index(drop=True)
# by_hour_g.rename(columns={'accident_id':'accident_count'}, inplace=True)
by_hour_cross = pd.crosstab(accidents.hour, accidents.severity).reset_index()

# by_hour = pd.merge(by_hour_cross, by_hour_g, on=['year', 'hour'])
by_hour = by_hour_cross

######
st.title("Traffic project")
st.subheader('Accidents')

# burbujas
from .widgets import bubble, tiles
from .accidents import temperature, precipitation, agg


temp = temperature[year[1]] 
temp_list = [round(temp[x]) for x in agg]

preci = precipitation[year[1]] 
preci_list = [round(preci[x]) for x in agg]

# st.write(temp_list)

st.write(f"""
<div style="display: flex;">
    {bubble([
    'Average</br>temp',
    'Min</br>temp',
    'Median</br>temp',
    'Max</br>temp',
    ],
   temp_list,
    ['#0C4990','#1770C2','#F1516E', '#69C1FF'])}
    {bubble([
    'Average</br>preci',
    'Min</br>preci',
    'Median</br>preci',
    'Max</br>preci',
    ],
    preci_list,
    ['#0C4990','#1770C2','#F1516E', '#69C1FF'])}
</div>""", unsafe_allow_html=True)


title = 'Total accidents'
titleValue = '31322'
subTitles=['Accidents with</br>Fatality', 'Accidents with</br>Injury', 'Accidents with </br> Material damage']
subValues=[24532, 35342, 35342]

st.write(tiles(title, titleValue, subTitles, subValues),  unsafe_allow_html=True)


# st.write(year)
# st.write(by_hour)

# by hour
by_hour_chart = alt.Chart(by_hour).transform_fold(
    accidents.severity.unique(),
    as_=['severity', 'accident_count']
).mark_bar().encode(
    # alt.X("Accidents by hour", bin=True),
    x='hour',
    y='accident_count:Q',
    color='severity:N',
    tooltip=['accident_count:Q', 'severity:N']
)
st.altair_chart(by_hour_chart, use_container_width=True)


by_day_cross = accidents.groupby(['hour', 'day']).count().reset_index()
by_day_cross.rename(columns={'accident_id':'accident_count'}, inplace=True)

# st.write(by_day_cross)
# row_sums = by_day_cross.to_numpy().sum(axis=1, keepdims=True)
# by_day_cross = by_day_cross / row_sums

by_day_chart = alt.Chart(by_day_cross).mark_rect().encode(
    x='hour:O',
    y='day:O',  
    color='accident_count:Q',
    tooltip=['hour','day', 'accident_count']
)
st.altair_chart(by_day_chart, use_container_width=True)

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data = accidents.sample(frac=0.1)

COLOR_BREWER_BLUE_SCALE = [
    [240, 249, 232],
    [204, 235, 197],
    [168, 221, 181],
    [123, 204, 196],
    [67, 162, 202],
    [8, 104, 172],
]

st.pydeck_chart(pdk.Deck(
  map_style='mapbox://styles/mapbox/light-v9',
  initial_view_state=pdk.ViewState(
      latitude=4.654335,
      longitude=-74.083644,
      zoom=11,
    #   pitch=50,
  ),
  layers=[
      pdk.Layer(
        "HeatmapLayer",
        data=data,
        opacity=0.9,
        get_position=["x", "y"],
        aggregation='"MEAN"',
        color_range=COLOR_BREWER_BLUE_SCALE,
        threshold=1,
        get_weight="severity_numeric",
        pickable=True,
    )
    ],
))
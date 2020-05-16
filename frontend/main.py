import streamlit as st
import pandas as pd
import numpy as np
import os
import altair as alt
from vega_datasets import data
import pydeck as pdk


# read dataset
data_folder = '../data'
accidents_file = os.path.join(data_folder, 'accident_clean.csv')
accidents = pd.read_csv(accidents_file,sep=',')
# accidents.head()

year = st.sidebar.slider('Year', 2014, 2019, (2014,2019))

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

st.sidebar.radio('Segmentation', ('Total', 'By Year'))

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
  
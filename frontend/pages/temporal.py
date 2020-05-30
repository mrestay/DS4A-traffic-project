import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk
from data import accidents, temperature, precipitation, agg
from widgets import bubble, tiles
from conf import mapbox_key

def write():
    st.markdown('Use the panel on the left to select your preferred year segmentation')
    #--- sidebar ---
    year = st.sidebar.slider('Year', 2015, 2019, (2015,2019))

    accidents_by_year = accidents[accidents['year'] <= year[1]][accidents['year'] >= year[0]]

    by_hour_cross = pd.crosstab(accidents_by_year.hour, accidents_by_year.severity).reset_index()

    by_hour = by_hour_cross

    st.write("Here is the distribution of accidents for every hour.")
    by_hour_chart = alt.Chart(by_hour).transform_fold(
            list(accidents_by_year.severity.unique()),
            as_=['severity', 'accident_count']
        ).mark_bar().encode(
            # alt.X("Accidents by hour", bin=True),
            x='hour',
            y='accident_count:Q',
        color='severity:N',
        tooltip=['accident_count:Q', 'severity:N']
    )

    st.altair_chart(by_hour_chart, use_container_width=True)

    cross_hour_day = accidents_by_year[['hour', 'day_of_week', 'population']].groupby(
        ['hour', 'day_of_week']).count().reset_index()
    cross_hour_day.columns = ['hour', 'day_of_week', 'accidents']
    ### ploting heatmap
    accidnt_cross_hour_day_chart = nt_type_s = alt.Chart(cross_hour_day).mark_rect().encode(
        x='hour:O',
        y='day_of_week:O',
        color=alt.Color('accidents:Q', scale=alt.Scale(scheme='bluepurple')),
        tooltip=['hour', 'day_of_week', 'accidents']
    )

    st.write("Accidents per hour for every day of the week.")
    st.altair_chart(accidnt_cross_hour_day_chart, use_container_width=True)

    cross_day_month = accidents_by_year[['day_of_week', 'month', 'population']].groupby(
        ['day_of_week', 'month']).count().reset_index()
    cross_day_month .columns = ['day_of_week', 'month', 'accidents']

    ### ploting heatmap
    accident_cross_day_month_chart = nt_type_s = alt.Chart(cross_day_month).mark_rect().encode(
        x='day_of_week:O',
        y='month:O',
        color=alt.Color('accidents:Q', scale=alt.Scale(scheme='bluepurple')),
        tooltip=['day_of_week', 'month', 'accidents']
    )
    st.write("Accidents per day of the week for every month.")
    st.altair_chart(accident_cross_day_month_chart, use_container_width=True)

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
    segmentation = st.sidebar.radio('Segmentation', ('Total', 'By Year'))

    accidents_by_year = accidents[accidents['year'] <= year[1]][accidents['year'] >= year[0]]

    # by date
    by_date = accidents_by_year[['date','population','year']].groupby(['year','date']).count().reset_index().sort_values(by='date')
    by_date = by_date.reset_index(drop=True)

    # by hour
    # by_hour_g = accidents_by_year[['hour','population', 'year', 'severity']].groupby(['year','hour']).count().reset_index().sort_values(by='year')
    # by_hour_g = by_hour_g.reset_index(drop=True)
    # by_hour_g.rename(columns={'population':'accident_count'}, inplace=True)
    by_hour_cross = pd.crosstab(accidents_by_year.hour, accidents_by_year.severity).reset_index()

    # by_hour = pd.merge(by_hour_cross, by_hour_g, on=['year', 'hour'])
    by_hour = by_hour_cross

    ######
    # st.title("Accidents")
    # # st.subheader('Accidents')
    #
    # # burbujas
    # temp = temperature[year[1]]
    # temp_list = [round(temp[x]) for x in agg]
    #
    # preci = precipitation[year[1]]
    # preci_list = [round(preci[x]) for x in agg]
    #
    # # st.write(temp_list)
    #
    # st.write(f"""
    # <div style="display: flex;">
    #     {bubble([
    #     'Average</br>temp',
    #     'Min</br>temp',
    #     'Median</br>temp',
    #     'Max</br>temp',
    #     ],
    #    temp_list,
    #     ['#0C4990','#1770C2','#F1516E', '#69C1FF'])}
    #     {bubble([
    #     'Average</br>preci',
    #     'Min</br>preci',
    #     'Median</br>preci',
    #     'Max</br>preci',
    #     ],
    #     preci_list,
    #     ['#0C4990','#1770C2','#F1516E', '#69C1FF'])}
    # </div>""", unsafe_allow_html=True)
    #
    #
    # title = 'Total accidents'
    # titleValue = '31322'
    # subTitles=['Accidents with</br>Fatality', 'Accidents with</br>Injury', 'Accidents with </br> Material damage']
    # subValues=[24532, 35342, 35342]
    #
    # st.write(tiles(title, titleValue, subTitles, subValues),  unsafe_allow_html=True)


    # st.write(year)
    # st.write(by_hour)

    # st.write(type(accidents_by_year.severity.unique()))
    # by hour
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

    st.title('Accident count/type by hour of the day')

    st.altair_chart(by_hour_chart, use_container_width=True)


    by_day_cross = accidents_by_year.groupby(['hour', 'day']).count().reset_index()
    by_day_cross.rename(columns={'population':'accident_count'}, inplace=True)

    # st.write(by_day_cross)
    # row_sums = by_day_cross.to_numpy().sum(axis=1, keepdims=True)
    # by_day_cross = by_day_cross / row_sums

    by_day_chart = alt.Chart(by_day_cross).mark_rect().encode(
        x='hour:O',
        y='day:O',  
        color='accident_count:Q',
        tooltip=['hour','day', 'accident_count']
    )

    st.title('Accident count by hour of the day and day of the month')
    st.altair_chart(by_day_chart, use_container_width=True)

    accidents_by_year = accidents_by_year.sample(frac=0.1)
    # st.table(data)

    COLOR_BREWER_BLUE_SCALE = [
        [240, 249, 232],
        [204, 235, 197],
        [168, 221, 181],
        [123, 204, 196],
        [67, 162, 202],
        [8, 104, 172],
    ]

    # print(accidents_by_year.info())

    layer = pdk.Layer(
            "HeatmapLayer",
            accidents_by_year[['x','y','severity_numeric']],
            opacity=0.9,
            get_position=["x", "y"],
            aggregation='"MEAN"',
            color_range=COLOR_BREWER_BLUE_SCALE,
            threshold=1,
            get_weight="severity_numeric",
            pickable=True,
        )

    st.pydeck_chart(pdk.Deck(
      map_style='mapbox://styles/mapbox/dark-v9',
      mapbox_key=mapbox_key,
      initial_view_state=pdk.ViewState(
          latitude=4.654335,
          longitude=-74.083644,
          zoom=11,
        #   pitch=50,
      ),
      layers=[layer],
    ))
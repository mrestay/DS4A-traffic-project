import streamlit as st
from data import centroids, clustered_points, accidents
import pydeck as pdk
from conf import mapbox_key
from data import accidents
import pandas as pd

def write():
    st.title('Cluster analysis')

    year = st.selectbox('Chooose a year', (2015, 2016, 2017, 2018, 2019))
    st.markdown(f'This is the accident distribution for {year}.')
    accidents_filtered = accidents[accidents.year == year][['x', 'y']].sample(frac=0.25)

    layer = pdk.Layer(
        "ScatterplotLayer",
        accidents_filtered,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=30,
        radius_min_pixels=1,
        radius_max_pixels=20,
        line_width_min_pixels=1,
        get_position=['x', 'y'],
        get_radius="exits_radius",
        get_fill_color=[255, 0, 0],
        get_line_color=[0, 0, 0],
    )
    # Set the viewport location
    view_state = pdk.ViewState(latitude=4.6585, longitude=-74.0935, zoom=13, bearing=0,
                               pitch=0)

    # Render
    r = pdk.Deck(layers=[layer], initial_view_state=view_state,
                  map_style='mapbox://styles/mapbox/dark-v9',
                  mapbox_key=mapbox_key)

    st.pydeck_chart(r)



    st.markdown(f'This are the results of the DBSCAN clustering of the accident data for {year}.')

    centroids_filtered = centroids[centroids.year == year]
    clustered_points_filtered = clustered_points[clustered_points.year == year]
    st.write(
        f'Clustered {accidents[accidents.year == year].shape[0]} points down to {centroids_filtered.shape[0]} clusters, for {round(1 - centroids_filtered.shape[0] / accidents[accidents.year == year].shape[0], 2) * 100}% compression.'
    )

    layer1 = pdk.Layer(
        "ScatterplotLayer",
        centroids_filtered,
        pickable=True,
        opacity=0.3,
        stroked=True,
        filled=True,
        radius_scale=200,
        radius_min_pixels=1,
        radius_max_pixels=200,
        line_width_min_pixels=1,
        get_position=['lon', 'lat'],
        get_radius="exits_radius",
        get_fill_color=[0, 102, 204],
        get_line_color=[0, 0, 0],
    )
    layer2 = pdk.Layer(
        "ScatterplotLayer",
        clustered_points_filtered,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=30,
        radius_min_pixels=1,
        radius_max_pixels=20,
        line_width_min_pixels=1,
        get_position=['lon', 'lat'],
        get_radius="exits_radius",
        get_fill_color=[255, 0, 0],
        get_line_color=[0, 0, 0],
    )
    # Set the viewport location
    # view_state = pdk.ViewState(latitude=4.6585, longitude=-74.0935, zoom=12, bearing=0,
    #                            pitch=0)

    # Render
    r1 = pdk.Deck(layers=[layer1, layer2], initial_view_state=view_state,
                 map_style='mapbox://styles/mapbox/dark-v9',
                 mapbox_key=mapbox_key)

    st.pydeck_chart(r1)

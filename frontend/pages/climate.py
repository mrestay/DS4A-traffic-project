import streamlit as st
import pydeck as pdk

def write():
  st.title('Climate')

  # data = borough_data.head(1).to_json()
  # data = '../data/borough.json'
  # st.write(borough_data.head(1)['geometry'].data)
  
  type_g = st.radio('classify by', ['accident_density_population', 'accident_density', 'accident_count'])
  st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=4.480335,
        longitude=-74.083644,
        zoom=10,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
          "GeoJsonLayer",
          "https://ds4a-traffic-accident-project-core.s3.amazonaws.com/datasets/borough.json",
          id="geojson",
          opacity=0.8,
          stroked=False,
          filled=True,
          extruded=True,
          wireframe=True,
          get_elevation=f"properties.{type_g}",
          get_fill_color="[48, 128, properties.accident_density * 255, 255]",
          get_line_color=[255, 255, 255],
        )
    ],
    
  ))

  
import streamlit as st
from widgets import video_youtube
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyAiMEuA9twXdcMskBgO8CzGul1yfUDhz8k')

def write():
  st.title('Model')

  address = st.text_input('Your address', 'terminal')
  geocode_result = gmaps.places(address,(4.6347139,-74.1070325),20000)

  # st.write(geocode_result)

  options_list = [ str(a['name']) +': ' + str(a['formatted_address']) for a in geocode_result['results']]
  # st.write(options_list)
  option = st.selectbox('options:',options_list)
  st.write('You selected:', option.split(': ')[0])

  st.deck_gl_chart(
     viewport={
         'latitude': 4.65,
         'longitude': -74.11,
         'zoom': 11,
         'pitch': 50,
     },
     layers=[{
         'type': 'HexagonLayer',
         # 'data': df,
         'radius': 200,
         'elevationScale': 4,
         'elevationRange': [0, 1000],
         'pickable': True,
         'extruded': True,
     }, {
         'type': 'ScatterplotLayer',
         # 'data': df,
     }])

  # st.date_input

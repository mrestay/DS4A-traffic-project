import streamlit as st
from widgets import video_youtube
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyAiMEuA9twXdcMskBgO8CzGul1yfUDhz8k')

def write():
  st.title('Model')

  address = st.text_input('Your address', 'terminal')
  geocode_result = gmaps.places(address,(4.6347139,-74.1070325),15000)

  # st.write(geocode_result)

  options_list = [ a['name'] for a in geocode_result['results']]
  # st.write(options_list)
  option = st.selectbox('options:',options_list)
  st.write('You selected:', option)
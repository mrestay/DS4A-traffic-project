import streamlit as st
from widgets import video_youtube
from darksky import get_dataframe
import googlemaps
import datetime
import pandas as pd

now = datetime.datetime.now()
gmaps = googlemaps.Client(key='AIzaSyAiMEuA9twXdcMskBgO8CzGul1yfUDhz8k')


def write():
    st.title('Model')

    address = st.text_input('Search for place', 'aeropuerto')
    geocode_result = gmaps.places(address, (4.6347139, -74.1070325), 20000)

    # st.write(geocode_result)

    options_list = [str(ind) + ') ' + str(a['name']) + ': ' + str(a['formatted_address']) for ind, a in
                    enumerate(geocode_result['results'])]
    # st.write(options_list)
    option = st.selectbox('options:', options_list)
    location_dict = geocode_result['results'][int(option[0])]['geometry']['location']
    st.write('You selected:', option.split(': ')[0].split(') ')[1], '\nwith lat: ', location_dict['lat'], 'and long: ', location_dict['lng'])

    date = st.date_input('Choose a date:', now, now + datetime.timedelta(days=30))
    st.write('You selected:', date)

    time = st.selectbox('Choose an hour:', list(range(25)))
    hour = datetime.time(time).strftime("%H:00:00")
    st.write('You selected:', hour)

    datetime_input = str(date) + ' ' + hour
    st.write(datetime_input)
    weather = get_dataframe(location_dict['lat'], location_dict['lng'])
    weather['x'] = location_dict['lat']
    weather['y'] = location_dict['lng']
    st.table(weather[weather.time == datetime_input])
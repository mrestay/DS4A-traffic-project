import streamlit as st
from darksky import get_dataframe
from model_apply import model_apply
import googlemaps
from datetime import datetime, timedelta, time
import pandas as pd
import pydeck as pdk

now = datetime.now()
gmaps = googlemaps.Client(key='AIzaSyAiMEuA9twXdcMskBgO8CzGul1yfUDhz8k')


def write():
    st.title('Interactive traffic accident forecasting')

    address = st.text_input('Search for place', 'aeropuerto')
    geocode_result = gmaps.places(address, (4.6347139, -74.1070325), 20000)

    # st.write(geocode_result)

    options_list = [str(ind) + ') ' + str(a['name']) + ': ' + str(a['formatted_address']) for ind, a in
                    enumerate(geocode_result['results'])]
    # st.write(options_list)
    option = st.selectbox('options:', options_list)
    location_dict = geocode_result['results'][int(option[0])]['geometry']['location']
    st.write('You selected:', option.split(': ')[0].split(') ')[1], '\nwith lat: ', location_dict['lat'], 'and long: ',
             location_dict['lng'])

    date = st.date_input('Choose a date:', value=None, min_value=now, max_value=now + timedelta(days=2))
    st.write('You selected:', date)

    # st.write(geocode_result)

    time_input = st.selectbox('Choose an hour:', [f'{x}:00' for x in range(24)])
    hour = time(int(time_input.split(':')[0])).strftime("%H:%M:00")
    st.write('You selected:', hour)

    datetime_input_string = str(date) + ' ' + str(hour)
    # st.write(datetime_input_string)
    datetime_input_dt = datetime.strptime(datetime_input_string, '%Y-%m-%d %H:%M:%S')
    weather = get_dataframe(location_dict['lat'], location_dict['lng'])
    weather['x'] = location_dict['lat']
    weather['y'] = location_dict['lng']
    weather_filtered = weather[weather.time == datetime_input_string]
    # st.dataframe(weather)

    if now > datetime_input_dt - timedelta(hours=48) and datetime_input_dt > now + timedelta(hours=5):
        if weather_filtered.empty():
            st.write(
                f"""The probability of an accident happening at the location you selected is:
                    {round(model_apply(weather_filtered, 'finalized_model.sav')[0] * 100, 2)}%""")
        else:
            st.write("Please choose another time, the weather API is having trouble forecasting the weather!")
    else:
        st.write('you need to select a time in the next 48 hours UTC time!')
    df = pd.DataFrame([location_dict], columns=['lat', 'lng'])
    df.columns = ['lat', 'lon']

    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=100,
        radius_min_pixels=1,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        get_position=['lon', 'lat'],
        get_radius="exits_radius",
        get_fill_color=[0, 102, 204],
        get_line_color=[0, 0, 0],
    )

    # Set the viewport location
    view_state = pdk.ViewState(latitude=location_dict['lat'], longitude=location_dict['lng'], zoom=11, bearing=0,
                               pitch=0)

    # Render
    r = pdk.Deck(layers=[layer], initial_view_state=view_state,
                 map_style='mapbox://styles/mapbox/dark-v9',
                 mapbox_key="pk.eyJ1IjoiZHM0YWJvZ3RhZzMiLCJhIjoiY2thazhpY3BwMG1nMDJybXEwdXRoMGZkciJ9.6DklXoUDb-sTIyRUUm5Qww")

    st.pydeck_chart(r)

import streamlit as st
from PIL import Image

def write():
  st.title('Traffic accident forecasting in Bogota')

  st.markdown("""
Traffic Accidents are a major cause of death globally. Every year, millions of individuals get injured or die on the roads.
In  Bogota's case, 32,000 traffic accidents on average occur each year, and as a result, 
one person suffers non-fatal injuries every hour and there is one fatality every 16 hours.

In this project, we built a machine learning model that predicts the probability of traffic accidents 
in different locations in Bogota. We hope that this project can contribute to the improvement of road safety.
  """)

  image = Image.open('images/traffic_accident.png')
  st.image(image, use_column_width = True)

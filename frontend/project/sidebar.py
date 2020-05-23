import streamlit as st


year = st.sidebar.slider('Year', 2014, 2019, (2014,2019))
segmentation = st.sidebar.radio('Segmentation', ('Total', 'By Year'))

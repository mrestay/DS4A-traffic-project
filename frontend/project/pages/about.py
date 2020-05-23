import streamlit as st
from ..widgets import video_youtube

def write():
  st.title('General')

  st.markdown("""
    This is an introduction of our project
    
  """)

  video_youtube('https://www.youtube.com/embed/Ni4JGwVbcf0', width=500)
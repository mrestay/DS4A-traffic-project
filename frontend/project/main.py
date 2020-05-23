import streamlit as st
from .pages import general
from .pages import climate
from .pages import cluster
from .pages import accidents

PAGES = {
    "General": general,
    "Cluster": cluster,
    "Climate": climate,
    "Accidents": accidents,
}

def main():
    st.sidebar.title("Accidents Project")
    st.sidebar.subheader("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]

    with st.spinner(f"Loading Page ..."):
        page.write()

    st.sidebar.title("Contribute")
    st.sidebar.info(
        "This an open source project: "
        "[repo](https://github.com/m-restrepo11/DS4A-traffic-project.git) "
    )
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app is made by:
        - Bibiana
        - Juan
        - Mateo
        - Sebastian
"""
    )
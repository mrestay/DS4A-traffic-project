import streamlit as st
import pages.about as about
import pages.general as general
import pages.cluster as cluster
import pages.spatial as spatial
import pages.temporal as temporal
import pages.model as model
import pages.summary as summary

from importlib import reload  

PAGES = {
    "About": about,
    "Summary ": summary,
    "General Analysis": general,
    "Clusters": cluster,
    # "Spatial Analysis": spatial,
    "Temporal Analysis": temporal,
    'Model': model,
}

def main():
    st.sidebar.title("Traffic Accident Forecasting in Bogotá")
    st.sidebar.subheader("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]

    # with st.spinner(f"Loading Page ..."):
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
        - [Bibiana Molina](https://www.linkedin.com/in/nebmolinaze)
        - [Juan Aguilar](https://www.linkedin.com/in/juanguilar)
        - [Mateo Restrepo](https://www.linkedin.com/in/mateorestrepoa)
        - [Sebastian Tabares](https://www.linkedin.com/in/sytabaresa)
"""
    )

if __name__ == "__main__":
    main()
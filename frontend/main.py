import streamlit as st
import pages.about as about
import pages.general as general
import pages.cluster as cluster
import pages.climate as climate
import pages.accidents as accidents
import pages.model as model
import pages.summary as summary
import pages.more as more

from importlib import reload  

PAGES = {
    "About": about,
    "Summary": summary,
    "General Analysis": more,
    # "General": general,
    "Clusters": cluster,
    "Spatial analysis": climate,
    "Accidents": accidents,
    'Model': model,
}

def main():
    st.sidebar.title("Traffic accidents forecasting Project")
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
        - Bibiana Molina
        - Juan Agilar
        - Mateo Restrepo
        - Sebastian Tabares
"""
    )

if __name__ == "__main__":
    main()
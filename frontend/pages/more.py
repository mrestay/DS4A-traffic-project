import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
from data import accidents
from widgets import bubble, tiles

def write():
  menu=['Weather','Accident severity', 'Accident type']
  choice= st.sidebar.selectbox("Type of analysis:", menu)
  st.markdown('Select on the \'type of analysis\' box on the left what you\'d like to see')


  if choice == 'Weather':
        st.title('Weather analysis in traffic accidents')

        #### text about this:
        # st.markdown('Let\'s look at some interesting data on the recorded climate, at the time of traffic accidents.')
        
        ##### calculated the accidents per each summary weather:
        summary=pd.DataFrame(accidents.summary.value_counts()).reset_index(drop=False)
        summary.columns=['weather','accidents']
        #### plotting a bar chart with alt:
        st.subheader('Weather condition vs. number of accidents')
        bars = alt.Chart(summary).mark_bar().encode(
            x='accidents',
            y="weather",opacity=alt.value(0.5),
            color=alt.value('steelblue')
        )
        text = bars.mark_text(align='left',baseline='middle',dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(text='weather')
        (bars + text).properties(height=700)
        st.altair_chart(bars, use_container_width=True)

        #### calculated mean tempeture by month
        m_temperature=accidents[['month','temperature']].groupby('month').agg(['mean','max','min'])#.reset_index(drop=True)
        m_temperature.columns=['mean','max','min']              
        #### calculated mean tempeture by year
        y_temperature=accidents[['year','temperature']].groupby('year').agg(['mean','max','min'])#.reset_index(drop=True)
        y_temperature.columns=['mean','max','min']
        
        ### making the options and plots
        st.header('**Temperature**')
        tempeture = st.radio("Select one",('By month', 'By year'), key = 0)
        if tempeture == 'By month':
              st.subheader('Temperature values for each month')
              st.line_chart(m_temperature)
        else:
              st.subheader('Temperature values for each year')
              st.line_chart(y_temperature)

        #### calculated mean tempeture by precipIntensity
        m_precipIntensity=accidents[['month','precipIntensity']].groupby('month').agg(['mean','max','min'])
        m_precipIntensity.columns=['mean','max','min']
        m_precipIntensity

        #### calculated mean precipIntensity by year
        y_precipIntensity=accidents[['year','precipIntensity']].groupby('year').agg(['mean','max','min'])
        y_precipIntensity.columns=['mean','max','min']
        y_precipIntensity

        ### making the options and plots
        st.header('**Precipitation Intensity**')
        Precipitation = st.radio("Select one",('By month', 'By year'), key = 1)
        if Precipitation == 'By month':
              st.subheader('Precipitation Intensity values for each month')
              st.line_chart(m_precipIntensity)
        else:
              st.subheader('Precipitation Intensity values for each year')
              st.line_chart(y_precipIntensity)
        #############################
        ### calculated relation accident weather and severity
        st.header('**Weather vs. Accident Severity**')
        cross_ws = accidents[['summary', 'severity','population']].groupby(['summary', 'severity']).count().reset_index()
        cross_ws.columns=['weather', 'severity','accidents']
        ### ploting heatmap
        accidecross_ws_chart=nt_type_s= alt.Chart(cross_ws).mark_rect().encode(
        x='severity:O',
        y='weather:O',  
        color=alt.Color('accidents:Q',scale=alt.Scale(scheme='lighttealblue')),
        tooltip=['severity','weather', 'accidents']
        )
        st.altair_chart(accidecross_ws_chart, use_container_width=True)

        #############################
        ### calculated relation accident weather and accident_type
        st.header('**Weather vs. Accident Type**')
        cross_wt = accidents[['summary', 'accident_type','population']].groupby(['summary', 'accident_type']).count().reset_index()
        cross_wt.columns=['weather', 'accident_type','accidents']
        ### ploting heatmap
        accidecross_wt_chart=nt_type_s= alt.Chart(cross_wt).mark_rect().encode(
        x='accident_type:O',
        y='weather:O',  
        color=alt.Color('accidents:Q',scale=alt.Scale(scheme='oranges')),
        tooltip=['accident_type','weather', 'accidents']
        )
        st.altair_chart(accidecross_wt_chart, use_container_width=True)
        
 ###################################################################
  elif choice == 'Accident severity':
        st.title('Accident severity analysis')

        #### text about this:
        # st.markdown('Let''s look at some interesting data on Accident severity analysis')

        ##### calculated the accidents per each severity
        severity=pd.DataFrame(accidents.severity.value_counts()).reset_index(drop=False)
        severity.columns=['severity','accidents']
        severity
                
        #### ploting a bar chart with alt
        st.subheader('Number of accidents for each severity')
        bars2 = alt.Chart(severity).mark_bar().encode(
            x='accidents',
            y="severity",opacity=alt.value(0.5),
            color=alt.value('#7D3C98')
        )
        text = bars2.mark_text(align='left',baseline='middle',dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(text='severity')
        (bars2 + text).properties(height=700)
        st.altair_chart(bars2, use_container_width=True)

        ### calculated accidents by severity and year
        cross_severity_y = accidents[['year', 'severity','population']].groupby(['year', 'severity']).count().reset_index()
        cross_severity_y.columns = ['year', 'severity','accidents']
        ### ploting heatmap
        severity_y= alt.Chart(cross_severity_y).mark_rect().encode(
        x='year:O',
        y='severity:O',  
        color=alt.Color('accidents:Q',scale=alt.Scale(scheme='purples')),
        tooltip=['year','severity', 'accidents']
        )
        #st.altair_chart(severity_y, use_container_width=True)
        ### calculated accidents by severity and month
        cross_severity_m = accidents[['month', 'severity','population']].groupby(['month', 'severity']).count().reset_index()
        cross_severity_m.columns=['month', 'severity','accidents']
        ### ploting heatmap
        severity_m= alt.Chart(cross_severity_m).mark_rect().encode(
        x='month:O',
        y='severity:O',  
        color=alt.Color('accidents:Q',scale=alt.Scale(scheme='purples')),
        tooltip=['month','severity', 'accidents']
        )
        #st.altair_chart(severity_m, use_container_width=True)
        ### making the options and plots
        st.header('**Temporal analysis of accident severity**')
        severity_r = st.radio("Select one",('By month', 'By year'), key = 2)
        if severity_r == 'By month':
              st.subheader('Accident Severity vs. Month')
              st.altair_chart(severity_m, use_container_width=True)
        else:
              st.subheader('Accident Severity vs. Year')
              st.altair_chart(severity_y, use_container_width=True)
        
        ### calculated relation accident type and severity
        st.header('**Accident Type vs. Accident Severity**')
        cross = accidents[['accident_type', 'severity','population']].groupby(['accident_type', 'severity']).count().reset_index()
        cross.columns=['accident_type', 'severity','accidents']
        ### ploting heatmap
        accident_type_s= alt.Chart(cross).mark_rect().encode(
        x='severity:O',
        y='accident_type:O',  
        color=alt.Color('accidents:Q',scale=alt.Scale(scheme='lighttealblue')),
        tooltip=['severity','accident_type', 'accidents']
        )
        st.altair_chart(accident_type_s, use_container_width=True)


      
###################################################################
  elif choice == 'Accident type':
        st.title('Accident type analysis')

        #### text about this:
        # st.markdown('Let''s look at some interesting data on Accident type analysis.')

        ##### calculated the accidents per each severity
        accident_type=pd.DataFrame(accidents.accident_type.value_counts()).reset_index(drop=False)
        accident_type.columns=['accident_type','accidents']
        
                
        #### ploting a bar chart with alt
        st.subheader('Number of accidents for each accident type')
        bars3 = alt.Chart(accident_type).mark_bar().encode(
            x='accidents',
            y="accident_type",opacity=alt.value(0.5),
            color=alt.value('chartreuse')
        )
        text = bars3.mark_text(align='left',baseline='middle',dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(text='accident_type')
        (bars3 + text).properties(height=700)
        st.altair_chart(bars3, use_container_width=True)

        ### calculated accidents by accident_type and year
        cross_accident_type_y = accidents[['year', 'accident_type','population']].groupby(['year', 'accident_type']).count().reset_index()
        cross_accident_type_y.columns=['year', 'accident_type','accidents']
        ### ploting heatmap
        accident_type_y= alt.Chart(cross_accident_type_y).mark_rect().encode(
        x='year:O',
        y='accident_type:O',  
        color=alt.Color('accidents:Q',scale=alt.Scale(scheme='greens')),
        tooltip=['year','accident_type', 'accidents']
        )
        #st.altair_chart(accident_type_y, use_container_width=True)
        ### calculated accidents by accident_type and month
        cross_accident_type_m = accidents[['month', 'accident_type','population']].groupby(['month', 'accident_type']).count().reset_index()
        cross_accident_type_m.columns=['month', 'accident_type','accidents']
        ### ploting heatmap
        accident_type_m= alt.Chart(cross_accident_type_m).mark_rect().encode(
        x='month:O',
        y='accident_type:O',  
        color=alt.Color('accidents:Q',scale=alt.Scale(scheme='greens')),
        tooltip=['month','accident_type', 'accidents']
        )
        #st.altair_chart(accident_type_m, use_container_width=True)
        ### making the options and plots
        st.header('**Temporal analysis of accident type**')
        accident_type_r = st.radio("Select one",('By month', 'By year'))
        if accident_type_r == 'By month':
              st.subheader('Accident Type vs. Month')
              st.altair_chart(accident_type_m, use_container_width=True)
        else:
              st.subheader('Accident Type vs. Year')
              st.altair_chart(accident_type_y, use_container_width=True)
        
        ### calculated relation accident type and severity
        st.header('**Accident Type vs. Accident Severity**')
        cross = accidents[['accident_type', 'severity','population']].groupby(['accident_type', 'severity']).count().reset_index()
        cross.columns=['accident_type', 'severity','accidents']
        ### ploting heatmap
        accident_type_s= alt.Chart(cross).mark_rect().encode(
        x='severity:O',
        y='accident_type:O',  
        color=alt.Color('accidents:Q',scale=alt.Scale(scheme='lighttealblue')),
        tooltip=['severity','accident_type', 'accidents']
        )
        st.altair_chart(accident_type_s, use_container_width=True)
  






  







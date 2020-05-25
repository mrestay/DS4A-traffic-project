import streamlit as st
from data import accidents
import seaborn as sns
from matplotlib import pyplot as plt


def write():
    st.title('What do you want to see?')
    # st.markdown('<style>h1{color: red;}</style>', unsafe_allow_html=True)

    ############################################# by year
    by_year = accidents['year'].value_counts(sort=True).rename_axis('year').reset_index(name='accident_count').sort_values(by='year').reset_index(drop=True)
    by_year
    #st.header('Yearly accidents.')
    if st.button('Yearly accidents'):
        placeholder1 = st.empty()
        if not st.checkbox("Hide Yearly accidents."):
            f, ax = plt.subplots(figsize=(27, 12))
            sns.set(style="whitegrid",font_scale=2)
            ticks = [x for x in range(2015, 2020)]
            sns.lineplot(by_year.year, by_year.accident_count, color='red')
            plt.xlabel('Year')
            plt.xticks( ticks, rotation=90)
            plt.ylabel('Number of Accidents')
            st.pyplot()
    else:
        st.write(' ')   

    #############################################
    #st.header('Percent change in yearly accidents.')   
    if st.button('Percent change in yearly accidents'):
        placeholder1 = st.empty()
        if not st.checkbox("Hide Percent change in yearly accidents"):
            by_year['percent_change'] = by_year.accident_count.pct_change()
            f, ax = plt.subplots(figsize=(27, 12))
            sns.set(style="whitegrid",font_scale=2)
            ticks2 = [x for x in range(2015, 2020)]              
            sns.lineplot(by_year.year, by_year.percent_change, color='b')
            plt.title('Percent change in yearly accidents', fontsize =20)
            plt.xlabel('Year')
            plt.xticks( ticks2, rotation=90)
            plt.ylabel('Number of Accidents')
            st.pyplot()
    else:
        st.write(' ') 
    ###############################################

    ############################################# by month
    by_month = accidents['month'].value_counts(sort=True).rename_axis('month').reset_index(name='accident_count').sort_values(by='month').reset_index(drop=True)
    months={1:'January',2:'February',3:'March',4:'April',
        5:'May',6:'June',7:'July',8:'August',
        9:'September',10:'October',11:'November',12:'December'}
    #st.header('month accidents.')
    if st.button('Monthly accidents'):
        placeholder1 = st.empty()
        if not st.checkbox("Hide monthly accidents."):
            f, ax = plt.subplots(figsize=(27, 12))
            sns.set(style="whitegrid",font_scale=2)
            ticks = [months[x] for x in range(1, 13)]
            sns.lineplot(by_month.month, by_month.accident_count, color='red')
            plt.xlabel('month')
            plt.xticks(range(1, 13), ticks, rotation=90)
            plt.ylabel('Number of Accidents')
            st.pyplot()
    else:
        st.write(' ')   
    
    ###############################################
    ############################################# by month
    by_day_of_week = accidents['day_of_week'].value_counts(sort=True).rename_axis('day_of_week').reset_index(name='accident_count').sort_values(by='day_of_week').reset_index(drop=True)
    day_of_weeks={1:'Monday',2:'Tuesday',3:'Wednesday',
        4:'Thursday',5:'Friday',6:'Saturday',7:'Sunday'}
    #st.header('day_of_week accidents.')
    if st.button('Accidents by day of week.'):
         placeholder1 = st.empty()
         if not st.checkbox("Hide day_of_weekly accidents."):
            f, ax = plt.subplots(figsize=(27, 12))
            sns.set(style="whitegrid",font_scale=2)
            ticks2 = [day_of_weeks[x] for x in range(1, 8)]
            sns.lineplot(by_day_of_week.day_of_week, by_day_of_week.accident_count, color='red')
            plt.xlabel('day_of_week')
            plt.xticks(range(0, 8), ticks2, rotation=90)
            plt.ylabel('Number of Accidents')
            st.pyplot()
    else:
        st.write(' ') 

    ############################################# by hour
    by_hour = accidents['hour'].value_counts(sort=True).rename_axis('hour').reset_index(name='accident_count').sort_values(by='hour').reset_index(drop=True)

    #st.header('hour accidents.')
    if st.button('Accidents by hour.'):
         placeholder2 = st.empty()
         if not st.checkbox("Hide hourly accidents."):
            f, ax = plt.subplots(figsize=(27, 12))
            sns.set(style="whitegrid",font_scale=2)
            sns.lineplot(by_hour.hour, by_hour.accident_count, color='red')
            plt.xlabel('hour')
            plt.ylabel('Number of Accidents')
            st.pyplot()
    else:
        st.write(' ') 





import streamlit as st
#from ingest import ingest_predicted_reviews, data_file
import pandas as pd
from datetime import datetime
import numpy as np

#################################################################
################## Page Settings ################################
#################################################################
st.set_page_config(page_title="My Streamlit App", layout="wide")
st.markdown('''
<style>
    #MainMenu
    {
        display: none;
    }
    .css-18e3th9, .css-1d391kg
    {
        padding: 1rem 2rem 2rem 2rem;
    }
</style>
''', unsafe_allow_html=True)

#################################################################
################## Page Header ##################################
#################################################################
st.header("Predicting Avocado Average Price")
st.write("Our application uses Artificial Intelligence to predict avocado average price during the preiod of 2015 to 2018")
st.markdown('---')

################## Sidebar Menu #################################
page_selected = st.sidebar.radio("Menu", ["Home", "Model"])

################################################################
################## Home Page ###################################
################################################################
data_file = "avocado.csv"


if page_selected == "Home":
        ######### Load labeled data from datastore #################
    df = pd.read_csv(data_file)
    ######### Year range slider ################################
    start, end = st.sidebar.select_slider(
                    "Select year Range", 
                    df.year.drop_duplicates().sort_values(), 
                    value=(df.year.min(), df.year.max()))

    ######### Avocado Ctegory Filter ################################
    region = st.sidebar.selectbox("region", ['All', 'LosAngeles', 'NewYork', 'Plains'])

    ######### Apply filters ####################################
    df_filter = df.loc[(df.year >= start) & (df.year <= end), :]
    if region != "All":
        df_filter = df_filter.loc[df_filter.region == region, :]
    
    if df_filter.shape[0] > 0:
    ######### Main Story Plot ###################################
        col1, col2 = st.columns((2,1))
        with col1: 
            ax = pd.crosstab(df_filter.year, df_filter.type).plot(
                    kind="bar", 
                    figsize=(6,2), 
                    xlabel = "year",
                    color={'conventional':'skyblue', 'organic': 'orange'})
            st.pyplot(ax.figure)
        with col2:
            st.write('This plot shows the sales of different categories of avocado during year 2015-2018 of Top 3 cities. It is clearly that the traditional conventional avocado still takes the dominant part of the market. Although organic avocado is more expensive, People in rich cities tend to choose healthy product.')
        st.markdown('---')

        ######### Length vs Hour Plot ###################################
        col1, col2 = st.columns((2,1))
        with col1: 
            ax = df_filter.plot.scatter(x='year', y='AveragePrice', figsize=(6,2))
            st.pyplot(ax.figure)
        with col2:
            st.write('This scatter plot shows the average price changes during 2015-2018. The price variation trend follows the sales trend.')
        st.markdown('---')

################################################################
############### Model Training and Evaluation ##################
################################################################
elif page_selected == "Model":
    st.subheader("Training and Model Evalutaion")
    col1,col2 = st.columns(2)
    with col1:
        st.image('final_result.png')
    with col2:
        st.write('With correlation analysis, we can find: 1. The average unit price is negatively correlated with the total sales. 2. The total sales volume is positively correlated with the total number of packaging bags (The larger the sales volume, the more the number of packaging bags)3. Average unit price is correlated with the type of avocado.')

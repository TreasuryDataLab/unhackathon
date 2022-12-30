import streamlit as st
import pandas as pd
import base64
import requests
from datetime import date
import json
import plotly.express as px
import pickle

LOGO_IMAGE = "./sdg.png"
#Read the Data
data_read = pd.read_excel('All Data.xlsx',engine='openpyxl')
data = data_read[(data_read.Country != "Dominica")]
#Disable Warning
#st.set_option('deprecation.showPyplotGlobalUse', False)
#Import model
model = pickle.load(open('finalized_model.sav', 'rb'))

st.markdown(
    f"""
    <div style="text-align: center;">
    <img class="logo-img" src="data:png;base64,{base64.b64encode(open(LOGO_IMAGE, 'rb').read()).decode()}">
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<h1 style='text-align: center; color: #F9F6EE; font-family:sans-serif'>Projecting the Impact of Conflict and Blockages, Preventing Malnourishment</h1>", unsafe_allow_html=True) 
menu = st.sidebar.selectbox("Select Menu", ("Clustering","Prediction"))
if menu == "Clustering":
    st.write("### Clustering")
    year = st.selectbox("Year",data.Year.unique())
    fig1 = px.scatter(data[(data.Year == int(year))], x="Prevalence of Undernourishment (%)", y="Food Price Index (May)", color="Agri to GDP t-1 (%)",
                    size="GDP per Capita t-1 (Current US$)",text='Country')
    fig1.update_layout(title="Clustering Food Price in the World")
    st.plotly_chart(fig1, use_container_width=True)
    col1,col2, col3 = st.columns(3)
    year_1 = int(year) - 1
    with col1:
        gap = data[(data.Year == int(year))]["Prevalence of Undernourishment (%)"].mean() - data[(data.Year == int(year_1))]["Prevalence of Undernourishment (%)"].mean()
        st.metric(label="Prevalance of Undernourishment " + str(year), value='{0:.2f}'.format(data[(data.Year == int(year))]["Prevalence of Undernourishment (%)"].mean()),
        delta = '{0:.2f}'.format(gap))
        if gap < 0 :
            st.write("Minus " + str('{0:.2f}'.format(gap)) + " from " + str(year_1))
        else :
            st.write("Plus "+ str('{0:.2f}'.format(gap)) + " from " + str(year_1))
    with col3:
        gap = data[(data.Year == int(year))]["Food Price Index (May)"].mean() - data[(data.Year == int(year_1))]["Food Price Index (May)"].mean()
        st.metric(label = "Food Price Index " + str(year),value = '{0:.2f}'.format(data[(data.Year == int(year))]["Food Price Index (May)"].mean()),
        delta = '{0:.2f}'.format(gap))
        if gap < 0 :
            st.write("Minus " + str('{0:.2f}'.format(gap)) + " from " + str(year_1))
        else :
            st.write("Plus "+ str('{0:.2f}'.format(gap)) + " from " + str(year_1))
    col4,col5,col6 = st.columns(3)
    with col4:
        gap = data[(data.Year == int(year))]["Agri to GDP t-1 (%)"].mean() - data[(data.Year == int(year_1))]["Agri to GDP t-1 (%)"].mean()
        st.metric(label="Agricultural to GDP " + str(year), value='{0:.2f}'.format(data[(data.Year == int(year))]["Agri to GDP t-1 (%)"].mean()),
        delta = '{0:.2f}'.format(gap))
        if gap < 0 :
            st.write("Minus " + str('{0:.2f}'.format(gap)) + " from " + str(year_1))
        else :
            st.write("Plus "+ str('{0:.2f}'.format(gap)) + " from " + str(year_1))
    with col6:
        gap = data[(data.Year == int(year))]["GDP per Capita t-1 (Current US$)"].mean() - data[(data.Year == int(year_1))]["GDP per Capita t-1 (Current US$)"].mean()
        st.metric(label = "GDP per Capita " + str(year),value = '{0:.2f}'.format(data[(data.Year == int(year))]["GDP per Capita t-1 (Current US$)"].mean()),
        delta = '{0:.2f}'.format(gap))
        if gap < 0 :
            st.write("Minus " + str('{0:.2f}'.format(gap)) + " from " + str(year_1))
        else :
            st.write("Plus "+ str('{0:.2f}'.format(gap)) + " from " + str(year_1))
if menu == "Prediction":
    st.write("### Prediction")
    country = st.selectbox("Choose country",data.Country.unique())
    col1,col2,col3 = st.columns(3)
    with col1:
        gdp = st.number_input('Input GDP per Capita(US$)',value=data[(data.Country == country) & (data.Year == 2022)]['GDP per Capita t-1 (Current US$)'].values[0])
    with col3:
        fpi = st.number_input('Input Food Price Index',value=data[(data.Country == country) & (data.Year == 2022)]['Food Price Index (May)'].values[0])
    col4,col5,col6 = st.columns(3)
    with col4:
        agri = st.number_input('Input Agricultural share of GDP (%)',value=data[(data.Country == country) & (data.Year == 2022)]['Agri to GDP t-1 (%)'].values[0])
    with col6:
        mer = st.number_input('Agricultural Share of Merchandise Import (%)',value = data[(data.Country == country) & (data.Year == 2022)]['Agri Raw Materials Import to Total Merchandise Import t-1 (%)'].values[0])
    data_pred = pd.DataFrame({
        "country" : country,
        "GDP per Capita t-1 (Current US$)" : gdp,
        "Food Price Index (May)" : fpi,
        "Agri to GDP t-1 (%)" : agri,
        "Agri Raw Materials Import to Total Merchandise Import t-1 (%)" : mer
    }, index=[0])
    st.write("The data for predict is below : ")
    st.write("### Country : " + country)
    col1,col2, col3 = st.columns(3)
    with col1:
        st.write('GDP per Capita : ' + '{0:.2f}'.format(gdp))
    with col3:
        st.write('Food Price Index : ' + '{0:.2f}'.format(fpi))
    col4,col5,col6 =  st.columns(3)
    with col4:
        st.write('Input Agricultural share of GDP (%) : ' + '{0:.2f}'.format(agri))
    with col6:
        st.write('Input Agricultural Share of Merchandise Import (%) : ' + '{0:.2f}'.format(mer))
    if st.button('Predict'):
        pred = model.predict(data_pred.drop(['country'],axis=1))
        st.write("Predicted of Prevalance Undernourishment in " + str(country) + " is " + str('{0:.2f}'.format(pred[0])))

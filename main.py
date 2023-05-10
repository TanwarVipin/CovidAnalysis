import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import streamlit as st
import Helper, Preprocess

st.set_page_config(layout="wide")

st.markdown("""
<style>
.big-font {
    font-size:500px !important;
}
</style>
""", unsafe_allow_html=True)

df = pd.read_csv(r'data/covid_worldwide.csv')
covid = pd.read_csv(r'WHO-COVID-19-global-data.csv')
df1 = Preprocess.preprocess(df)
country = Helper.country(df1)
st.sidebar.image('https://www.sakraworldhospital.com/spl_splimgs/antigen-test-labs-bangalore.jpg')
# st.header('Covid 19 Country Wise Analysis')
col1, col2, col3 = st.columns(3, gap='large')
col4, col5 = st.columns(2, gap='medium')
select_country = st.sidebar.selectbox('Select Country', country)
table = Helper.get1(df1, select_country)
table2 = Helper.get(df1, select_country)
if select_country == 'Overall':
    with col1:
        st.header('Total World Population')
        st.write(table.sum()[5])
    with col2:
        st.header('Total World Covid Cases')
        st.write(table.sum()[0])
    with col3:
        st.header('Total Recovered')
        st.write(table.sum()[2])
    with col4:
        st.header('Total Active Cases Worldwide')
        st.write(table.sum()[3])
    with col5:
        st.header('Total Deaths Worldwide')
        st.write(table.sum()[1])
else:
    st.title('Covid Analysis of ' + select_country)
    with col1:
        cols = table2.columns.tolist()
        st.header('Total Population')
        st.write(table2[cols[5]][0])
    with col2:
        st.header('Total Cases')
        st.write(table2[cols[0]][0])
    with col3:
        st.header('Total Recovered')
        st.write(table2[cols[2]][0])
    with col4:
        st.header('Active Cases')
        st.write(table2[cols[3]][0])
    with col5:
        st.header('Total Deaths')
        st.write(table2[cols[1]][0])
x = Helper.get1(df1, select_country)
if select_country == 'Overall':
    x = x.sum().reset_index().rename(columns={'index': 'Stats', 0: 'Count'})
    fig = px.bar(x, x='Stats', y='Count', log_y=True)
    fig.update_layout({'title': 'World Wide Analysis'})
    st.plotly_chart(fig)
else:
    fig = px.bar(x, x='Stats', y='Count', log_y=True)
    fig.update_layout({'title': 'Analysis By CountryWise'})
    st.plotly_chart(fig)
data = Preprocess.preprocess1(covid)
if select_country == 'Overall':
    x = data.groupby('Year', as_index=False)[['New_cases', 'New_deaths']].sum()
    fig = px.bar(x, x='Year', y=['New_cases', 'New_deaths'], barmode='group', log_y=True)
    fig.update_layout({
        'title': 'Death and Cases Year Wise'
    })
    st.plotly_chart(fig)
else:
    x, y = Helper.get2(data, select_country)
    fig = px.line(x, y=['New_deaths', 'Cumulative_deaths'], log_y=True)
    fig.update_layout({
        'title': 'Death Trend on Date'
    })
    st.plotly_chart(fig)
    fig1 = px.line(y, y=['New_cases', 'Cumulative_cases'], log_y=True)
    fig1.update_layout({
        'title': 'New Cases Trend on Date'
    })
    st.plotly_chart(fig1)
year = data.Year.unique().tolist()
select_year = st.sidebar.selectbox('Select Year', year)
data1, data2 = Helper.get3(data, select_country, select_year)
if select_country == 'Overall':
    st.title('Top 10  Cases Nation in ' + str(select_year))
    fig = px.bar(data1, x='Country', y='New_cases', log_y=True)
    st.plotly_chart(fig)
    st.title('Top 10  Deaths Nation in ' + str(select_year))
    fig1 = px.bar(data2, x='Country', y='New_deaths', log_y=True)
    st.plotly_chart(fig1)
else:
    st.title('Cases Trend of ' + select_country + 'in' + str(select_year) + 'Over Month')
    fig = px.line(data1, x='Month', y=['New_cases', 'Cumulative_cases'], log_y=True)
    st.plotly_chart(fig)
    st.title('Deaths Trend of' + select_country + 'in' + str(select_year) + 'Over Month')
    fig1 = px.line(data2, x='Month', y=['New_deaths', 'Cumulative_deaths'], log_y=True)
    st.plotly_chart(fig1)

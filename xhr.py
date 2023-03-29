import streamlit as st
import pandas as pd
from datetime import datetime as dt

st.set_page_config(page_title="Xhr Analysis",
                   page_icon=":bar_chart:",
                   layout="wide")

if 'count' not in st.session_state:
    st.session_state.count = 0

@st.cache_resource(show_spinner=False, ttl=60*60*24)
def get_df():
    df = pd.read_csv('https://github.com/enzobo/analysis/blob/main/xhr.py?raw=true')
    return df

def add_count():
    st.session_state.count = 1

def reset_count():
    st.session_state.count = 0


streamlit_df = get_df()

col1, col2, col3, col4 = st.columns([1,1,1,3])

with col1:
    app = st.selectbox(label='Application Category',
                       options= streamlit_df.app.unique(),
                       on_change=reset_count)
with col2:
    plat_l1 = st.selectbox(label='Platform L1',
                           options= streamlit_df.query('app == @app').l1.unique())
with col3:
    plat_l3 = st.selectbox(label='Platform L3',
                           options= streamlit_df.query('app == @app and l1 == @plat_l1').l3.unique())
with col4:
    url = st.text_input(label='URL Input')

with col1:
    country = st.selectbox(label='Countries',
                           options= streamlit_df.query('app == @app and l1 == @plat_l1 and l3 == @plat_l3').country.unique())
with col2:
    device = st.selectbox(label='Device Types',
                          options= streamlit_df.query('app == @app and l1 == @plat_l1 and l3 == @plat_l3 and country == @country').device.unique())
with col3:
    dts = st.date_input(label='Date Range: ',
                value=(dt(year=2022, month=5, day=20, hour=16, minute=30), 
                        dt(year=2022, month=5, day=30, hour=16, minute=30)))
    
generate_analysis = st.button('Generate Report', on_click=add_count)

if st.session_state.count > 0:
    st.dataframe(streamlit_df.query('app == @app and l1 == @plat_l1 and l3 == @plat_l3 and country == @country and device == @device'))

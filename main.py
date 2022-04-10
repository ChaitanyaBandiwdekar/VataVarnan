import my_component 
import climate
import news
import streamlit as st
from PIL import Image


PAGES = {
    "Weather": my_component,
    "Climate": climate,
    "News": news
}

st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

image = Image.open('logo.jpeg')
st.image(image)

st.sidebar.title('Criteria')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
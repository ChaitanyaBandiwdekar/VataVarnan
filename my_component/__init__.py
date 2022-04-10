import os
import click
import streamlit as st
import streamlit.components.v1 as components
import requests

_RELEASE = False
st.set_page_config(page_title='VataVarnan')

if not _RELEASE:
    _component_func = components.declare_component(
        "my_component",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("my_component", path=build_dir)


def my_component(key=None):
    component_value = _component_func(key=key, default=0)
    return component_value


def app():
    if not _RELEASE:
        msg = 'Select a location to view weather details!'
        st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
        st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])

        with col1:
            col1.header("Select location ")
            clicked_coords = my_component()
            

        with col2:
            col2.header("Weather ")
            if type(clicked_coords) is dict:
                latitude = clicked_coords.get('lat', 25)
                longitude = clicked_coords.get('lng', 25)
                r = requests.get(f"http://127.0.0.1:5000/weather?lat={latitude}&lon={longitude}")

                days = r.json()['data']
                st.subheader('Today')
                st.write('Weather is ', days[0][1], ' today')
                st.write('Max temp: ', days[0][2], ' °C')
                st.write('Min temp: ', days[0][3], ' °C')
                st.subheader('Following days')
                for x in days[1:]:
                    date = str(x[0])
                    st.write(date[6:], '/', date[4:6], '/', date[0:4], ' - ', x[1], ' - ', x[2] , '/', x[3])
                    print(x)

            else:
                st.write('Please select a location to view weather details!')

        
        
        # print(clicked_coords)
        
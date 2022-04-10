from msilib.schema import Component
from turtle import title
import requests
import streamlit as st
import streamlit.components.v1 as components


def app():
    st.header('News Section')
    url = "https://climate-change-news48.p.rapidapi.com/news/tnyt"

    headers = {
        "X-RapidAPI-Host": "climate-change-news48.p.rapidapi.com",
        "X-RapidAPI-Key": "0479b7e2f0msh10a9a16ca3b31b7p195d78jsn59ce49f41572"
    }

    response = requests.request("GET", url, headers=headers).json()
    print(response)
    # st.text(response.title)
    components.html("""<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
            <div class="card p-4 bordered rounded">
        <div class="card-body">
        <h5 class="card-title">{title}</h5>
        <h6 class="card-subtitle mb-2 text-muted">{source}</h6>
        <a href="{url}" class="card-text">{url}</a> </div>
        </div>

        <div class="card p-4">
        <div class="card-body">
        <h5 class="card-title">{title1}</h5>
        <h6 class="card-subtitle mb-2 text-muted">{source1}</h6>
        <a href="{url1}" class="card-text">{url1}</a> </div>
        
        </div>
        
        """.format(
                title = response[0]['title'],
                source = response[0]['source'],
                url = response[0]['url'],
                title1 = response[1]['title'],
                source1 = response[1]['source'],
                url1 = response[1]['url'],
                ), width=600, height=525)

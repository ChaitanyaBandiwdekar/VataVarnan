import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static;
from geopy.geocoders import Nominatim


def app():
    geolocator = Nominatim(user_agent="climate")


    st.header('Climate')

    option = st.selectbox('Measures', ('Methane Emissions', 'Air Quality Index', 'Arctic Ice Cover'))

    if (option == 'Arctic Ice Cover'):
        st.markdown("""

        <p>
        <h4>Arctic Ice Cover</h4>
        The sea ice cover is one of the key components of the polar climate system. It has been a focus of attention in recent years, largely because of a strong decrease in the Arctic sea ice cover and modeling results that indicate that global warming could be amplified in the Arctic on account of ice-albedo feedback. This results from the high reflectivity (albedo) of the sea ice compared to ice-free waters. 
        </p>
        <p>
        A satellite-based data record starting in late 1978 shows that indeed rapid changes have been occurring in the Arctic, where the ice coverage has been declining at a substantial rate. In contrast, in the Antarctic the sea ice coverage has been increasing although at a lesser rate than the decreases in the Arctic.
        </p>
        <p>
        The graph below shows the gradual decrease in the area and extent of the arctic ice cover from 1979 to 2019:
        </p>
        """
        , 
        unsafe_allow_html=True)

        data = requests.get('http://127.0.0.1:5000/ice-cover')
        ice_data = data.json()['data']
        # print(data.json().data)
        print(ice_data)
        years = []
        data_arr = []

        for year in ice_data:
            years.append(year)
            data_arr.append([ice_data[year][0], ice_data[year][1]])
        
        chart_data = pd.DataFrame(
        data_arr, years,
        columns=['Area', 'Extent'])

        st.line_chart(chart_data)


    elif(option == "Air Quality Index"):
        clist = requests.get("http://127.0.0.1:5000/air-quality/get-countries").json()['countries']
        country = st.sidebar.selectbox("Select a country:", clist)

        if (country):
            print(country)
            query_params = {'country': country}
            slist = requests.get('http://127.0.0.1:5000/air-quality/get-states', params=query_params).json()['states']
            print(slist)
            state = st.sidebar.selectbox("Select a state:", slist)
            query_params = {'country': country, 'state': state}
            location = geolocator.geocode(state)
            m = folium.Map(location=[location.latitude, location.longitude], zoom_start=6)
        
            aqi_data = requests.get('http://127.0.0.1:5000/air-quality/get-aqi', params=query_params).json()
            print(aqi_data)

            feature_group = folium.FeatureGroup("Locations")
            for key, value in aqi_data.items():
                location2 = geolocator.geocode(key)                                  
                # folium.Marker([location2.latitude,location2.longitude], popup=aqi_data[data]).add_to(m)
                feature_group.add_child(folium.Marker(location=[location2.latitude,location2.longitude],popup=value))
            
            m.add_child(feature_group)
            # m.save('text23.html')
            folium_static(m)


        st.markdown("""
        <p>
        <h4>Air Quality Index</h4>
        An air quality index (AQI) is used by government agencies to communicate to the public how polluted the air currently is or how polluted it is forecast to become. Public health risks increase as the AQI rises. Different countries have their own air quality indices, corresponding to different national air quality standards.
        </p>
        <p>
        Computation of the AQI requires an air pollutant concentration over a specified averaging period, obtained from an air monitor or model. Taken together, concentration and time represent the dose of the air pollutant. Health effects corresponding to a given dose are established by epidemiological research.[4] Air pollutants vary in potency, and the function used to convert from air pollutant concentration to AQI varies by pollutant. Its air quality index values are typically grouped into ranges. Each range is assigned a descriptor, a color code, and a standardized public health advisory. 
        The AQI can increase due to an increase of air emissions (for example, during rush hour traffic or when there is an upwind forest fire or from a lack of dilution of air pollutants. Stagnant air, often caused by an anticyclone, temperature inversion, or low wind speeds lets air pollution remain in a local area, leading to high concentrations of pollutants, chemical reactions between air contaminants and hazy conditions.
        </p>
        """
        , 
        unsafe_allow_html=True)


    elif (option == "Methane Emissions"):
        st.markdown("""
        <p>
        <h4>Methane</h4> Methane is the primary contributor to the formation of ground-level ozone, a hazardous air pollutant and greenhouse gas, exposure to which causes 1 million premature deaths every year. Methane is also a powerful greenhouse gas. Over a 20-year period, it is 80 times more potent at warming than carbon dioxide.
        </p>
        <p>
        Methane has accounted for roughly <b>30</b> per cent of global warming since pre-industrial times and is proliferating faster than at any other time since record keeping began in the 1980s. In fact, according to data from the United States National Oceanic and Atmospheric Administration, even as carbon dioxide emissions decelerated during the pandemic-related lockdowns of 2020, atmospheric methane shot up.
        </p>
        <p>
        The following line graph shows the steady increase of methane emissions (in parts per million):
        </p>
        """
        , 
        unsafe_allow_html=True)
        
        data = requests.get('http://127.0.0.1:5000/methane').json()['data']
        print(data)

        year = []
        methane_value = []
        for i in data:
            year.append(str(int(float(i))))
            methane_value.append(data[i])
        

        chart_data = pd.DataFrame(
            methane_value,
        year)


        st.line_chart(chart_data)

        st.markdown("""
        <p>
        Until recently, little was known about where leaks were occurring, or the best way to fix them. In 2012, we kicked off a research series to better pinpoint leaks — and to find solutions. It is the largest body of peer-reviewed research on the issue.

        A synthesis of the research found that the U.S. oil and gas industry was emitting at least 13 million metric tons of methane a year — about 60% more than the Environmental Protection Agency estimated at the time. The volume represents enough natural gas to fuel 10 million homes.

        Today we have much better data on where the methane is coming from and how to prevent it. Ground-based measurement tools along with a growing number of satellites — including one being launched by our MethaneSAT subsidiary — are making it faster and cheaper than ever to locate, measure and reduce emissions.

        In fact, the International Energy Agency estimates that worldwide, the oil and gas industry can achieve a 75% reduction using technologies available today — two-thirds of it at no net cost.


        </p>
        """
        , 
        unsafe_allow_html=True)

        


    




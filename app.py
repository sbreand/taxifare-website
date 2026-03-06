import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

@st.cache_data
def geocode_address(address, geocoder):
    """Adresse texte → latitude, longitude"""
    try:
        location = geocoder.geocode(address + ", New York, NY")
        return (location.latitude, location.longitude) if location else None
    except:
        return None

geocoder = Nominatim(user_agent="taxifare-website")





def adresse_to_coords(adresse):
    geolocator = Nominatim(user_agent="taxi_app")
    location = geolocator.geocode(adresse + ", New York, NY")

    if location:  # location est un objet Location
        return (location.latitude, location.longitude)  # tuple (float, float)
    return None

# Utilisation
start = adresse_to_coords("Times Square")  # (40.7580, -73.9855)




st.title("🚕 NY Taxi Fare Predictor")

st.markdown("""
Please fill this form
""")


col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Pickup")
    pickup_adress = st.text_input("Pickup")
    pickup_date = st.date_input("Date:", format="YYYY/MM/DD")
    pickup_time = st.time_input("Time:")
    #pickup_longitude = st.number_input("Longitude:", value=-73.950655)
    #pickup_latitude = st.number_input("Latitude:", value=40.783282)


with col2:
    st.subheader("🎯 Dropoff")
    dropoff_adress = st.text_input("Dropoff")
    #dropoff_longitude = st.number_input("Longitude:", value=-73.984365)
    #dropoff_latitude = st.number_input("Latitude:", value=40.769802)
    passenger_count = st.number_input("Passengers:", min_value=1, max_value=6, value=1)

if st.button("🔮 Predict", type="primary"):
    pickup_datetime =f'{pickup_date} {pickup_time}'


    # Utilisation
    start = adresse_to_coords(pickup_adress)  # (40.7580, -73.9855)
    pickup_latitude = start[0]
    pickup_longitude = start[1]

    end = adresse_to_coords(dropoff_adress)
    dropoff_latitude = end[0]
    dropoff_longitude = end[1]

    params = dict(
    pickup_datetime=pickup_datetime,
    pickup_longitude=pickup_longitude,
    pickup_latitude=pickup_latitude,
    dropoff_longitude=dropoff_longitude,
    dropoff_latitude=dropoff_latitude,
    passenger_count=passenger_count)


    #response = requests.get('https://taxifare.lewagon.ai/predict', params = params)

    response = requests.get('https://taxifare-393521676533.europe-west1.run.app/predict', params = params)
    result = response.json()['fare']

    st.success(f"💰**Estimated fare: {result:.2f} USD**")

    map_data = pd.DataFrame({
                "lat": [pickup_latitude, dropoff_latitude],
                "lon": [pickup_longitude, dropoff_longitude],
                "type": ["🚕 Pickup", "🎯 Dropoff"]
            })
    st.map(map_data, zoom=13)

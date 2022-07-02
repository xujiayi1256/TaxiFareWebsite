from datetime import datetime

import requests
import streamlit as st
# importing geopy library
from geopy.geocoders import Nominatim

# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")

'''
# TaxiFareModel front
'''

d = st.date_input("Pickup Date")
t = st.time_input('Pickup Time')
dt = datetime.combine(d, t)

print(dt)

dt = datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
st.write('Pickup time:', dt)

pickup = st.text_input('Pickup Location', placeholder='Enter your pickup location',
                       value='Madison Square Garden, New York')
if pickup:
    pickupLoc = loc.geocode(pickup)
    if pickupLoc:
        st.write('Pickup Adderss:', pickupLoc.address)
        st.write("Latitude = ", pickupLoc.latitude, "\n")
        st.write("Longitude = ", pickupLoc.longitude)

dropoff = st.text_input('Dropoff Location', placeholder='Enter your dropoff location',
                        value='Trump Tower, New York')
if dropoff:
    dropoffLoc = loc.geocode(dropoff)
    if dropoffLoc:
        st.write('Dropoff Adderss:', pickupLoc.address)
        st.write("Latitude = ", dropoffLoc.latitude, "\n")
        st.write("Longitude = ", dropoffLoc.longitude)

passenger = st.slider('passenger count', 1, 4, 1)

if st.button('Predict'):
    data = {
        'pickup_datetime': dt,
        'pickup_longitude': pickupLoc.longitude,
        'pickup_latitude': pickupLoc.latitude,
        'dropoff_longitude': dropoffLoc.longitude,
        'dropoff_latitude': dropoffLoc.latitude,
        'passenger_count': passenger
    }
    response = requests.get("https://taxifare.lewagon.ai/predict", params=data)
    if response.ok:
        st.header('Fare: $' + str(round(response.json()['fare'], 2)))
    elif response.status_code == 400:
        st.header("Something went wrong")

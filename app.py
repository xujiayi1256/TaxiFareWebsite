from datetime import datetime

import requests
import streamlit as st
# importing geopy library
from geopy.geocoders import Nominatim

# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")

'''
# New York Taxi Fare Estimator
'''

d = st.date_input("Pickup Date")
t = st.time_input('Pickup Time')
dt = datetime.combine(d, t)

dt = datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
st.write('Pickup time:', dt)

pickup = st.text_input('Pickup Location', placeholder='Enter your pickup location',
                       value='Madison Square Garden, New York')
pickupLoc = None
if pickup:
    try:
        pickupLoc = loc.geocode(pickup)
    except:
        pass
    if pickupLoc:
        st.write('Pickup Address:', pickupLoc.address)
        st.write("Latitude = ", pickupLoc.latitude, )
        st.write("Longitude = ", pickupLoc.longitude)

dropoff = st.text_input('Drop Off Location', placeholder='Enter your drop off location',
                        value='Trump Tower, New York')
dropoffLoc = None
if dropoff:
    try:
        dropoffLoc = loc.geocode(dropoff)
    except:
        pass
    if dropoffLoc:
        st.write('Drop Off Address:', dropoffLoc.address)
        st.write("Latitude = ", dropoffLoc.latitude)
        st.write("Longitude = ", dropoffLoc.longitude)

passenger = st.slider('passenger count', 1, 4, 1)

if st.button('Predict') and pickupLoc and dropoffLoc:
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
        st.header('Fare Estimate: $' + str(round(response.json()['fare'], 2)))
    elif response.status_code == 400:
        st.header("Something went wrong")
else:
    st.header("Something went wrong")

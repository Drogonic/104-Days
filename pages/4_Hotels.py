import streamlit as st
import pandas as pd
import datetime
import json
import main_functions
import requests
st.set_page_config(layout="wide")
#Logo image
st.image("104dayslogo.png", width=300)



def hotel_details(counter, hotels, loops):
    for i in range(loops):
        if counter == 6 or counter == 15 or counter == 24:
            print(" ")
        else:
            new_width = int(hotels[counter]['image_width'] * 180 / hotels[counter]['image_height'])
            st.image(hotels[counter]['image'], width=new_width)
            st.caption("Rating: " + hotels[counter]['rating'])
            with st.expander(hotels[counter]['name']):
                st.caption("[Website](hotels[counter]['website'])")
                st.caption("Ranking:" + hotels[counter]['ranking'])
                st.caption("Price:" + hotels[counter]['price'])
        counter += 1
    return counter


@st.cache_data(ttl=5)
def api(rooms, checkin, nights, results, low, high, amenities, tabnum):
    latitude = 25.75425773850914
    longitude = -80.37638818520564

    data = json.load(open("hotel1.json"))
    return data


def display(rooms, checkin, nights, results, low, high, amenities, tabnum):
    latitude = 25.75425773850914
    longitude = -80.37638818520564
    data = api(rooms, checkin, nights, results, low, high, amenities, tabnum)
    hotels = []
    hotels_coordinates = []
    if data['paging']['results'] == '0':
        return 0
    for i in range(results):
        hotels.append({
            'name': data['data'][i].get('name', 'Unavailable'),
            'latitude': float(data['data'][i].get('latitude', latitude)),
            'longitude': float(data['data'][i].get('longitude', longitude)),
            'website': data['data'][i].get('website', 'Unavailable'),
            'rating': data['data'][i].get('rating', 'No Rating'),
            'ranking': data['data'][i].get('ranking', 'Unavailable'),
            'price': data['data'][i].get('price', 'Unavailable'),
            'image': data['data'][i].get('photo', {}).get('images', {}).get('small', {}).get('url',
                                                                                             'https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg'),
            'image_width': int(
                data['data'][i].get('photo', {}).get('images', {}).get('small', {}).get('width', 480)),
            'image_height': int(
                data['data'][i].get('photo', {}).get('images', {}).get('small', {}).get('height', 360)),
            'visible': True
        })
        if tabnum == 2:
            hotels.append({'image': data['data'][i].get('photo', {}).get('images', {}).get('large', {}).get('url',
                                                                                                            'https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg'),
                           'image_width': int(
                               data['data'][i].get('photo', {}).get('images', {}).get('large', {}).get('width', 480)),
                           'image_height': int(
                               data['data'][i].get('photo', {}).get('images', {}).get('large', {}).get('height', 360))})

            st.header("Hotel for you")
    maps(hotels, tabnum, latitude, longitude, results)


def maps(hotels, tab_num, latitude, longitude, num_result):
    if tab_num == 1:
        st.header("Hotels")
    latitude = 25.75425773850914
    longitude = -80.37638818520564
    map_col1, map_col2 = st.columns(2)

    visible_hotels = []

    with map_col1:
        if tab_num == 1:
            show_all = st.button("Show All")
            hide_all = st.button("Hide All")
            if show_all:
                for i in range(len(hotels)):
                    hotels[i]['visible'] = True
                    if hotels[i]['visible']:
                        visible_hotels.append(hotels[i])
            elif hide_all:
                for i in range(len(hotels)):
                    hotels[i]['visible'] = False
                    if hotels[i]['visible']:
                        visible_hotels.append(hotels[i])
            for i in range(len(hotels)):
                if i == 6 or i == 15 or i == 24:
                    print("")
                else:
                    hotels[i]['visible'] = st.checkbox(hotels[i]['name'], value=hotels[i]['visible'],
                                                       key=i * 31 + 8)
                    if hotels[i]['visible']:
                        visible_hotels.append(hotels[i])
        else:
            visible_hotels.append(hotels[0])
            counter = 0
            hotel_details(counter, hotels, 1)

    with map_col2:
        if visible_hotels:
            df = pd.DataFrame(visible_hotels)
            st.map(df, zoom=13)
            df = df.drop(columns='latitude')
            df = df.drop(columns='longitude')
            df = df.drop(columns='visible')
        else:
            st.map([{'latitude': latitude,
                     'longitude': longitude}], zoom=10)

    st.write("##")
    st.write('##')

    if tab_num == 1:
        att_col1, att_col2, att_col3, att_col4, att_col5 = st.columns(5)
        counter = 0

        with att_col1:
            counter = hotel_details(counter, hotels, num_result // 5)
        with att_col2:
            counter = hotel_details(counter, hotels, num_result // 5)
        with att_col3:
            counter = hotel_details(counter, hotels,num_result // 5)
        with att_col4:
            counter = hotel_details(counter, hotels, num_result // 5)
        with att_col5:
            counter = hotel_details(counter, hotels, num_result // 5)


# Hotel

tab1, tab2 = st.tabs(["Hotels Near You", "Looking for Specific Hotel"])
with tab1:
    status1 = display(1, None, 1, 30, None, None, None, 1)
    if status1 == 0:
        st.write("No results found")
with tab2:
    min_price = st.number_input("Lowest Price", min_value=1, max_value=3000, value=1, format="%d")
    max_price = st.number_input("Highest Price", min_value=2, max_value=3000, value=3000, format="%d")
    rooms = st.number_input("Rooms", min_value=1, max_value=10, format="%d")
    amenities = st.multiselect("Amenities", ['beach', 'bar_lounge', 'airport_transportation'])
    check_in2 = st.date_input(
        "Check In",
        datetime.date(2023, 4, 28))
    nights = st.number_input("Nights", min_value=1, max_value=100, format="%d")
    ready = st.button("Find Hotels")
    refresh=0
    if ready or refresh:
        status2 = display(rooms, check_in2, nights, 1, min_price, max_price, amenities, 2)
        if status2 == 0:
            st.write("No results found")

            if refresh:
                status2 = display(rooms, check_in2, nights, 1, min_price, max_price, amenities, 2)
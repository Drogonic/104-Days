import streamlit as st
import pandas as pd
import json
import requests
import random
import main_functions

st.set_page_config(layout="wide")
# Logo image
st.image("104dayslogo.png", width=300)


def restaurant_details(counter, restaurant, loops):
    for i in range(loops):
        if counter == 6 or counter == 13 or counter == 20:
            print(" ")
        else:
            new_width = int(restaurant[counter]['image_width'] * 180 / restaurant[counter]['image_height'])
            st.image(restaurant[counter]['image'], width=new_width)
            st.caption("Rating: " + restaurant[counter]['rating'])
            with st.expander(restaurant[counter]['name']):
                st.caption("[Website](restaurant[counter]['website'])")
                st.caption("Description:" + restaurant[counter]['description'])
                st.caption("Price:" + restaurant[counter]['price'])
                st.caption("Ranking:" + restaurant[counter]['ranking'])
                st.caption(
                    restaurant[counter]['street1'] + "  \n" + restaurant[counter]['city'] + " " + restaurant[counter][
                        'state'] + ", " + restaurant[counter]['postalcode'])
        counter += 1
    return counter


@st.cache_data(ttl=5)
def api(num_results, ratings, units, tabnum):
    latitude = 25.75425773850914
    longitude = -80.37638818520564
    if tabnum:
        data = json.load(open("restaurant.json"))

    return data


def display(num_results, ratings, units, tabnum):
    latitude = 25.75425773850914
    longitude = -80.37638818520564
    data = api(num_results, ratings, units, tabnum)
    restaurant = []
    restaurant_coordinates = []

    if tabnum == 1:
        for i in range(num_results):
            restaurant.append({
                'name': data['data'][i].get('name', 'Unavailable'),
                'latitude': float(data['data'][i].get('latitude', latitude)),
                'longitude': float(data['data'][i].get('longitude', longitude)),
                'street1': data['data'][i].get('address_obj', {}).get('street1', 'Unavailable'),
                'description': data['data'][i].get('description', 'None Provided'),
                'city': data['data'][i].get('address_obj', {}).get('city', 'Unavailable'),
                'state': data['data'][i].get('address_obj', {}).get('state', 'Unavailable'),
                'country': data['data'][i].get('address_obj', {}).get('country', 'Unavailable'),
                'postalcode': data['data'][i].get('address_obj', {}).get('postalcode', 'None'),
                'ranking': data['data'][i].get('ranking', 'Unavailable'),
                'website': data['data'][i].get('website', 'Unavailable'),
                'rating': data['data'][i].get('rating', 'No Rating'),
                'price': data['data'][i].get('price_level', 'Unavailable'),
                'image': data['data'][i].get('photo', {}).get('images', {}).get('small', {}).get('url',
                                                                                                 'https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg'),
                'image_width': int(
                    data['data'][i].get('photo', {}).get('images', {}).get('small', {}).get('width', 480)),
                'image_height': int(
                    data['data'][i].get('photo', {}).get('images', {}).get('small', {}).get('height', 360)),
                'visible': True
            })

    if tabnum == 2:
        for i in range(num_results):
            rating = data['data'][i].get('rating', '0')
            rate_string = str(ratings)
            if rate_string <= rating:
                restaurant.append({

                    'name': data['data'][i].get('name', 'Unavailable'),
                    'latitude': float(data['data'][i].get('latitude', latitude)),
                    'longitude': float(data['data'][i].get('longitude', longitude)),
                    'street1': data['data'][i].get('address_obj', {}).get('street1', 'Unavailable'),
                    'description': data['data'][i].get('description', 'None Provided'),
                    'city': data['data'][i].get('address_obj', {}).get('city', 'Unavailable'),
                    'state': data['data'][i].get('address_obj', {}).get('state', 'Unavailable'),
                    'country': data['data'][i].get('address_obj', {}).get('country', 'Unavailable'),
                    'postalcode': data['data'][i].get('address_obj', {}).get('postalcode', 'None'),
                    'ranking': data['data'][i].get('ranking', 'Unavailable'),
                    'website': data['data'][i].get('website', 'Unavailable'),
                    'rating': data['data'][i].get('rating', 'No Rating'),
                    'price': data['data'][i].get('price_level', 'Unavailable'),
                    'image': data['data'][i].get('photo', {}).get('images', {}).get('small', {}).get('url',
                                                                                                     'https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg'),
                    'image_width': int(
                        data['data'][i].get('photo', {}).get('images', {}).get('small', {}).get('width', 480)),
                    'image_height': int(
                        data['data'][i].get('photo', {}).get('images', {}).get('small', {}).get('height', 360)),
                    'visible': True
                })

    maps(restaurant, tabnum, latitude, longitude, num_results)


def maps(restaurant, tab_num, latitude, longitude, num_result):
    if tab_num == 2:
        st.header("Restaurant")
    latitude = 25.75425773850914
    longitude = -80.37638818520564
    map_col1, map_col2 = st.columns(2)

    visible_restaurant = []
    with map_col1:
        if tab_num == 1:
            show_all = st.button("Show All")
            hide_all = st.button("Hide All")
            if show_all:
                for i in range(len(restaurant)):
                    restaurant[i]['visible'] = True
                    if restaurant[i]['visible']:
                        visible_restaurant.append(restaurant[i])
            elif hide_all:
                for i in range(len(restaurant)):
                    restaurant[i]['visible'] = False
                    if restaurant[i]['visible']:
                        visible_restaurant.append(restaurant[i])
            for i in range(len(restaurant)):
                if i == 6 or i == 13 or i == 20:
                    print("")
                else:
                    restaurant[i]['visible'] = st.checkbox(restaurant[i]['name'], value=restaurant[i]['visible'],
                                                           key=i * 31 + 8)
                    if restaurant[i]['visible']:
                        visible_restaurant.append(restaurant[i])
        else:
            counter = 0
            random_rest = random.randint(1, 3)
            if random_rest == 1:
                counter = random.randint(7, 9)
            elif random_rest == 2:
                counter = 2
            elif random_rest == 3:
                counter = random.randint(16, 17)
            restaurant_details(counter, restaurant, 1)

    with map_col2:
        if visible_restaurant:
            df = pd.DataFrame(visible_restaurant)
            st.map(df, zoom=13)
            df = df.drop(columns='latitude')
            df = df.drop(columns='longitude')
            df = df.drop(columns='visible')
        elif tab_num == 2:
            restaurant[random_rest]['visible'] = True
            visible_restaurant.append(restaurant[random_rest])
            if visible_restaurant:
                df = pd.DataFrame(visible_restaurant)
                st.map(df, zoom=13)
                df = df.drop(columns='latitude')
                df = df.drop(columns='longitude')
                df = df.drop(columns='visible')
        else:
            st.map([{'latitude': latitude,
                     'longitude': longitude}], zoom=0)

    st.write("##")
    st.write('##')

    if tab_num == 1:
        att_col1, att_col2, att_col3, att_col4, att_col5 = st.columns(5)
        counter = 0

        with att_col1:
            counter = restaurant_details(counter, restaurant, num_result // 5)
        with att_col2:
            counter = restaurant_details(counter, restaurant, num_result // 5)
        with att_col3:
            counter = restaurant_details(counter, restaurant, num_result // 5)
        with att_col4:
            counter = restaurant_details(counter, restaurant, num_result // 5)
        with att_col5:
            counter = restaurant_details(counter, restaurant, num_result // 5)


# restaurant

tab1, tab2 = st.tabs(["Restaurants Near You", "Looking for Specific Restaurants"])
with tab1:
    status1 = display(30, 1, "mi", 1)
    if status1 == 0:
        st.write("No results found")
with tab2:
    ratings = st.slider("Minimum Rating", min_value=3.0, max_value=4.5, step=.25, format="%f")
    units = st.radio("Distance Unit", ('mi', 'km'))
    ready = st.button("Find Restaurant")

    if ready:
        status2 = display(30, ratings, units, 2)
        if status2 == 0:
            st.write("No results found")

import streamlit as st
import pandas as pd
import json
import requests
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(layout="wide")
#Logo image
st.image("104dayslogo.png", width=300)

latitude = 25.75425773850914
longitude = -80.37638818520564


data = json.load(open("attractions.json"))

# st.write(data

attractions = []
attraction_coordinates = []

for i in range(10):
    attractions.append({
        'name': data['data'][i].get('name', 'Unavailable'),
        'latitude': float(data['data'][i].get('latitude', latitude)),
        'longitude': float(data['data'][i].get('longitude', longitude)),
        'description': data['data'][i].get('description', 'Unavailable'),
        'website': data['data'][i].get('website', 'Unavailable'),
        'rating': data['data'][i].get('rating', 'No Rating'),
        'street1': data['data'][i].get('address_obj', {}).get('street1', 'Unavailable'),
        'city': data['data'][i].get('address_obj', {}).get('city', 'Unavailable'),
        'state': data['data'][i].get('address_obj', {}).get('state', 'Unavailable'),
        'country': data['data'][i].get('address_obj', {}).get('country', 'Unavailable'),
        'postalcode': data['data'][i].get('address_obj', {}).get('postalcode', 'None'),
        'image': data['data'][i].get('photo', {}).get('images', {}).get('medium', {}).get('url','https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg'),
        'image_width': int(data['data'][i].get('photo', {}).get('images', {}).get('medium', {}).get('width', 480)),
        'image_height': int(data['data'][i].get('photo', {}).get('images', {}).get('medium', {}).get('height', 360)),
        'visible': True
    })


def attraction_details(counter):
    for i in range(2):

        new_width = int(attractions[counter]['image_width'] * 155 / attractions[counter]['image_height'])
        st.image(attractions[counter]['image'], width= new_width)
        st.caption("Rating: " + attractions[counter]['rating'])
        with st.expander(attractions[counter]['name']):
            st.write(attractions[counter]['description'])
            st.caption("[Website](attractions[counter]['website'])")
            st.caption(attractions[counter]['street1'] + "  \n" + attractions[counter]['city'] + " " + attractions[counter]['state'] + ", " + attractions[counter]['postalcode'])
            counter += 1

    return counter


def toggle_all_visibility(visible):
    for attraction in attractions:
        attraction['visible'] = visible

st.header("Attractions near you")
map_col1, map_col2 = st.columns(2)

visible_attractions = []
attraction_visibility = {attraction['name']: True for attraction in attractions}

with map_col1:
    show_all = st.button("Show All")
    hide_all = st.button("Hide All")

    if show_all:
        attraction_visibility = {attraction['name']: True for attraction in attractions}
    elif hide_all:
        attraction_visibility = {attraction['name']: False for attraction in attractions}


    for i in range(10):
        visible = attractions[i]['visible'] = st.checkbox(attractions[i]['name'],value=attraction_visibility[attractions[i]['name']])
        attraction_visibility[attractions[i]['name']] = visible
        if visible:
            visible_attractions.append(attractions[i])

with map_col2:
  if visible_attractions:
    df = pd.DataFrame(visible_attractions)
    st.map(df, zoom=13)
    df = df.drop(columns='latitude')
    df = df.drop(columns='longitude')
    df = df.drop(columns='visible')
  else:
    st.map([{'latitude': latitude,
            'longitude': longitude}], zoom=13)

st.write("##")
st.write('##')

att_col1, att_col2, att_col3, att_col4, att_col5 = st.columns(5)
counter = 0

with att_col1:
    counter = attraction_details(counter)
with att_col2:
    counter = attraction_details(counter)
with att_col3:
    counter = attraction_details(counter)
with att_col4:
    counter = attraction_details(counter)
with att_col5:
    counter = attraction_details(counter)

#plots

st.write("About our attractions:")
url = "https://travel-advisor.p.rapidapi.com/attractions/list"
headers = {
    "X-RapidAPI-Key": "b2f06dab7cmshc3882d170776bd7p1bda36jsn54a3c3ba4504",
    "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
}

data = json.load(open("attractions.json"))
#print(data)
data2 = json.load(open("hotels.json"))


df = pd.DataFrame(data["data"])
df1 = df[["name", "location_string", "num_reviews", "description"]]
df['num_reviews'] = pd.to_numeric(df['num_reviews'])
st.subheader("Bar plot")

#st.write(df)
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("name"),
    y=alt.Y("num_reviews", sort="ascending")
).interactive()

st.altair_chart(chart, use_container_width=True)

st.subheader("Line plot")
fig, ax = plt.subplots()
ax.plot(df["name"], df["rating"], marker="o")
ax.set_xlabel("Attraction")
ax.set_ylabel("Rating")
ax.set_title("Attraction rating")
ax.set_xticklabels(df["name"], rotation=90)
ax.invert_yaxis()
st.pyplot(fig)

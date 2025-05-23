import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import json
import altair as alt

st.set_page_config(layout="wide")

st.image("104dayslogo.png", width=300)

st.image("homepagePic.jpg")
st.header("About Us")

st.subheader("Our Goal")

st.write(""" Provide information to Florida International University students of 
            fun activities and places to stay during the summer near FIU main campus in Miami, Florida. 
             """)

st.info("""
             This is a website created using Streamlit, a powerful library for building data-driven web applications in Python.
             Our team consists of four students: Valeria, Jerrick, Cate, and Giovanny .
             This is the final product of our team applying web development best practices in Spring 2023.
             If you're interested in learning more about this project, please don't hesitate to contact us.
             Thank you for visiting our website!
             """)






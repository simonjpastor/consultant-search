import pandas as pd
from bs4 import BeautifulSoup
import requests
import streamlit as st

APP_NAME = "Consulting Job Search"

st.title(APP_NAME)

search = st.text_input("Enter your search term", "Junior Analyst")

submit_button = st.button('Submit', key="search_submit")


jobs = []
links = []

def find_job_booz(search):
    search = f'https://careers.boozallen.com/jobs/search/{search}'
    response = requests.get(search, headers={'User-Agent': 'Chrome/86.0.4240.111'})
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all(class_="cell-title")
    st.write()
    st.markdown("**Booz Allen**")
    for i in jobs:
        job = i.find("a").text
        link = i.find("a")["href"]
        st.markdown(f"[{job}]({link})")
    st.write()

def find_job_bcg(search):
    search = f'https://careers.bcg.com/search-results?m=3&keywords={search}'
    response = requests.get(search, headers={'User-Agent': 'Chrome/86.0.4240.111'})
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.select("div")
    print("BCG")
    #for i in jobs:
        #print(i.find(class_="job-title").text)


if submit_button:
    search = search.replace(" ","%20")
    find_job_booz(search)
    find_job_bcg(search)

import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import chromedriver_binary

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

    jobs_and_locations = soup.find_all("td")
    positions = soup.find_all(class_="cell-title")
    jobs = []
    links = []
    locations = []
    excluding_list = []

    st.markdown("**Booz Allen**")

    for i in positions:
        excluding_list.append(i)
        jobs.append(i.find('a').text)
        links.append(i.find('a')["href"])
    for j in jobs_and_locations:
        if j not in excluding_list:
            locations.append(j.text)
    for f in range (0,len(locations)):
        st.markdown(f"[{jobs[f]}]({links[f]}) - {locations[f]}")

    #jobs = soup.find_all("td")
    #st.write(soup)
    #count = 2
    #for i in jobs:
        #if count % 2 ==0:
            #job = i.find("a").text
            #link = i.find("a")["href"]
            #count += 1
        #elif count %2 != 0:
            #location = i.text
            #st.markdown(f"[{job}]({link}) - {location}")
    #st.write()

def find_job_bcg(search):
    driver = webdriver.Chrome()
    driver.get(f"https://careers.bcg.com/search-results?m=3&keywords={search}")
    driver.implicitly_wait(10)
    driver.find_elements_by_xpath("/html/body/div[1]/section/div/div/header/div/section/div/div/div/div[2]/button")[0].click()
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    jobs = soup.select("div .information")
    job_link = {}
    st.markdown("**BCG**")
    for i in jobs:
        st.markdown(f"[{i.find("a")["data-ph-at-job-title-text"]}]({i.find("a")["href"]})")


if submit_button:
    search = search.replace(" ","%20")
    find_job_booz(search)
    find_job_bcg(search)

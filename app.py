import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import chromedriver_binary
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

APP_NAME = "Consulting Job Search"

st.title(APP_NAME)

search = st.text_input("Enter your search term", "Junior Analyst")

submit_button = st.button('Submit', key="search_submit")


jobs = []
links = []

def find_job_mckinsey(search):
    options = Options()
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"')
    #driver.delete_all_cookies()
    #driver.get("chrome://settings/clearBrowserData")
    driver.get(f'https://www.mckinsey.com/careers/search-jobs#?query={search}')
    driver.implicitly_wait(9)
    driver.find_elements_by_xpath("/html")[0].click()
    #driver.find_elements_by_css_selector("body > div.cookie-warning-wrapper.-show > div.box > div > div > div.cookie-compliance.row > a.btn.btn-fill.cookie-btn.accept-btn.at-element-click-tracking")[0].click()
    #st.write(driver.find_elements_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]"))
    #driver.find_elements_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/a[1]")[0].click()
    html = driver.page_source
    #st.write(html)
    soup = BeautifulSoup(html, "html.parser")
    jobs = soup.select(".job-listing-link")

    st.markdown("**McKinsey & Company**")
    for i in jobs:
        st.markdown(f'[{i["data-layer-text"]}](https://www.mckinsey.com/careers{i["href"][1:]}) - {i.find(class_="city ng-binding ng-scope").text}')

    return driver

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
        st.markdown(f'[{jobs[f]}]({links[f]}) - {locations[f]}')

def find_job_bcg(search, driver):
    driver.get(f"https://careers.bcg.com/search-results?m=3&keywords={search}")
    driver.implicitly_wait(10)
    driver.find_elements_by_xpath("/html/body/div[1]/section/div/div/header/div/section/div/div/div/div[2]/button")[0].click()
    html = driver.page_source
    #driver.quit()
    soup = BeautifulSoup(html, "html.parser")

    jobs = soup.select("div .information")
    job_link = {}
    st.markdown("**BCG**")
    for i in jobs:
        st.markdown(f'[{i.find("a")["data-ph-at-job-title-text"]}]({i.find("a")["href"]})')

    return driver

def find_job_mercer(search, driver):
    driver.get(f"https://careers.mmc.com/global/en/search-results?keywords={search}")
    driver.implicitly_wait(9)
    #driver.find_elements_by_xpath("/html/body/div[1]/section/div/div/header/div/section/div/div/div/div[2]/button/ppc-content")[0].click()
    driver.find_elements_by_xpath("/html")[0].click()
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    st.markdown("**Mercer**")
    for i in soup.find_all(class_="information"):
        if i.find("span").find("a"):
                x = i.find("span").find("a")
                st.markdown(f'[{x["data-ph-at-job-title-text"]}]({x["href"]}) - {x["data-ph-at-job-location-area-text"]}')
        else:
            continue
    return driver

if submit_button:
    search = search.replace(" ","%20")
    driver = find_job_mckinsey(search)
    st.write()
    driver = find_job_bcg(search, driver)
    st.write()
    find_job_booz(search)
    st.write()
    driver = find_job_mercer(search,driver)
    driver.quit()


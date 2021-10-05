from tweepy import OAuthHandler
from tweepy import API, error
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import time
import json
from datetime import datetime
import pandas as pd
import random
import config
import streamlit as st
#from config.py import CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN_KEY, ACCESS_TOKEN_SCRET

APP_NAME = "TwittLists"

st.title(APP_NAME)

search = st.text_input("Enter the accounts", "@GretaThunberg, @UNEP")

submit_button = st.button('Submit', key="search_submit")


consumer_key=config.CONSUMER_KEY
consumer_secret=config.CONSUMER_SECRET
access_token_key=config.ACCESS_TOKEN_KEY
access_token_secret=config.ACCESS_TOKEN_SCRET
access_token_secret=config.ACCESS_TOKEN_SCRET
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

civic_lists = []
civic_lists_history = []
civic_name = []
civic_dates = []
civic_followers = []
civic_members = []
all_members = []

new_civic_lists = []
dict_with_people_list = []

cool_people = {}
cool_followers = {}


def initial_function(dict_with_people):
    #Use this function at the very beginning and after each successful final_members() function
    for peoples in dict_with_people.keys():
        dict_with_people_list.append(peoples)
    return dict_with_people_list

def members_to_lists(dict_with_people,looking_for):
    for people in dict_with_people_list:
        try :
            for i in api.lists_memberships(people, count=10):
                if i.id not in civic_lists and i.id not in civic_lists_history:
                    for j in looking_for:
                        if j in i.name.lower():
                            civic_lists.append(i.id)
                            civic_lists_history.append(i.id)
                            civic_name.append(i.name)
                            civic_dates.append(i.created_at)
                            civic_followers.append(i.subscriber_count)
                            civic_members.append(i.member_count)
                            if len(dict_with_people_list) % 10 == 0:
                                print(len(dict_with_people_list))
        except error.TweepError:
            pass
        dict_with_people_list.remove(people)
    return civic_lists


def list_to_members(dict_with_people,looking_for):
    for i in members_to_lists(dict_with_people,looking_for):
        try :
            all_members.append(api.list_members(list_id=i))
        except error.TweepError:
            pass
        civic_lists.remove(i)
    return all_members

def final_members(dict_with_people,looking_for):
    for members in list_to_members(dict_with_people,looking_for):
        for i in members:
            if i.screen_name in cool_people.keys():
                cool_people[i.screen_name] += 1
            else:
                cool_people[i.screen_name] = 0
    return cool_people

def top5(dict_with_people,looking_for):
    ranking = []
    number = []
    for i,j in final_members(dict_with_people,looking_for).items():
        if len(ranking) < 300:
            ranking.append(i)
            number.append(j)
        else:
            if j > min(number):
                ranking.pop(number.index(min(number)))
                number.pop(number.index(min(number)))
                ranking.append(i)
                number.append(j)
            else:
                continue

    x = list(zip(ranking,number))
    return x

def run(iterations):
    initial_function(cool_people)
    top5(cool_people,looking_for_list)
    print("_____")
    while iterations > 1:
        print(f"{iterations} iteration successful")
        iterations = iterations - 1
        initial_function(cool_people)
        top5(cool_people,looking_for_list)
    final_results = end(cool_people)
    return final_results

def end(results):
    results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    values = []
    accounts = []
    for i in results:
        accounts.append(i[0])
        values.append(i[1])
    final_results = pd.DataFrame.from_dict({"Accounts":accounts,"Counts":values})
    return final_results


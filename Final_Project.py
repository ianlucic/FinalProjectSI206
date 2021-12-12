# FALL 2021
# SI 206
# Final Project
# Your name: Sarayu Dandamudi
# Your student id: 27141407
# Your email: sarayud@umich.edu
# List who you have worked with on this project: Ian Lucic, Sarayu Dandamudi 

from bs4 import BeautifulSoup
import sqlite3
import unittest
import requests
import json
import os
import pandas as pd
import io
from urllib.request import urlopen
import plotly.graph_objects as go
import plotly.express as px
  
def readDatafromAPI():
    url = "https://api.covidactnow.org/v2/states.json?apiKey=e1ad87ee3e3c4558a7e573a795f6ee60"
    response = urlopen(url)
    data_json = json.loads(response.read())
    #print(data_json)
    return data_json


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpCovidTable(json_data, cur, conn):
    #if the count is 1, then table exists
    if len(cur.fetchall()) != 0 : 
        print('Table exists.')
    else :
        print('Table does not exist.')
        cur.execute('DROP TABLE IF EXISTS covid_rate_data')
        cur.execute('CREATE TABLE covid_rate_data (state TEXT, total_cases INTEGER, total_deaths INTEGER, total_hospitalizations INTEGER, icu_beds INTEGER, total_positive_tests INTEGER, total_negative_tests INTEGER)')

    conn.commit()
    #print(json_data[0])

def storeData(json_data, cur, conn):
    for dict in json_data:
        state = dict['state']
        #print(state) 
        total_cases = dict['actuals']['cases']
        #print(total_cases)
        total_deaths = dict['actuals']['deaths']
        #print(total_deaths)
        total_hospitalizations = dict['actuals']['hospitalBeds']['currentUsageCovid']
        #print(total_hospitalizations)
        icu_beds = dict['actuals']['icuBeds']['currentUsageCovid']
        #print(icu_beds)
        total_positive_tests = dict['actuals']['positiveTests']
        total_negative_tests = dict['actuals']['negativeTests']
        cur.execute('INSERT INTO covid_rate_data (state, total_cases, total_deaths, total_hospitalizations, icu_beds, total_positive_tests, total_negative_tests) Values(?,?,?,?,?,?,?)', (state, total_cases, total_deaths, total_hospitalizations, icu_beds, total_positive_tests, total_negative_tests))
        cur_nrows = len(cur.fetchall())
    
    
    conn.commit()

def plotdata(json_data):
    state_list = []
    covid_list = []
    for dict in json_data:
        states = dict['state']
        state_list.append(states)
        total_cases = dict['actuals']['cases']
        covid_list.append(total_cases)
    print(state_list)
    print(covid_list)
    #MI_exams = [299, 389, 410, 577, 593, 936, 962, 1025, 1192, 1165]
    #GA_exams = [692, 884, 1037, 1261, 1536, 1658, 2033, 1914, 2095, 2257]

    fig = px.choropleth(locations= state_list, locationmode="USA-states", color= covid_list, scope="usa")
    fig.show()

def main():
    json_data = readDatafromAPI()
    cur, conn = setUpDatabase('COVIDdata.db')
    setUpCovidTable(json_data, cur, conn)
    storeData(json_data, cur, conn)


    conn.close()

    plotdata(json_data)


        
        
if __name__ == '__main__':
    main()
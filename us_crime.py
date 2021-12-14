# FALL 2021
# SI 206
# Final Project
# Your name: Claire Zuo
# Your student id: 72712801
# Your email: zclaire@umich.edu
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

def readDataFromAPI():
    base_url = 'https://api.usa.gov/crime/fbi/sapi/api/data/supplemental/burglary/states/{}/OFFENSE/2019/2020?API_KEY=iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv'
    infodata = []
    stateslist = ['AL','AK','AS','AZ','AR','CA','CO','CT','DE','DC','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX','UT','VT','VA','VI','WA','WV','WI','WY']
    for state in stateslist:
        url = base_url.format(state)
        r = requests.get(url)
        results = r.json()["results"]
        for result in results:
            result["state"] = state
            infodata.append(result)
    return infodata

def setUpDatabase(db_name):
    path = '/Users/clairezuo/Desktop/'
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpCrimeTable(cur, conn):
        #get the count of tables with the name
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='crime_rate_data';")

    #if the count is 1, then table exists
    if len(cur.fetchall()) != 0 : 
        print('Table exists.')
        return
    else :
        print('Table does not exist.')
        cur.execute('DROP TABLE IF EXISTS crime_rate_data')
        cur.execute('CREATE TABLE crime_rate_data (state TEXT, offense TEXT, year INTEGER, stolen INTEGER)') #can remove offense
    conn.commit()

def storeData(infodata, cur, conn):
    cur.execute("SELECT * FROM crime_rate_data")
    num_rows = len(cur.fetchall())
    if num_rows == 102:
        return 
    else:
        for i in range(num_rows, num_rows+17):
            year = infodata[i]['data_year']
            stolen = infodata[i]['actual_count']
            state = infodata[i]['state']
            cur.execute("INSERT INTO crime_rate_data(state, offense, year, stolen)VALUES(?,?,?,?)",(state, year, stolen))
    conn.commit()



def connectdata(cur,conn):
    cur.execute("SELECT total_cases FROM covid_rate_data JOIN crime_rate_data ON covid_rate_data.state = crime_rate_data.state;") 

# def delete_table(cur, conn):
#     cur.execute('DROP TABLE IF EXISTS crime_rate_data')
#     conn.commit()



def main():
    infodata = readDataFromAPI()
    cur, conn = setUpDatabase('Database-Claire.db')
    setUpCrimeTable(cur, conn)
    storeData(infodata, cur, conn)
    plotdata1(infodata)
    averagecrimeperyear(infodata)

    # delete_table(cur, conn)
    conn.close()

    # plotdata(infodata)


if __name__ == "__main__":
    main()   

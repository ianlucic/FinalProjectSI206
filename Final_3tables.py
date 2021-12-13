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

def readDataFromAPI_crime():
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

def readDatafromAPI_covidUS():
    url = "https://api.covidactnow.org/v2/states.json?apiKey=e1ad87ee3e3c4558a7e573a795f6ee60"
    response = urlopen(url)
    data_json = json.loads(response.read())
    #print(data_json)
    return data_json

# this method is pretty simple - it just creates the server connection
def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        pass
    cur = conn.cursor()
    return conn, cur

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn



def setUpCrimeTable(cur, conn):
        #get the count of tables with the name
    cur.execute('SELECT count(*) FROM crime_rate_data')

    #if the count is 1, then table exists
    if len(cur.fetchall()) != 0 : 
        print('Table exists.')
        return
    else :
        print('Table does not exist.')
        cur.execute('DROP TABLE IF EXISTS crime_rate_data')
        cur.execute('CREATE TABLE crime_rate_data (state TEXT, offense TEXT, year INTEGER, stolen INTEGER)') #can remove offense
    conn.commit()

def setUpCovidTable(cur, conn):
    cur.execute('SELECT count(*) FROM covid_rate_data')
    #if the count is 1, then table exists
    if len(cur.fetchall()) != 0 : 
        print('Table exists.')
    else :
        print('Table does not exist.')
        cur.execute('DROP TABLE IF EXISTS covid_rate_data')
        cur.execute('CREATE TABLE covid_rate_data (state TEXT, total_cases INTEGER, total_deaths INTEGER, total_hospitalizations INTEGER, icu_beds INTEGER, total_positive_tests INTEGER, total_negative_tests INTEGER)')

    conn.commit()
    #print(json_data[0])


def setUpCanadaTable(cur, conn):
        #get the count of tables with the name
    try:
        cur.execute('SELECT count(*) FROM covid_canada_3')
    except:
        pass

    #if the count is 1, then table exists
    if len(cur.fetchall()) != 0 : 
        print('Table exists.')
        return
    else :
        print('Table does not exist.')
        cur.execute('DROP TABLE IF EXISTS covid_canada_3')
        cur.execute('CREATE TABLE covid_canada_3 (province TEXT, date TEXT, change_cases INTEGER, change_fatalities INTEGER, change_tests INTEGER,  change_criticals INTEGER, change_hospitalizations INTEGER, change_vaccinations INTEGER, change_recoveries INTEGER, change_vaccinated INTEGER, change_boosters_1 INTEGER, change_vaccines_distributed INTEGER, total_cases INTEGER, total_fatalities INTEGER,  total_tests INTEGER, total_hospitalizations INTEGER, total_criticals INTEGER, total_recoveries INTEGER, total_vaccinations INTEGER, total_vaccinated INTEGER, total_boosters_1 INTEGER, total_vaccines_distributed INTEGER)') 
    conn.commit()

def storeData_crime(infodata, cur, conn):
    cur.execute("SELECT * FROM crime_rate_data")
    num_rows = len(cur.fetchall())
    if num_rows == 102:
        return 
    else:
        for i in range(num_rows, num_rows+17):
            year = infodata[i]['data_year']
            stolen = infodata[i]['actual_count']
            state = infodata[i]['state']
            cur.execute("INSERT INTO crime_rate_data(state, offense, year, stolen)VALUES(?,?,?,?)",(state, "burglary", year, stolen))
    conn.commit()

def storeData_covidUS(json_data, cur, conn):
    cur.execute('SELECT * FROM covid_rate_data')
    num_rows = len(cur.fetchall())
    print(num_rows)
    if num_rows == 53:
        return 
    else:
        for i in range(num_rows, num_rows+1):
            sql = "INSERT INTO covid_rate_data VALUES (?,?,?,?,?,?,?)"
            state = json_data[i]['state']
            total_cases = json_data[i]['actuals']['cases']
            total_deaths = json_data[i]['actuals']['deaths']
            total_hospitalizations = json_data[i]['actuals']['hospitalBeds']['currentUsageCovid']
            icu_beds = json_data[i]['actuals']['icuBeds']['currentUsageCovid']
            total_positive_tests = json_data[i]['actuals']['positiveTests']
            total_negative_tests = json_data[i]['actuals']['negativeTests']
            cur.execute(sql ,(state, total_cases, total_deaths, total_hospitalizations, icu_beds, total_positive_tests, total_negative_tests))

    
            #for dict in json_data:
                #state = dict['state']
                #print(state) 
                #total_cases = dict['actuals']['cases']
                #print(total_cases)
                #total_deaths = dict['actuals']['deaths']
                #print(total_deaths)
                #total_hospitalizations = dict['actuals']['hospitalBeds']['currentUsageCovid']
                #print(total_hospitalizations)
                #icu_beds = dict['actuals']['icuBeds']['currentUsageCovid']
                #print(icu_beds)
                #total_positive_tests = dict['actuals']['positiveTests']
                #total_negative_tests = dict['actuals']['negativeTests']
            #list_vals = [state, total_cases, total_deaths, total_hospitalizations, icu_beds, total_positive_tests, total_negative_tests]
            #print(list_vals)
                #cur.execute(sql, (state, total_cases, total_deaths, total_hospitalizations, icu_beds, total_positive_tests, total_negative_tests))
            #cur.execute('INSERT INTO covid_rate_data (state, total_cases, total_deaths, total_hospitalizations, icu_beds, total_positive_tests, total_negative_tests) Values(?,?,?,?,?,?,?)', (state, total_cases, total_deaths, total_hospitalizations, icu_beds, total_positive_tests, total_negative_tests))
    
    conn.commit()

def storeData_covidCA(project, cur, conn):
    cur.execute("SELECT * FROM covid_canada_3")
    num_rows = len(cur.fetchall())
    print(num_rows)
    if num_rows == 13:
        return 
    else:
        for i in range(num_rows, num_rows+1):
            sql = "INSERT INTO covid_canada_3 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)" # this line is the SQL commands, the ? represent each column
    
            cur = conn.cursor()
            print(project[i])
            # this basically puts the row into list form so that it is easier to insert
            list_vals = [project[i]["province"], project[i]["date"],  project[i]["change_cases"], project[i]["change_fatalities"], 
            project[i]["change_tests"],  project[i]["change_criticals"], project[i]["change_hospitalizations"], 
            project[i]["change_vaccinations"], project[i]["change_recoveries"], project[i]["change_vaccinated"], 
            project[i]["change_boosters_1"], project[i]["change_vaccines_distributed"], project[i]["total_cases"], project[i]["total_fatalities"],
            project[i]["total_tests"], project[i]["total_hospitalizations"], project[i]["total_criticals"], project[i]["total_recoveries"],
            project[i]["total_vaccinations"], project[i]["total_vaccinated"], project[i]["total_boosters_1"], project[i]["total_vaccines_distributed"]]
            print(list_vals)
            cur.execute(sql, list_vals)

            conn.commit()







def main():
    #crime data
    infodata = readDataFromAPI_crime()
    cur, conn = setUpDatabase('Final_data.db')
    setUpCrimeTable(cur, conn)
    storeData_crime(infodata, cur, conn)


    #USAcovid
    json_data = readDatafromAPI_covidUS()
    cur, conn = setUpDatabase('Final_data.db')
    setUpCovidTable(cur, conn)
    storeData_covidUS(json_data, cur, conn)


    #Canadacovid
    database = r"/Users/ianlucic/Documents/Michigan W21/SI 206 - Python/Final/Final_data.db"  #path to your database

    conn, cur = create_connection(database)
    
    with conn:
    
        data = requests.get('https://api.covid19tracker.ca/summary/split')
        data_dict = data.json()["data"]
        #goes thru api data row by row and inserts
        
        setUpCanadaTable(cur, conn)
        storeData_covidCA(data_dict, cur, conn)

    conn.close()



    



if __name__ == "__main__":
    main() 

  



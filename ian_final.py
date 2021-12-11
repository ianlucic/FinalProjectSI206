import requests
import unittest
import sqlite3
import json
import os
import pandas as pd
import io



def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        pass

    return conn


def insert_row(conn, project):


    sql = "INSERT INTO covid_canada VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)" 
    
    cur = conn.cursor()
    

    list_vals = [project["province"], project["date"],  project["change_cases"], project["change_fatalities"], 
    project["change_tests"],  project["change_criticals"], project["change_hospitalizations"], 
    project["change_vaccinations"], project["change_recoveries"], project["change_vaccinated"], 
    project["change_boosters_1"], project["change_vaccines_distributed"], project["total_cases"], project["total_fatalities"],
    project["total_tests"], project["total_hospitalizations"], project["total_criticals"], project["total_recoveries"],
    project["total_vaccinations"], project["total_vaccinated"], project["total_boosters_1"], project["total_vaccines_distributed"]]

    cur.execute(sql, list_vals)
    conn.commit()

#WORK IN PROGRESS
def setCanadaTable(cur, conn, data_json, limit=22):
    cur.execute("CREATE TABLE IF NOT EXISTS CanadaLimit (province TEXT, date TEXT, change cases INTEGAR, change fatalities INTEGAR, change tests INTEGAR, change hopsitalizations INTEGAR, chnage criticals INTEAGR, change recoveries INTEGAR, change vaccinations INTEGAR, change vaccinated INTEGAR, change booster 1 INTEGAR, change vaccine distributed INTEGAR, total cases INTEGAR, total fatalities INTEGAR, total tests INTEGAR, total hospitalizations INTEGAR, total cirticals INTEGAR, total recoveries INTEGAR, total vaccinations INTEGAR, total vaccinated INTEGAR, total booster 1 INTEGAR, total vaccines distrubed INTEGAR)")
    cur.execute("SELECT * FROM CanadaLimit")
    nrows = len(cur.fetchall())
    for i in json_data:
        province = i['province']
        date = i['date']
        change_cases = i['change cases']
        change_fatalities = i['change fatalities']
        change_tests = i['change tests']
        change_hospitalizations = i['change hospitalizations']
        change_criticals = i['change citicials']
        change_recoveries = i['change recoveries']
        change_vaccinations = i['change vaccinations']
        change_vaccinated = i['changed vaccinated']
        change_boosters_1 = i['change boosters 1']
        change_vaccines_distributed = i['change vaccines distributed']
        total_cases = i['total cases']
        total_fatalities = i['total fatalities']
        total_tests = i['total tests']
        total_hospitalizations = i['total hospitalizations']
        total_criticals = i['total criticals']
        total_recoveries = i['total recoveries']
        total_vaccinations = i['total vaccinations']
        total_vaccinated = i['total vaccinated']
        total_boosters_1 = i['total booster 1']
        total_vaccines_distributed = i['total vaccines distributed']
        cur.execute("INSERT INTO OR IGNORE CanadaLimit (province, date, change cases, change fatalities, change tests, change hopsitalizations, chnage criticals, change recoveries, change vaccinations, change vaccinated, change booster 1, change vaccine distributed, total cases, total fatalities, total tests, total hospitalizations, total cirticals, total recoveries, total vaccinations, total vaccinated, total booster 1, total vaccines distrubed) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
        cur.execute("SELECT * FROM CanadaLimit")
        cur_nrows = len(cur.fetchall())
        if(cur_nrows == nrows+limit):
            break
    cur.execute("SELECT * FROM populations")
    nrows = len(cur.fetcall())
    conn.commit()
    print(str(nrows)+"/286 entries in the Tables")


def main():
    #path to your database
    database = r"/Users/ianlucic/Documents/Michigan W21/SI 206 - Python/Final/CanadaCOVIDData.db"

    conn = create_connection(database)
    with conn:
    
        data = requests.get('https://api.covid19tracker.ca/summary/split')
        data_dict = data.json()["data"]

        #goes thru api data row by row and inserts
        for row in data_dict:
            insert_row(conn, row)

        
        
if __name__ == '__main__':
    main()
    
    
    
    
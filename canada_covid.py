import requests
import unittest
import sqlite3
import json
import os
import pandas as pd
import io


# this method is pretty simple - it just creates the server connection
def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        pass
    cur = conn.cursor()
    return conn, cur

#this is the method we will use to insert each row into the database

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

def storeData(project, cur, conn):
    cur.execute("SELECT * FROM covid_canada_3")
    num_rows = len(cur.fetchall())
    print(num_rows)
    if num_rows == 13:
        return 
    else:
        for i in range(num_rows, num_rows+13):
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
    #path to your database
    database = r"/Users/ianlucic/Desktop/FinalProjectSI206/DATAFINAL.db"

    conn, cur = create_connection(database)
    with conn:
    
        data = requests.get('https://api.covid19tracker.ca/summary/split')
        data_dict = data.json()["data"]
        #goes thru api data row by row and inserts
        
        setUpCanadaTable(cur, conn)
        storeData(data_dict, cur, conn)

if __name__ == '__main__':
    main()
    
    
    
    
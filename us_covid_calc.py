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

def plotdata(json_data):
    state_list = []
    covid_list = []
    for d in json_data:
        states = d['state']
        state_list.append(states)
        total_cases = d['actuals']['cases']
        covid_list.append(total_cases)
    #print(state_list)
    #print(covid_list)
    
    
    fig = px.choropleth(locations= state_list, locationmode="USA-states", color= covid_list, scope="usa")
    fig.update_layout(title='US Covid Cases For Each State',
                    font=dict(
                        family = "Futura",
                        size=20))
    fig.show()

def plot_line(json_data):
    state_list = []
    covid_list = []
    for d in json_data:
        states = d['state']
        state_list.append(states)
        total_cases = d['actuals']['cases']
        covid_list.append(total_cases)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=state_list, y = covid_list, name='2020',
                         line=dict(color='blue', width=3)))
 
    fig.update_layout(title='US Covid Cases For Each State',
                    xaxis_title='States',
                    yaxis_title='Covid Cases',
                    font=dict(
                        family = "Futura",
                        size=20,
                        color='black'
                    ))
    fig.show()

def plot_together():

    label_list = ['US cases','Canada cases']
    value_list = [49799780, 1838277]

    fig = go.Figure(data=[go.Pie(labels=label_list, values=value_list)])
    color_list = ['#FF0000', '#000080']
    fig.update_traces(hoverinfo='label+percent', textfont_size=20,
                  marker=dict(colors=color_list))

    fig.update_layout(title='US Covid Cases For Each State',
                    xaxis_title='States',
                    yaxis_title='Covid Cases',
                    font=dict(
                        family = "Futura",
                        size=20,
                        color='black'
                    ))
                    
    fig.show()

def USA_covid_total(json_data):
    total_cases = []
    for dict in json_data:
        cases = dict['actuals']['cases']
        total_cases.append(cases)
    total = 0
    for i in total_cases:
        total += i
    print("The total number of COVID cases in USA: " + str(total))
    return total

def USA_deaths_total(json_data):
    total_deaths = []
    for dict in json_data:
        deaths = dict['actuals']['deaths']
        total_deaths.append(deaths)
    total = 0
    for i in total_deaths:
        total+= i
    print("The total number of deaths in USA: " + str(total))
    return total

def USA_perecentage(json_data):
    total_cases_list = []
    total_deaths_list = []
    for dict in json_data:
        cases = dict['actuals']['cases']
        total_cases_list.append(cases)
    total_cases = 0
    for i in total_cases_list:
        total_cases += i
    total_US_population = 333807743

    for dict in json_data:
        deaths = dict['actuals']['deaths']
        total_deaths_list.append(deaths)
    total_deaths = 0
    for i in total_deaths_list:
        total_deaths += i
    
    percentage_cases = (total_cases / total_US_population) * 100
    percentage_deaths = (total_deaths / total_US_population) * 100
    print("The percentage of COVID cases in USA: " + str(round(percentage_cases, 2)))
    print("The percentage of COVID deaths in USA: " + str(round(percentage_deaths, 2)))

def USA_average_cases(json_data):
    total_cases = []
    for dict in json_data:
        cases = dict['actuals']['cases']
        total_cases.append(cases)
    total = 0
    for i in total_cases:
        total += i
    average = total // len(total_cases)
    print("The average number of COVID cases in USA: " + str(average))
    return average
        
    


def main():
    json_data = readDatafromAPI()
    plot_together()
    plot_line(json_data)
    plotdata(json_data)
    USA_covid_total(json_data)
    USA_deaths_total(json_data)
    USA_perecentage(json_data)
    USA_average_cases(json_data)

if __name__ == '__main__':
    main()
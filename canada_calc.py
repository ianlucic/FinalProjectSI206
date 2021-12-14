import requests
import unittest
import sqlite3
import json
import os
import pandas as pd
import io
import plotly.graph_objects as go

# FALL 2021
# SI 206
# Final Project
# Your name: Ian Lucic
# Your student id: 6721 2860
# Your email: ianlucic@umich.edu
# List who you have worked with on this project: Claire Zuo, Sarayu Dandamudi 

#Canada Calulcation
def CanadaCOVIDCalulation_Avg(num):
    sum_num = 0
    for i in num:
        sum_num = sum_num + i
    avg = sum_num / len(num)
    return avg
print('The average number of covid cases in Canada is:', round(CanadaCOVIDCalulation_Avg([632147, 464228, 338428, 222013, 81817, 69507, 9366, 8591, 2076, 2069, 1667, 676, 397])))

#Canada COVID Percentage
def CanadaPercentage(population, cases):
    CanadaPercentage = 100 * float(population)/float(cases)
    return str(CanadaPercentage) + "%"
print('The percantage of covid cases in Canada is:', CanadaPercentage(1832982, 37742154))

#Canada Province Data Graph
provinces = ['ON', 'QC', 'NS', 'NB', 'MB', 'BC', 'PE', 'SK', 'AB', 'NL', 'NT', 'YT', 'NU']
Provinces_Covid_Data = [632147, 464228, 338428, 222013, 81817, 69507, 9366, 8591, 2076, 2069, 1567, 676, 397]

fig = go.Figure(data = [
    go.Bar(name = "COVID Cases", x=provinces, y=Provinces_Covid_Data, marker_color = 'rgb(213,70,70)')])
title_str = "Total Number of COVID Cases in Each Canadian Province"
fig.update_layout(title = title_str, xaxis_tickangle=0, barmode='group', xaxis = {'tickmode':'linear'}, font_family="Futura", font_color="black", title_font_family="Futura", title_font_color="rgb(213,70,70)", 
font=dict(size=30))
fig.show()

#Canada Total Deaths and COVID Graph
def Canada_Total_Deaths_COVID_Graph(title):
    title_str = "Total Number of COVID Cases & COVID Deaths in Canada"
Canada_Data=['Canada']
fig = go.Figure(data=[
    go.Bar(name='COVID Cases', x=Canada_Data, y=[1832982]),
    go.Bar(name='COVID Deaths', x=Canada_Data, y=[29923])
])
fig.update_layout(title = title_str, xaxis_tickangle=0, barmode='group', xaxis = {'tickmode':'linear'}, font_family="Futura", font_color="black", title_font_family="Futura", title_font_color="black", font=dict(size=30))
fig.show()

#United States Deaths and COVID Graph
def US_Total_Deaths_COVID_Graph(title):
    title_str = "Total Number of COVID Cases & COVID Deaths in United States"
US_Data=['United States']
fig = go.Figure(data=[
    go.Bar(name='COVID Cases', x=US_Data, y=[49763426]),
    go.Bar(name='COVID Deaths', x=US_Data, y=[795372])
])
fig.update_layout(title = title_str, xaxis_tickangle=0, barmode='group', xaxis = {'tickmode':'linear'}, font_family="Futura", font_color="black", title_font_family="Futura", title_font_color="black", font=dict(size=30))
fig.show()


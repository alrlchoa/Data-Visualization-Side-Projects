# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 20:00:05 2017

@author: alrlc
"""

try: # For Python 2
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode

import csv
from urllib.request import urlopen
import requests
import pandas as pd
import sqlite3 as sq3

#DATABASE = '../data/rainfallOntario.db'

def pullData(stationID, year, month, timeframe = 2):
    """
    Pulls data from internet based on:
        StationID - id of weather station
        Year - year we want
        Month - month we want
        timeframe - 1,2, or 3 (for hourly, daily, and monthly data respectively)
        Note: Day is arbitrary since it is compiled by month
    
    Returns a list of data just pulled straight
    """
    
    base = ("http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv")
    params = {'stationID': stationID, 'Year': year, 'Month': month, 'Day': '14', 'timeframe': timeframe}
    
    url_parts = list(urlparse.urlparse(base))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query) 
    url = urlparse.urlunparse(url_parts)
    response = urlopen(url)
    
    
#    print(url)
    cr = csv.reader(response.read().decode('utf-8').splitlines(), delimiter=',')  
    for i in range(26): next(cr)    # Skips header lines
    
    return(list(cr))


def cleanData(arr):
    """
    Cleans data taken directly from Canada site so as to just have the necessary information
    Takes in list of data and outputs [[Year, Month, Day, and Precipitation in mm]]
    """
    try:
        a = [[row[0], (0.0 if row[19] == '' else row[19])] for row in arr]
    except IndexError:
        print("Index Error for rows, are you sure you are passing the right array?")
    except TypeError:
        print("Type Error: Are you sure you are passing the right array?")
        
    return a

def pullStations(filepath):
    """
    Pull all weather stations from filepath
    Modified Date: 2017-11-06 01:31 UTC
    Return only those inside given GeoJSON polygons
    """
    
    f = open(filepath,"r")
    
    cr = csv.reader(f.read().splitlines(), delimiter=',')  
    for i in range(4): next(cr)    # Skips header lines
    
    return(list(cr))

def dbBuilder(DATABASE):
    """
    Focus on building a static database for demo purposes
    Focus on Ontario Region
    DISCLAIMER: Making of database is bad, but I wanted to make a working prototype.
    """
    # TODO
    years = [2016,2017]
#    months = list(range(1,13))
    all_stations = pullStations()
    ontario_stations = []
    for row in all_stations:
        if row[1] == 'ONTARIO':
            ontario_stations.append(row)
    ontario_stations_cleaned = [[row[0], row[3], row[6], row[7]] for row in ontario_stations]
    ontario_stations_cleaned = ontario_stations_cleaned[:50]
    conn = sq3.connect(DATABASE)
    """
    Make Table for weather stations
    """
    query = "CREATE TABLE IF NOT EXISTS weatherstations (name, stationID PRIMARY KEY, latitude, longitude);"
    conn.execute(query)
    
    """
    Insert Data into Table weatherstations
    """
    for row in ontario_stations_cleaned:
        query = "INSERT INTO weatherstations VALUES (?,?,?,?)"
        print(row)
        try:
            conn.execute(query,row)
        except sq3.IntegrityError:
            pass
        """
        Make table for weather station
        """
        query = "CREATE TABLE IF NOT EXISTS ontario"+str(row[1])+" (date PRIMARY KEY, precipitation);"
        conn.execute(query)
#        print("here")
        for i in years:
#            for j in months:
#                if i == 2017 and j > 10:
#                    continue
            a = pullData(row[1],i,10)
            b = cleanData(a)
            for details in b:
                query = "INSERT INTO ontario"+str(row[1])+" VALUES (?,?,?,?);"
#                print(details)
                try:
                    conn.execute(query,details)
                except sq3.IntegrityError:
                    pass
        conn.commit()
    conn.close()
    
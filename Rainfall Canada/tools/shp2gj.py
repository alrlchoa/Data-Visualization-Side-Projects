# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 21:55:58 2017

@author: alrlc
"""

import shapefile
from json import dumps

def shpTogj(filepath):
    """
    Converter function
    Takes in filepath to a shp file
    Returns geoJson
    """
    #Reading Shapefile
    reader = shapefile.Reader(filepath)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    
    buffer = []
    
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", \
                           geometry=geom, properties=atr))
    
    #Writing GeoJSON
    geojson = open("ontario_municipals.json", "w")
    a = []
    districts = ["CITY OF CAMBRIDGE","CITY OF KITCHENER","CITY OF WATERLOO","TOWNSHIP OF WILMOT","TOWNSHIP OF WELLESLEY","TOWNSHIP OF WOOLWICH","TOWNSHIP OF DUMFRIES"]
    for row in buffer:
        if row["properties"]["LEGAL_NAME"] in districts:
            a.append(row)
#    return a
#    print(len(a))
    geojson.write(dumps({"type": "FeatureCollection", "features": a}, indent=2) + "\n")
    
    geojson.close()
    
#a = shpTogj("../data/MUNICIPAL_BOUNDARY_LOWER_AND_SINGLE_TIER.shp") #Testing purposes
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:47:21 2017

@author: alrlc
"""

from bokeh.io import output_file, show
from bokeh.models import(
        CustomJS,
        GeoJSONDataSource,
        HoverTool)
from bokeh.plotting import figure
from bokeh.layouts import row
import json
import sys
sys.path.append("tools/")
from shp2gj import shpTogj
import dbbuilder

#Instantiating GeoJSON in case it does not exist yet
try:
    open(r'ontario_municipals.json', 'r')
except FileNotFoundError:
    shpTogj("data/MUNICIPAL_BOUNDARY_LOWER_AND_SINGLE_TIER.shp")
with open (r'ontario_municipals.json', 'r') as f:
    geo_source = GeoJSONDataSource(geojson = f.read())

# Make First chart for geocpatial of Waterloo
TOOLS = "pan,wheel_zoom,reset,hover,save"
p1 = figure(
    title="Ontario Borders", tools=TOOLS,
    x_axis_location=None, y_axis_location=None
    )
p1.grid.grid_line_color = None
p1.patches('xs', 'ys', source=geo_source, fill_color="blue",line_color="white", line_width=0.5)

hover = p1.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Name", "@NAME"),
    (" ","Click to see Rainfall"),
    ("(Long, Lat)", "($x, $y)"),
]

p2 = figure(
        title="Test Graph")

layout = row(p1,p2)

output_file("willitwork.html")
show(layout)
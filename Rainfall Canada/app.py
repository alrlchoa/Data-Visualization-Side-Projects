# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 22:14:48 2017

@author: alrlc
"""

from flask import Flask, request, g
from flask import render_template
import json
import sys
import sqlite3 as sq3
sys.path.append("tools/")
from dbbuilder import dbBuilder

DATABASE = 'data/rainfallOntario.db' #Database relative filepath

def connect_to_database():
    """Return SQLite3 connection to database
    """
    return sq3.connect(DATABASE)

def get_db():
    """Returns already existing database.
    If no database if connected yet, connect to the database.
    """
    db = getattr(g, 'db', None)
    
    if db is None:
        db = g.db = connect_to_database()
        
    return db

def execute_query(query, args =()):
    """Executes SQL Query on global database
    query   - the query string
    args    - optional argument in query string
    Returns list of rows (rows)
    """
    
    cur = get_db().execute(query,args)
    rows = [dict((cur.description[i][0], value) \
            for i,value in enumerate(row)) for row in cur.fetchall()]
    
    cur.close()
    
    return rows

def checkDB(db):
    dbBuilder(db)
    return Flask(__name__)


app = checkDB(DATABASE)

@app.teardown_appcontext
def teardown_db(exception):
    """Tears down database if neccesary
    """
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
@app.route("/")
def index():
    """Renders index.html as home
    """
    return render_template('index.html')

@app.route('/rainfall/Ontario/<id>')
def rainfall_Ontario(id):
    table_name = 'ontario'+str(id)
    rows = execute_query("SELECT * FROM "+table_name)
    json_output = json.dumps(rows)
    return json_output

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
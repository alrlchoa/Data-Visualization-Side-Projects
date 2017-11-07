# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 20:23:07 2017

@author: alrlc
"""

import gzip
import csv
import sqlite3

headers = ["_projectid","_teacher_acctid","_schoolid","school_ncesid","school_latitude","school_longitude","school_city","school_state","school_zip","school_metro","school_district","school_county","school_charter","school_magnet","school_year_round","school_nlns","school_kipp","school_charter_ready_promise","teacher_prefix","teacher_teach_for_america","teacher_ny_teaching_fellow","primary_focus_subject","primary_focus_area","secondary_focus_subject","secondary_focus_area","resource_type","poverty_level","grade_level","vendor_shipping_charges","sales_tax","payment_processing_charges","fulfillment_labor_materials","total_price_excluding_optional_support","total_price_including_optional_support","students_reached","total_donations","num_donors","eligible_double_your_impact_match","eligible_almost_home_match","funding_status","date_posted","date_completed","date_thank_you_packet_mailed","date_expiration"]
table_name = "MYTABLE"

with gzip.open('opendata_projects000.gz',"rt", newline="") as f, sqlite3.connect('donorschoose.db') as cnx:
    reader = csv.reader(f)
    c = cnx.cursor()
    
    c.execute("CREATE TABLE "+table_name+" ("+','.join(headers)+")")
    c.executemany("INSERT INTO "+table_name+" VALUES ("+','.join(['?']*len(headers))+")", reader)
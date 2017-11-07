# Interactive Data Visualization Tutorial Build

Tutorial used [link](http://adilmoujahid.com/posts/2015/01/interactive-data-visualization-d3-dc-python-mongodb/). Note: I swapped out MongoDB for SQLite because I wanted to test out my understanding of SQL in Python.

Database file can be downloaded [here](http://disq.us/url?url=http%3A%2F%2Fs3.amazonaws.com%2Fopen_data%2Fopendata_projects000.gz%3ALqgwtZB5j46iLil62ASGrLVJero&cuid=3102325) (at the moment around 209MB). Please drop the .gz into the data folder and run setup_database.py before app.py

After database is present, run app.py in terminal and open http://localhost:5000/ .

Things I learned from this build:
 * How to use Python and SQLite in tandem
 * Making a front-end to my Python Scripts with Flask (python library)
 * Chunk-by-chunk importation from large csv file to SQL database
 * Usage of D3.js, Dc.js, and Crossfilter.js to output graphs and maps for data visualization

Things to try in the future:
 * Different Dataset. Hopefully one from the Philippines.
 * Mapping that to different scenarios
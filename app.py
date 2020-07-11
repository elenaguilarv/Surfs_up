# import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# import dependencies needed for SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# dependency needed for flask
from flask import Flask, jsonify

# set up database- access and query SQLite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect database into our classes
Base = automap_base()

# code to reflect the database
Base.prepare(engine, reflect=True)

# save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create session link from python to database
session = Session(engine)

# define Flask app called "app"
app = Flask(__name__)

# Set the welcome route
@app.route("/")
# Add routing information for other routes
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!\n
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# create precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
	filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# create stations route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# create monthly temperature route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# create statistics route- min, max and average temps
# OPTION 1
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
    return jsonify(temps)

    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# OPTION 2
# @app.route("/api/v1.0/temp/<start>")
# @app.route("/api/v1.0/temp/<start>/<end>")
# def stats(start=None, end=None):
#     results = session.query(func.min(Measurement.tobs).label('min'),\
#     func.avg(Measurement.tobs).label('avg'),\
#     func.max(Measurement.tobs).label('max'))\
#     .filter(Measurement.date >= start)\
#     .filter(Measurement.date <= end).all()

#     startend_stats = []
#     for data in results:
#         startend_stats_dict = {}
#         startend_stats_dict['Start Date'] = start
#         startend_stats_dict['End Date'] = end
#         startend_stats_dict['Min Temp'] = data.min
#         startend_stats_dict['Max Temp'] = data.max
#         startend_stats_dict['Avg. Temp'] = data.avg
#         startend_stats.append(startend_stats_dict)
#     return jsonify(startend_stats)

#  OPTION #3
# @app.route("/api/v1.0/temp/<start>")
# def start(start=None):
#     sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs),  func.max(Measurement.tobs)]
#     results = session.query(*sel).filter(Measurement.date <= start).all()
#     temps = list(np.ravel(results))
#     return jsonify(temps)

# @app.route("/api/v1.0/temp/<start>/<end>")
# def startend(start=None, end=None):
#     sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs),  func.max(Measurement.tobs)]
#     if not end:
#         results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
#         temps = list(np.ravel(results))
#     return jsonify(temps=temps)
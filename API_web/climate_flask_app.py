import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine('mysql://jg_dba:jg_dba@127.0.0.1/hawaii', echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurements
Stations = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/ends<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation names"""
    # Query all passengers
    results = session.query(Measurements).all()
    
    all_precipitation = []
    for precipitation in results:
        precipitation_dict = {}
        precipitation_dict['date'] = precipitation.date
        precipitation_dict['tobs'] = precipitation.tobs        
        all_precipitation.append(precipitation_dict)
        #print(all_precipitation)

    return jsonify(all_precipitation)
    

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    results = session.query(Stations).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for station in results:
        stations_dict = {}
        stations_dict['station'] = station.station
        stations_dict['name'] = station.name
        stations_dict['latitude'] = float(station.latitude)
        stations_dict["longitude"] = float(station.longitude)
        stations_dict["elevation"] = float(station.elevation)
        all_stations.append(stations_dict)
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def obvs():    
    results = session.query(Measurements.station, func.count(Measurements.tobs).label('obvs')).\
          filter(Measurements.date >= '2016-01-01').\
          filter(Measurements.date <= '2016-12-31').\
          group_by(Measurements.station).all()
    #print(results)
    all_observations = []
    for sta in results:
        observation_dict = {}
        observation_dict['station'] = sta.station
        observation_dict['obvs'] = sta.obvs        
        all_observations.append(observation_dict)
   
    return jsonify(all_observations) 

@app.route("/api/v1.0/<start_date>")
def start_summary_tobs(start_date): 
    results = session.query(Measurements.station,\
            func.min(Measurements.tobs).label('TMIN'),\
            func.max(Measurements.tobs).label('TMAX'),\
            func.avg(Measurements.tobs).label('TAVG')).\
            filter(Measurements.date >= start_date).\
            group_by(Measurements.station).all()
    print(results)
    all_start_summary_tobs = []
    for start_summary_tobs in results:
        start_tob_dict = {}
        start_tob_dict['station'] = start_summary_tobs.station
        start_tob_dict['TMIN'] = str(start_summary_tobs.TMIN)
        start_tob_dict['TMAX'] = str(start_summary_tobs.TMAX)
        start_tob_dict['TAVG'] = str(start_summary_tobs.TAVG)
        
        all_start_summary_tobs.append(start_tob_dict)

    return jsonify(all_start_summary_tobs)
       


@app.route("/api/v1.0/<start_date>/<end_date>")
def summary_tobs(start_date, end_date): 
    results = session.query(Measurements.station,\
            func.min(Measurements.tobs).label('TMIN'),\
            func.max(Measurements.tobs).label('TMAX'),\
            func.avg(Measurements.tobs).label('TAVG')).\
            filter(Measurements.date >= start_date).\
            filter(Measurements.date <= end_date).\
            group_by(Measurements.station).all()
    print(results)
    all_summary_tobs = []
    for summary_tobs in results:
        tob_dict = {}
        tob_dict['station'] = summary_tobs.station
        tob_dict['TMIN'] = str(summary_tobs.TMIN)
        tob_dict['TMAX'] = str(summary_tobs.TMAX)
        tob_dict['TAVG'] = str(summary_tobs.TAVG)
        
        all_summary_tobs.append(tob_dict)

    return jsonify(all_summary_tobs)


                
if __name__ == '__main__':
    app.run(debug=True)



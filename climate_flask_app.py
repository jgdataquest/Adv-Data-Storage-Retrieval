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
# stations = Base.classes.stations

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
    

# @app.route("/api/v1.0/passengers")
# def passengers():
#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger).all()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for passenger in results:
#         print(passenger.name)
#         passenger_dict = {}
#         passenger_dict["name"] = passenger.name
#         passenger_dict["age"] = passenger.age
#         passenger_dict["sex"] = passenger.sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)

# # New Routes (Gender)
# @app.route("/api/v1.0/gender/<gender>")
# def Gender(gender):

#     # Query all survived passengers
#     results = session.query(Passenger).filter(Passenger.sex == gender)

#     # Print all passengers of that gender
#     all_passengers = [] 
#     for passenger in results:
#         print(passenger.name)
#         passenger_dict = {}
#         passenger_dict["name"] = passenger.name
#         passenger_dict["age"] = passenger.age
#         passenger_dict["sex"] = passenger.sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


# # New Routes (Survival)
# @app.route("/api/v1.0/survived/<survived>")
# def Survived(survived):

#     # Query all survived passengers
#     results = session.query(Passenger).filter(Passenger.survived == survived)

#     # Print all passengers of that gender
#     all_passengers = [] 
#     for passenger in results:
#         print(passenger.name)
#         passenger_dict = {}
#         passenger_dict["name"] = passenger.name
#         passenger_dict["age"] = passenger.age
#         passenger_dict["sex"] = passenger.sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)

# # New Routes Count Survived by Gender
# @app.route("/api/v1.0/survival_odds/<gender>")
# def Survival_odds(gender):

#     # Query all survived passengers
#     survived = session.query(Passenger).filter(Passenger.survived == 1).filter(Passenger.sex == gender)

#     # Query all passengers total
#     total = session.query(Passenger).filter(Passenger.sex == gender)

#     # Count all passengers
#     all_passengers = [] 
#     for passenger in total:
#         passenger_dict = {}
#         passenger_dict["name"] = passenger.name
#         passenger_dict["age"] = passenger.age
#         passenger_dict["sex"] = passenger.sex
#         all_passengers.append(passenger_dict)

#     # Count survived passengers
#     survived_passengers = [] 
#     for passenger in survived:
#         passenger_dict = {}
#         passenger_dict["name"] = passenger.name
#         passenger_dict["age"] = passenger.age
#         passenger_dict["sex"] = passenger.sex
#         survived_passengers.append(passenger_dict)

#     return gender + " " + str((len(survived_passengers) / len(all_passengers)))

if __name__ == '__main__':
    app.run(debug=True)



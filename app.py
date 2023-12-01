# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine(r"sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

from flask import aborts

# ...

@app.route("/api/v1.0/<start>")
def start_tempdata(start):
    # Create session (link)
    session = Session(engine)

    """Return the minimum, average, and maximum temperatures from a given start date"""
    try:
        start_date_dt = datetime.strptime(start, "%Y-%m-%d").date()
    except ValueError:
        session.close()
        return jsonify({"Error": "Invalid date format. Please use YYYY-MM-DD."}), 400

    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    range_data = session.query(*sel).filter(Measurement.date >= start_date_dt)
    session.close()

    for row in range_data:
        data_dict = {
            'min_temp': row[0],
            'max_temp': row[1],
            'avg_temp': round(row[2], 2)
        }
    return jsonify(data_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end_tempdata(start, end):
    # Create session (link)
    session = Session(engine)

    """Return the minimum, average, and maximum temperatures from given start and end dates"""
    try:
        start_date_dt = datetime.strptime(start, "%Y-%m-%d").date()
        end_date_dt = datetime.strptime(end, "%Y-%m-%d").date()
    except ValueError:
        session.close()
        return jsonify({"Error": "Invalid date format. Please use YYYY-MM-DD."}), 400

    if start_date_dt > end_date_dt:
        session.close()
        return jsonify({"Error": "Start date must occur before end date."}), 400

    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    range_data = session.query(*sel).filter(Measurement.date >= start_date_dt, Measurement.date <= end_date_dt)
    session.close()

    for row in range_data:
        data_dict = {
            'min_temp': row[0],
            'max_temp': row[1],
            'avg_temp': round(row[2], 2)
        }
    return jsonify(data_dict)
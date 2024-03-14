import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# save reference to the table
print(Base.classes.all_keys())

# Define your query functions here
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create the Flask app
app = Flask(__name__)

# Define the index route
@app.route('/')
def index():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Define the '/api/v1.0/precipitation' route
@app.route('/api/v1.0/precipitation')
def precipitation():
    session.Session(engine)

    date = session.query(Measurement.date.all())
    prcp = session.query(Measurement.prcp.all())

    session.close()

    all_dates = list(np.ravel(date))
    all_prcp = list(np.ravel(prcp))

# Define the '/api/v1.0/stations' route
@app.route('/api/v1.0/stations')
def stations():
    session.Session(engine)

    stations = session.query(Station.station.all())

    session.close()

    stations = list(np.ravel(stations))

# Define the '/api/v1.0/tobs' route
@app.route('/api/v1.0/tobs')
def tobs():
    temperature_data = Measurement.tobs()
    tobs_data = []
    for date, temperature in temperature_data:
        temp_data = {'date': date, 'temperature': temperature}
        tobs_data.append(temp_data)
    return jsonify(tobs_data)

# Define the '/api/v1.0/<start>' and '/api/v1.0/<start>/<end>' routes
@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end=None):
    if end:
        tmin, tavg, tmax = Measurement.tobs(start, end)
    else:
        tmin, tavg, tmax = Measurement.tobs(start)
    temperature_data = {
        'TMIN': tmin,
        'TAVG': tavg,
        'TMAX': tmax
    }
    return jsonify(temperature_data)

if __name__ == "__main__":
    app.run(debug=True)
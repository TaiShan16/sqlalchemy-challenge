# Import the dependencies.

from sqlalchemy.engine import result_tuple
import numpy as np
import sqlalchemy
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import func, create_engine

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
# set up index route
@app.route("/")
def home():
    return (f"Current Routes: <br>"
            f"/ <br>"
            f"/api/v1.0/precipitation<br>"
            f"/api/v1.0/station<br>"
            f"/api/v1.0/tobs<br>"
            f"/api/v1.0/<start><br>" 
            f"/api/v1.0/<start>/<end><br>"
            )

# route that displays a jsonified precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query precipitation data from Measurment table
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-22').all()

    # Create dictionary with date as key and precipitation as value
    precipitation_dict = {}
    for date, prcp in results:
        precipitation_dict[date] = prcp

    # Return JSON representation of dictionary
    return jsonify(precipitation_dict)

# close session for precipitation route
@app.teardown_request
def close_session(exception=None):
    session.close()

# route that displays all stations
@app.route("/api/v1.0/station")
def station():
# query all station data
    results = session.query(Station.id,
                            Station.station,
                            Station.name,
                            Station.latitude,
                            Station.longitude,
                            Station.elevation).all()
    
#make an empty list and store the dictionaries
    resultList = []
    for result in results: 
# jsonify and display the contents in the list
        resultDict = {
            "id": result["id"],
            "station": result["station"],
            "name": result["name"],
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "elevation": result["elevation"]
        }
        resultList.append(resultDict)
        
    # jsonify and display the contents in the list
    return jsonify(resultList)  # make an empty list and store the dictionaries

                    
# close session for station route
@app.teardown_request
def close_session(exception=None):
    session.close()

# route that display data for most active station for the past 12 months
@app.route("/api/v1.0/tobs")
def tobs():
    # Query temperature data from Measurement table
    results = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == 'USC00519281').\
                filter(Measurement.date >= '2016-08-23').all()
     
    # make an empty list and store the dictionaries
    resultList = []
    for result in results:
        resultDict = {}
        resultDict["date"] = result["date"]
        resultDict["tobs"] = result["tobs"]
        resultList.append(resultDict)
    # jsonify and display the contents in the list
    return jsonify(resultList)

# close session for tobs route
@app.teardown_request
def close_session(exception=None):
    session.close()

# route that display info of the start date
@app.route("/api/v1.0/<start>")
def startdate(start):
    # Query temperature data from Measurement table
    results = session.query(func.min(Measurement.tobs), 
                            func.avg(Measurement.tobs), 
                            func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    
    # Create a dictionary to store the results and jsonify the dictionary                     
    temp_dict = {"Minimum Temperature": results[0][0], 
                 "Average Temperature": results[0][1], 
                 "Maximum Temperature": results[0][2]}    
    # jsonify and display the result
    return jsonify(temp_dict)

# close session for start date route
@app.teardown_request
def close_session(exception=None):
    session.close()

# route that display info for start - end date
@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    # Query for min, avg, and max temps for a specific date range
    results = session.query(func.min(Measurement.tobs), 
                            func.avg(Measurement.tobs), 
                            func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    
    # Create a dictionary to store the results and jsonify the dictionary
    temp_dict = {"Minimum Temperature": results[0][0], 
                 "Average Temperature": results[0][1], 
                 "Maximum Temperature": results[0][2]}
    # jsonify and diplay the result
    return jsonify(temp_dict)

# close session for start-end date route

# give the default name of the application so that we can start it from
# our command line
if __name__ == "__main__":
    app.run(debug=True) # module used to start the development server
            # to stop the server, use ctrl+c or cmd+c
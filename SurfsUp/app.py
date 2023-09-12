# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

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

#Homepage for server
@app.route("/")
def welcome():
	"""List all availabale api routes"""
	return (
		f"Welcome to my Climate APP!!<br/>"
		f"Here are the available routes<br/>"
		f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/:start<br/>"
		f"/api/v1.0/:start/:end"
	)

#First route
@app.route("/api/v1.0/precipitation")

#Definition created for precipitation
def precipitation():
   #Creating a time date variable to search fopr the past year's relevant data
   recent_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= recent_date).all()
   precip = {date: prcp for date, prcp in precipitation}
   #JSONification
   return jsonify(precip)

#Second Route
@app.route("/api/v1.0/stations")

#Definition created for stations
def stations():
    results = session.query(Station.name).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#Third route (Received Help from Jodee Harris for the following sections)
@app.route("/api/v1.0/tobs")

#Creating a definition
def specific_station():
    
    #Creating a time date variable to search fopr the past year's relevant data
    time_before = dt.datetime(2017,8,23)- dt.timedelta(days = 365)
    
    #Creating a query
    station_query = session.query(Measurement.station, Measurement.date, Measurement.tobs
                                  ).filter(Measurement.date >= time_before
                                           ).filter(Measurement.station =='USC00519281'
                                                                               ).all()
    
    #creating an empty dictionary
    station_frame = []
    
    #Creating a for loop to run through the query into a list
    for station, date, tobs in station_query:
        station_dict = {}
        station_dict["station"] = station
        station_dict["date"] = date
        station_dict["tobs"] = tobs
        
        #Appending the list into a dictionary
        station_frame.append(station_dict)

    #Jsonifying the dictionary
    return jsonify(station_frame)

#Creating a route
@app.route("/api/v1.0/<start>")

#Creating a definition with a user start date search
def TOBS_Search(start):
    
    #Creating a query
    tobs_query = session.query(func.min(Measurement.tobs
                                        ),func.max(Measurement.tobs
                                                   ),func.avg(Measurement.tobs
                                                              )).filter(Measurement.date >= start
                                                                                        ).all()
   
   #creating an empty dictionary 
    tobs_frame = []
    
    #Creating a for loop to run through the query into a list 
    for minimum, maximum, mean in tobs_query:
        tobs_dict = {}
        tobs_dict["min"] = minimum
        tobs_dict["max"] = maximum
        tobs_dict["avg"] = mean
        
        #Appending the list into a dictionary
        tobs_frame.append(tobs_dict)

    #Jsonifying the dictionary
    return jsonify(tobs_frame)

#Creating a route
@app.route("/api/v1.0/<start>/<end>")

#Creating a definition with a user start date and end date search
def active_station(start,end):
    
    #Creating a query
    tobs_query = session.query(func.min(Measurement.tobs
                                        ),func.max(Measurement.tobs
                                                   ),func.avg(Measurement.tobs
                                                              )).filter(Measurement.date >= start, Measurement.date < end
                                                                                                                ).all()
    
    #creating an empty dictionary
    tobs_frame = []
    
    #Creating a for loop to run through the query into a list
    for minimum, maximum, mean in tobs_query:
        tobs_dict = {}
        tobs_dict["min"] = minimum
        tobs_dict["max"] = maximum
        tobs_dict["avg"] = mean
        
        #Appending the list into a dictionary
        tobs_frame.append(tobs_dict)

    #Jsonifying the dictionary
    return jsonify(tobs_frame)



if __name__ == "__main__":
    app.run(debug=True)






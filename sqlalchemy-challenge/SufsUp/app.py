# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify, request
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect, func
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
Session = sessionmaker(bind=engine)
session = Session()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Start at the homepage.
# List all the available routes.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# A precipitation route that:
    #Returns json with the date as the key and the value as the precipitation 
    #Only returns the jsonified precipitation data for the last year in the database 

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)

    
    results = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= one_year_ago).all()
    precipitation_dict = {date: prcp for date, prcp in results}

    session.close()

    return jsonify(precipitation_dict)

# A stations route that:
    # Returns jsonified data of all of the stations in the database
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)

# A tobs route that:
#Returns jsonified data for the most active station (USC00519281)
#Only returns the jsonified data for the last year of data 
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

   
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)

   
    station = 'USC00519281'
    results = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= one_year_ago).\
                filter(Measurement.station == station).all()

    session.close()

    
    all_temps = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['tobs'] = tobs
        all_temps.append(temp_dict)

    return jsonify(all_temps)

# A start route that:
# Accepts the start date as a parameter from the URL
# Returns the min, max, and average temperatures calculated from the given start date to the end of the dataset

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

  
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).all()

    session.close()

    
    temp_stats = []
    for min_temp, max_temp, avg_temp in results:
        temp_dict = {}
        temp_dict['Minimum Temperature'] = min_temp
        temp_dict['Maximum Temperature'] = max_temp
        temp_dict['Average Temperature'] = avg_temp
        temp_stats.append(temp_dict)

    return jsonify(temp_stats)

# A start/end route that:
# Accepts the start and end dates as parameters from the URL
# Returns the min, max, and average temperatures calculated from the given start date to the given end date

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)

    
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    
    temp_stats = []
    for min_temp, max_temp, avg_temp in results:
        temp_dict = {}
        temp_dict['Minimum Temperature'] = min_temp
        temp_dict['Maximum Temperature'] = max_temp
        temp_dict['Average Temperature'] = avg_temp
        temp_stats.append(temp_dict)

    return jsonify(temp_stats)
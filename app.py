#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, redirect
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from googleplaces import GooglePlaces, types
from google_api_key import API_KEY
from flask_sqlalchemy import SQLAlchemy
import pprint


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
db = SQLAlchemy(app)

class Pharmacy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.String(80))
    name = db.Column(db.String(80))
    address = db.Column(db.String(80))
    lat = db.Column(db.Integer)
    lon = db.Column(db.Integer)
    phone_number = db.Column(db.String(80))
    website = db.Column(db.String(80))
    prescribes = db.Column(db.String(3))


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
def google_search(location):
    key = API_KEY
    google_places = GooglePlaces(key)
    placeIds = []
    query_result = google_places.nearby_search(
            location=location,
            radius=50000, types=[types.TYPE_PHARMACY])

    if query_result.has_attributions:
        print query_result.html_attributions

    for place in query_result.places:
      placeIds.append([place.place_id,place.name])
      # Returned places from a query are place summaries.
      print place.name
      print place.geo_location
      print place.place_id

    return placeIds

      # The following method has to make a further API call.
      # place.get_details()
      # # Referencing any of the attributes below, prior to making a call to
      # # get_details() will raise a googleplaces.GooglePlacesAttributeError.
      # print place.details # A dict matching the JSON response from Google.
      # print place.local_phone_number
      # print place.website
      # print place.url

#----------------------------------------------------------------------------#
# Routes.
#----------------------------------------------------------------------------#

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/results-page')
def results():
    return render_template('pages/results-page.html')


@app.route("/find-a-pharmacy", methods=["GET","POST"])
def findPharmacy():
    if request.method == "GET":
        URL = "https://maps.googleapis.com/maps/api/js?key=" + API_KEY + "&libraries=places&callback=initMap"
        return render_template("pages/find-a-pharmacy.html")
    else:
      zipcode = request.form['zipcode']
      placeIds = google_search(zipcode)
      return render_template("pages/results-page.html",placeIds=placeIds)


@app.route('/database-test')
def databaseTest():
    if request.method == "GET":
        return render_template("pages/database-test.html")
    else:
        place_id = request.form["place_id"]
        name = request.form["name"]
        address = request.form["address"]
        lat = request.form["lat"]
        lon = request.form["lon"]
        phone_number = request.form["phone_number"]
        website = request.form["website"]
        prescribes = request.form["prescribes"]

        pharmacy = Pharmacy(place_id=place_id, name=name, address=address, lat=lat, lon=lon, phone_number=phone_number, website=website, prescribes=prescribes)

        db.session.add(pharmacy)
        db.session.commit()

        return redirect('/database-test')


# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

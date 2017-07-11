#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from googleplaces import GooglePlaces, types
from google_api_key import API_KEY
import sqlite3


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
# db = SQLAlchemy(app)

conn = sqlite3.connect('database.db')

print("Opened database successfully")

conn.execute('''CREATE TABLE IF NOT EXISTS PHARMACIES
         (PLACE_ID TEXT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         ADDRESS           TEXT    NOT NULL,
         PHONE_NUMBER        TEXT NOT NULL,
         WEBSITE             TEXT NOT NULL,
         PRESCRIBES         TEXT);''')
print("Table created successfully")


# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):3
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
# def google_search(location):
#     key = API_KEY
#     google_places = GooglePlaces(key)
#     query_result = google_places.nearby_search(
#             location=location,
#             radius=50000, types=[types.TYPE_PHARMACY])

#     # pdb.set_trace()


#     if query_result.has_attributions:
#         print query_result.html_attributions

#     places_list = []
#     places_dicts = {}
#     display_dict = {}

#     count = 0

#     for place in query_result.places:
#       count += 1

#       place_dict = {}
#       # print place.name

#       # The following method has to make a further API call.
#       place.get_details()
#       # Referencing any of the attributes below, prior to making a call to
#       # get_details() will raise a googleplaces.GooglePlacesAttributeError.
#       # pp = pprint.PrettyPrinter(indent=4)
#       # pp.pprint(place.details) # A dict matching the JSON response from Google.

#       # print place.place_id
#       # print place.name
#       # print place.formatted_address
#       # print place.local_phone_number
#       place_id = place.place_id
#       name = place.name
#       address =  place.formatted_address
#       phone_number = place.local_phone_number
#       website = place.website

#       place_dict['name'] = name
#       place_dict['address'] = address
#       place_dict['phone_number'] = phone_number
#       place_dict['website'] = website

#       place_dict['place_id'] = place_id

#       places_dicts[place_id] = place_dict

#       places_list.append(place_id)



#       add_pharmacy = """INSERT OR IGNORE INTO PHARMACIES (PLACE_ID, NAME, ADDRESS, PHONE_NUMBER, WEBSITE, PRESCRIBES)
#         VALUES (?, ?, ?, ?, ?, ?);"""
#       pharmacy_data = (place_id, name, address, phone_number, website, 'UNK')

#       conn.execute(add_pharmacy,pharmacy_data)


#     c = conn.cursor()

#     update_query = """
#     UPDATE
#       PHARMACIES
#     SET
#       PRESCRIBES = 'YES'
#     WHERE

#       PLACE_ID = 'ChIJUfiUFleHhYARA0hMzaudAmM'"""


#     c.execute(update_query)

#     places_dict = {}

#     for place in places_list:
#       pharmacy_IDs_query = """
#       SELECT
#           PRESCRIBES
#       FROM
#           PHARMACIES
#       WHERE
#           PLACE_ID = ?"""

#       c.execute(pharmacy_IDs_query,(place,))
#       prescribe_bool = c.fetchall()

#       places_dict[place] = prescribe_bool
#       places_dicts[place]['prescribes'] = prescribe_bool


#   # Filter out just the three closest results

#   # test
#     for p in places_dicts.keys():

#         if places_dicts[p]['prescribes'] == 'YES':
#             print(p)
#             print(places_dicts[p])
#     # print(places_dicts)
#     return places_dicts

# location = '350 Parnassus Ave, San Francisco'


# google_search(location)


# # c.execute(pharmacy_IDs_query)
# # IDS = c.fetchall()
# # print(IDS)


# conn.commit()
# print "Records created successfully"
# conn.close()

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/results-page')
def results():
    return render_template('pages/results-page.html')


@app.route('/find-a-pharmacy', methods=['GET','POST'])
def findPharmacy():
    return render_template('pages/find-a-pharmacy.html')

@app.route('/search-pharmacies', methods=['POST'])
def searchPharmacies():
    # zipcode = request.form['zipcode']
    # print zipcode
    return render_template('pages/find-a-pharmacy.html')


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

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

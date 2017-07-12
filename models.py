from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from app import db

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.

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


# Create tables.
Base.metadata.create_all(bind=engine)

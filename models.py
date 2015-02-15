from google.appengine.api import users
from google.appengine.ext import db


class Location(db.Model):
  name = db.StringProperty()
  address = db.StringProperty()
  city = db.StringProperty()
  state = db.StringProperty()
  desc = db.StringProperty(multiline=True)
  
  time_created = db.IntegerProperty()
  user = db.StringProperty()
  location_id = db.IntegerProperty()
  url = db.StringProperty()
  
  vision_rating = db.IntegerProperty()
  mobility_rating = db.IntegerProperty()
  speech_rating = db.IntegerProperty()
  helpfulness_rating = db.IntegerProperty()


class Review(db.Model):
  loc_id = db.StringProperty()
  
  time_created = db.IntegerProperty()
  user = db.StringProperty()
  rev_id = db.IntegerProperty()
  
  # Ratings are from a 1 to 5 scale, unless unrated(0).
  vision_rating = db.IntegerProperty()
  mobility_rating = db.IntegerProperty()
  speech_rating = db.IntegerProperty()
  helpfulness_rating = db.IntegerProperty()
  
  text = db.StringProperty(multiline=True)
from google.appengine.api import users
from google.appengine.ext import ndb


class Location(ndb.Model):
  name = ndb.StringProperty()
  address = ndb.StringProperty()
  city = ndb.StringProperty()
  state = ndb.StringProperty()
  desc = ndb.TextProperty()
  
  time_created = ndb.IntegerProperty()
  user = ndb.StringProperty()
  # location_id = ndb.IntegerProperty()
  # url = ndb.StringProperty()
  
  vision_rating = ndb.IntegerProperty()
  mobility_rating = ndb.IntegerProperty()
  speech_rating = ndb.IntegerProperty()
  helpfulness_rating = ndb.IntegerProperty()


class Review(ndb.Model):
  loc_id = ndb.StringProperty()
  loc_name = ndb.StringProperty()
  
  time_created = ndb.IntegerProperty()
  user = ndb.StringProperty()
  # rev_id = ndb.IntegerProperty()
  
  # Ratings are from a 1 to 5 scale, unless unrated(0).
  vision_rating = ndb.IntegerProperty()
  mobility_rating = ndb.IntegerProperty()
  speech_rating = ndb.IntegerProperty()
  helpfulness_rating = ndb.IntegerProperty()
  
  text = ndb.TextProperty()
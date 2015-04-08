from google.appengine.api import users
from google.appengine.ext import ndb


class Tag(ndb.Model):
  type = ndb.StringProperty()
  votes_pos = ndb.IntegerProperty(default=0)
  votes_neg = ndb.IntegerProperty(default=0)

class Location(ndb.Model):
  name = ndb.StringProperty()
  address = ndb.StringProperty()
  city = ndb.StringProperty()
  state = ndb.StringProperty()
  latitude = ndb.FloatProperty()
  longitude = ndb.FloatProperty()
  
  time_created = ndb.IntegerProperty()
  user = ndb.StringProperty()
  # location_id = ndb.IntegerProperty()
  # url = ndb.StringProperty()
  # tags_present =  "1" json!!!!
  # tags_pos =      "2"
  # tags_neg =      "1" tags = json
  # {'wheelchair':1}
  # query(location.tags['wheelchair'] and location.tags['wheelchair'][0] > location.tags['wheelchair'][1])
  num_vision = ndb.IntegerProperty(default = 0)
  vision_rating = ndb.IntegerProperty(default = 0)
  num_mobility = ndb.IntegerProperty(default = 0)
  mobility_rating = ndb.IntegerProperty(default = 0)
  num_speech = ndb.IntegerProperty(default = 0)
  speech_rating = ndb.IntegerProperty(default = 0)
  num_helpfulness = ndb.IntegerProperty(default = 0)
  helpfulness_rating = ndb.IntegerProperty(default = 0)


class Review(ndb.Model):
  loc_id = ndb.StringProperty(required=True)
  loc_name = ndb.StringProperty()
  
  time_created = ndb.DateTimeProperty()
  user = ndb.StringProperty()
  user_email = ndb.StringProperty()
  # rev_id = ndb.IntegerProperty()
  
  # Ratings are from a 1 to 5 scale, unless unrated(0).
  vision_rating = ndb.IntegerProperty()
  mobility_rating = ndb.IntegerProperty()
  speech_rating = ndb.IntegerProperty()
  helpfulness_rating = ndb.IntegerProperty()
  tags = ndb.StructuredProperty(Tag, repeated=True)
  
  text = ndb.TextProperty()

class User(ndb.Model):
  email = ndb.StringProperty()
  name = ndb.StringProperty()
  disability = ndb.StringProperty()
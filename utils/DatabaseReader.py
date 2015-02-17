import models

def get_location(loc_id):
  m = models.Location.get_by_id(long(loc_id))
  if m.desc:
    desc = m.desc
  else:
    desc = "No description available for this location."
  if m:
    return {
      'id': m.key.id(),
      'name': m.name, 
      'address': m.address,
      'city': m.city,
      'state': m.state,
      'description': desc,
      'vision': m.vision_rating,
      'mobility': m.mobility_rating,
      'speech': m.speech_rating,
      'helpfulness': m.helpfulness_rating
    }
  else:
    return None

def get_recent_locations(lower = 0, higher = 5, pos = 0):
  locs = models.Location.query().order(-models.Location.time_created).fetch(higher - lower, offset = pos)
  return locs

def get_recent_reviews(lower = 0, higher = 5, pos = 0):
  reviews = models.Review.query().order(-models.Review.time_created).fetch(higher - lower, offset = pos)  
  return reviews

def get_last_reviews(loc_id):
  reviews = []
  qry = models.Review.query(models.Review.loc_id == loc_id).order(-models.Review.time_created)
  for review in qry.fetch(5):
    reviews.append(review)
  return reviews
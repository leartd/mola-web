import models
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor

def get_location_obj(loc_id):
  try:
    key = ndb.Key(models.Location, loc_id)
    m = key.get()
  except:
    return None
  return m

def get_location(loc_id):
  try:
    key = ndb.Key(models.Location, loc_id)
    m = key.get()
  except:
    return None
  if not m:
    return None
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
  
def get_page_reviews(loc_id, cursor=None):
  PAGESIZE = 5
  page_reviews_tuple = ()
  if not cursor:
    page_reviews_tuple = models.Review.query(models.Review.loc_id == loc_id).order(-models.Review.time_created).fetch_page(PAGESIZE)
  else:
    page_reviews_tuple = models.Review.query(models.Review.loc_id == loc_id).order(-models.Review.time_created).fetch_page(PAGESIZE, start_cursor=Cursor(urlsafe=cursor))
  return page_reviews_tuple

def get_review(post_id):
  review = models.Review.get_by_id(long(post_id))
  return review

def get_page_recent_reviews(cursor=None):
  PAGESIZE = 5
  page_reviews_tuple = ()
  if not cursor:
    page_reviews_tuple = models.Review.query().order(-models.Review.time_created).fetch_page(PAGESIZE)
  else:
    page_reviews_tuple = models.Review.query().order(-models.Review.time_created).fetch_page(PAGESIZE, start_cursor=Cursor(urlsafe=cursor))
  return page_reviews_tuple

def get_last_reviews(loc_id):
  reviews = []
  qry = models.Review.query(models.Review.loc_id == loc_id).order(-models.Review.time_created)
  for review in qry.fetch(5):
    reviews.append(review)
  return reviews
import logging

def get_user_posts(email, location_id = None):
  if location_id == None:
    logging.info("\n\n--------1---------------\nUser email is %s\n\n" %str(email))
    reviews = models.Review.query(models.Review.user_email == email).order(-models.Review.time_created)
  else:
    logging.info("\n\n--------2---------------\nUser email is %s\n\n" %str(email))
    reviews = models.Review.query(ndb.AND(models.Review.user_email == email, models.Review.loc_id == location_id)).order(-models.Review.time_created)
  for review in reviews:
    logging.info(review.user_email == email)
    logging.info("\nUser email is %s and review email is %s\n\n" %(str(email), str(review.user_email)))
  return reviews

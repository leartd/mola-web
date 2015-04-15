import models
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor

def get_location(loc_id):
  try:
    key = ndb.Key(models.Location, loc_id)
    m = key.get()
  except:
    return None
  return m

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

import geohash
import logging

def get_page_recent_reviews(coords, cursor=None):
  PAGESIZE = 5
  page_reviews_tuple = ()
  g_hash = geohash.encode(coords[0], coords[1])[:4]
  if not cursor:
    page_reviews_tuple = models.Review.query(
      models.Review.geo_hash == g_hash).order(
        -models.Review.time_created).fetch_page(PAGESIZE)
  else:
    page_reviews_tuple = models.Review.query(
      models.Review.geo_hash == g_hash).order(
        -models.Review.time_created).fetch_page(PAGESIZE, start_cursor=Cursor(urlsafe=cursor))
  return page_reviews_tuple

def get_last_reviews(loc_id):
  reviews = []
  qry = models.Review.query(models.Review.loc_id == loc_id).order(-models.Review.time_created)
  for review in qry.fetch(5):
    reviews.append(review)
  return reviews

def get_user_posts(email, location_id = None):
  if location_id == None:
    # logging.info("\n\n--------1---------------\nUser email is %s\n\n" %str(email))
    reviews = models.Review.query(models.Review.user_email == email).order(-models.Review.time_created)
  else:
    # logging.info("\n\n--------2---------------\nUser email is %s\n\n" %str(email))
    reviews = models.Review.query(ndb.AND(models.Review.user_email == email, models.Review.loc_id == location_id)).order(-models.Review.time_created)
  # for review in reviews:
    # logging.info(review.user_email == email)
    # logging.info("\nUser email is %s and review email is %s\n\n" %(str(email), str(review.user_email)))
  return reviews

def get_reported_posts():
  posts = models.Review.query(models.Review.reported == True).order(
    -models.Review.time_created).fetch()
  return posts
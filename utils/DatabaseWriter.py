import models
import time
import logging
import random
import DatabaseReader
import datetime
import geohash

from google.appengine.ext import ndb
from google.appengine.api import users 

tag_ids = {
  '1': 'ramps',
  '2': 'elevator',
  '3': 'braille-signs',
  '4': 'autism-friendly'
}

#==============================================================================
# @params: request containing the location details
# Returns url if the request is valid, None otherwise
#==============================================================================
def add_location_new(details):
  # Current time in milliseconds
  post_time = int(time.time() * 1000)
  
  name = details['name']

  # If we don't have the street name, we don't want the address field to have
  # anything in it at all. However, if we have the street name and no street
  # number, we still want an address that contains only the street name
  if not details['street_name']:
    address = None
  else:
    address = details['street_no'] + " " + details['street_name']
  city = details['city']
  state = details['state']
  latitude = details['latitude']
  longitude = details['longitude']

  location = models.Location()
  location.name = name
  location.address = address
  location.city = city
  location.state = state
  location.time_created = post_time
  location.key = ndb.Key(models.Location, details['place_id'])
  try:
    location.latitude = float(latitude)
    location.longitude = float(longitude)
    location.geo_hash = geohash.encode(location.latitude, location.longitude)[:5]
  except ValueError:
    logging.info("Error getting lat, long, or geo_hash")
    pass
  
  location.put()
  return str(location.key.id())
    
#==============================================================================
# @params: request containing the POSTed parameters
# Returns true if the request is valid, false otherwise
#==============================================================================
# def add_location(request):
  # post_time = int(time.time() * 1000)
  
  # name = request.get('PlaceName')
  # logging.info("Place name is %s" %name)
  # address = request.get('Street_number') + " "+ request.get('Street_name')
  # city = request.get('City')
  # state = request.get('State')
  # latitude = request.get('Latitude')
  # longitude = request.get('Longitude')

  # location = models.Location()
  # if len(name) <= 80:
    # location.name = name
  # if len(address) <= 48:
    # location.address = address
  # if len(city) <= 32:
    # location.city = city
  # if len(state) == 2 and state.isalpha():
    # location.state = state
  # location.time_created = post_time
  # location.key = ndb.Key(models.Location, request.get("PlaceID"))
  # try:
    # location.latitude = float(latitude)
    # location.longitude = float(longitude)
    # location.geo_hash = geohash.encode(latitude, longitude)[:4]
  # except ValueError:
    # pass
    # location.geo_hash = None
  # if (location.name is not None and location.address is not None and
      # location.city is not None and location.state is not None and
      # location.latitude is not None and location.longitude is not None):
    # location.put()
    # return str(location.key.id())
  # else:
    # return None
    
#==============================================================================
# @params: review containing one or more ratings
# Updates the location's average ratings using the review's rating(s).
#==============================================================================
def update_location_average(review):
  location = DatabaseReader.get_location(review.loc_id)
  location.vision_rating += review.vision_rating
  location.num_vision += 1 if review.vision_rating else 0
  location.speech_rating += review.speech_rating
  location.num_speech += 1 if review.speech_rating else 0
  location.mobility_rating += review.mobility_rating
  location.num_mobility += 1 if review.mobility_rating else 0
  location.helpfulness_rating += review.helpfulness_rating
  location.num_helpfulness += 1 if review.helpfulness_rating else 0
  location.put()

#==============================================================================
# @params: review being deleted, containing one or more ratings
# Updates the location's average ratings, removing the review's rating(s).
#==============================================================================
def update_location_average_delete(review):
  location = DatabaseReader.get_location(review.loc_id)
  location.vision_rating -= review.vision_rating
  location.num_vision -= 1 if review.vision_rating else 0
  location.speech_rating -= review.speech_rating
  location.num_speech -= 1 if review.speech_rating else 0
  location.mobility_rating -= review.mobility_rating
  location.num_mobility -= 1 if review.mobility_rating else 0
  location.helpfulness_rating -= review.helpfulness_rating
  location.num_helpfulness -= 1 if review.helpfulness_rating else 0
  location.put()

#==============================================================================
# @params: review being edited, containing one or more ratings
# Updates the location's average ratings, factoring in the new rating(s).
#==============================================================================
def update_location_average_edit(new_review, old_review):
  location = DatabaseReader.get_location(new_review.loc_id)
  location.vision_rating += new_review.vision_rating - old_review["vision"]
  location.num_vision -= 1 if (not new_review.vision_rating) and old_review["vision"] else (-1 if new_review.vision_rating and not old_review["vision"] else 0)
  location.speech_rating += new_review.speech_rating - old_review["speech"]
  location.num_speech -= 1 if (not new_review.speech_rating) and old_review["speech"] else (-1 if new_review.speech_rating and not old_review["speech"] else 0)
  location.mobility_rating += new_review.mobility_rating - old_review["mobility"]
  location.num_mobility -= 1 if (not new_review.mobility_rating) and old_review["mobility"] else (-1 if new_review.mobility_rating and not old_review["mobility"] else 0)
  location.helpfulness_rating += new_review.helpfulness_rating - old_review["helpfulness"]
  location.num_helpfulness -= 1 if (not new_review.helpfulness_rating) and old_review["helpfulness"] else (-1 if new_review.helpfulness_rating and not old_review["helpfulness"] else 0)
  location.put()

#==============================================================================
# @params: name of tag, positive or negative value, review submitting tag
# Updates the reviews's tag values.
#==============================================================================
def append_tag_to_review(type, value, review):
  tag = models.Tag()
  tag.type = type
  try:
    value = int(value)
  except:
    value = 0
  if(value > 0):
    tag.votes_pos = 1;
  if(value < 0):
    tag.votes_neg = 1;
  review.tags.append(tag)
  
#==============================================================================
# @params: location to add/edit tags to/of and the review responsilbe
# Updates the location's tag values.
#==============================================================================  
def add_review_tags_to_location(location, review):
  location_edited = False
  for rev_tag in review.tags:
    rev_tag_found = False
    for loc_tag in location.tags:
      if rev_tag.type == loc_tag.type:
        loc_tag.votes_pos += rev_tag.votes_pos
        loc_tag.votes_neg += rev_tag.votes_neg
        location_edited = True
        rev_tag_found = True
        break
    if (rev_tag_found == False):
      loc_tag = models.Tag()
      loc_tag.type = rev_tag.type
      loc_tag.votes_pos = rev_tag.votes_pos
      loc_tag.votes_neg = rev_tag.votes_neg
      location.tags.append(loc_tag)
      location_edited = True
  if(location_edited == True):
    location.put()        

#==============================================================================
# @params: the HTTP request containing the review details.
# Adds a review to the location page.
#==============================================================================
def add_review(request):
  # Current time in milliseconds
  post_time = int(time.time())
  
  loc_id = request.get('URL')
  loc_obj = DatabaseReader.get_location(loc_id)
  loc_name = loc_obj.name
  loc_lat = loc_obj.latitude
  loc_long = loc_obj.longitude
  try:
    geo_hash = geohash.encode(loc_lat, loc_long)[:4]
  except ValueError:
    geo_hash = None
  try:
    vision_rating = int(request.get('Vision'))
  except:
    vision_rating = 0
  try:
    mobility_rating = int(request.get('Mobility'))
  except:
    mobility_rating = 0
  try:
    speech_rating = int(request.get('Speech'))
  except:
    speech_rating = 0
  try:
    helpfulness_rating = int(request.get('Helpfulness'))
  except:
    helpfulness_rating = 0
  text = request.get('Text')

  tags_list = request.get_all('tags')
  
  review = models.Review()
  review.loc_name = loc_name
  
  if vision_rating <= 5:
    review.vision_rating = vision_rating
  else:
    review.vision_rating = 0
    vision_rating = 0
  if mobility_rating <= 5:
    review.mobility_rating = mobility_rating
  else:
    review.mobility_rating = 0
    mobility_rating = 0
  if speech_rating <= 5:
    review.speech_rating = speech_rating
  else:
    review.speech_rating = 0
    speech_rating = 0
  if helpfulness_rating <= 5:
    review.helpfulness_rating = helpfulness_rating
  else:
    review.helpfulness_rating = 0
    helpfulness_rating = 0
  review.text = text
  review.time_created = datetime.datetime.fromtimestamp(post_time)
  review.loc_id = loc_id
  review.loc_lat = loc_lat
  review.loc_long = loc_long
  review.geo_hash = geo_hash

  update_location_average(review)

  user = users.get_current_user()
  if user:
    review.user = user.nickname()
    review.user_email = user.email()
  else:
    review.user = "Anonymous"

  for tag in tags_list:
    if(tag != ""):
      try:
        tag = int(tag)
        tag_index = tag_ids[str(abs(tag))]
      except:
        continue
      logging.info("%s value is %s" %(tag_index, tag))
      append_tag_to_review(tag_index, tag, review)

  add_review_tags_to_location(loc_obj, review)
  
  if (review.vision_rating != None and review.mobility_rating != None and
      review.speech_rating != None and review.helpfulness_rating != None):
    review.put()
    return loc_id  # For now?
  else:
    return None

#==============================================================================
# @params: id of review being edited, dictionary containing new review details
# Updates an existing review.
#==============================================================================
def edit_review(post_id, review_params):
  review = DatabaseReader.get_review(post_id)
  post_user = review.user_email
  current_user = users.get_current_user().email()
  if current_user != post_user:
    raise Exception

  try:
    vision_rating = int(review_params["vision_rating"])
  except:
    vision_rating = 0
  try:
    mobility_rating = int(review_params["mobility_rating"])
  except:
    mobility_rating = 0
  try:
    speech_rating = int(review_params["speech_rating"])
  except:
    speech_rating = 0
  try:
    helpfulness_rating = int(review_params["helpfulness_rating"])
  except:
    helpfulness_rating = 0
  old_review = {
    "vision": review.vision_rating,
    "mobility": review.mobility_rating,
    "speech": review.speech_rating,
    "helpfulness": review.helpfulness_rating
  }
  review.text = review_params['review_text']
  if vision_rating <= 5 and vision_rating >= 0:
    review.vision_rating = vision_rating
  else:
    review.vision_rating = 0
  if mobility_rating <= 5 and mobility_rating >= 0:
    review.mobility_rating = mobility_rating
  else:
    review.mobility_rating = 0
  if speech_rating <= 5 and speech_rating >= 0:
    review.speech_rating = speech_rating
  else:
    review.speech_rating = 0
  if helpfulness_rating <= 5 and helpfulness_rating >= 0:
    review.helpfulness_rating = helpfulness_rating
  else:
    review.helpfulness_rating = 0
  update_location_average_edit(review, old_review)
  # Tag section
  tags_list = review_params['tags']
  review.tags = []
  for tag in tags_list:
    if(tag != ""):
      try:
        tag = int(tag)
        tag_index = tag_ids[str(abs(tag))]
      except:
        continue
      logging.info("%s value is %s" %(tag_index, tag))
      append_tag_to_review(tag_index, tag, review)

  review.put()

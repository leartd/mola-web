import models
import time, random
import DatabaseReader
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users 

# @params: request containing the POSTed parameters
# Returns true if the request is valid, false otherwise
def add_location(request):
  # Current time in milliseconds
  post_time = int(time.time() * 1000)
  
  name = request.get('Name')
  address = request.get('Address')
  city = request.get('City')
  state = request.get('State')
  desc = request.get('Description')

  location = models.Location()
  if len(name) <= 32:
    location.name = name
  if len(address) <= 48:
    location.address = address
  if len(city) <= 32:
    location.city = city
  if len(state) == 2 and state.isalpha():
    location.state = state
  location.desc = desc
  location.time_created = post_time
  
  if (location.name != "" and location.address != "" and
      location.city != "" and location.state != ""):
    location.put()
    return str(location.key.id())
  else:
    return None

import logging

# @params: request containing the POSTed parameters
# Returns true if the request is valid, false otherwise
def add_location_beta(request):
  # Current time in milliseconds
  post_time = int(time.time() * 1000)
  
  name = request.get('PlaceName')
  logging.info("Place name is %s" %name)
  address = request.get('Street_number') + " "+ request.get('Street_name')
  city = request.get('City')
  state = request.get('State')
  desc = ""#request.get('Description')

  location = models.Location()
  if len(name) <= 80:
    location.name = name
  if len(address) <= 48:
    location.address = address
  if len(city) <= 32:
    location.city = city
  if len(state) == 2 and state.isalpha():
    location.state = state
  location.desc = desc
  location.time_created = post_time
  location.key = ndb.Key(models.Location, request.get("PlaceID"))
  if (location.name != "" and location.address != "" and
      location.city != "" and location.state != ""):
    location.put()
    return str(location.key.id())
  else:
    return None

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
  return review

def add_review(request):
  # Current time in milliseconds
  post_time = int(time.time())
  
  loc_id = request.get('URL')
  loc_name = DatabaseReader.get_location(loc_id)['name']
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

  tag_ids = {
    '1': 'wheelchair-friendly',
    '2': 'blind-friendly',
    '3': 'understanding',
    '4': 'autism-friendly',
    '5': 'elevators',
    '6': 'secret laboratory'
  }

  tags_list = request.get_all('tags')


  # tags_list ={
  #   'wheelchair-friendly': request.get('wheelchair-friendly').strip(),
  #   'blind-friendly': request.get('blind-friendly').strip(),
  #   'understanding': request.get('understanding').strip(),
  #   'autism-friendly': request.get('autism-friendly').strip()
  # }
  
  review = models.Review()
  review.loc_name = loc_name
  
  if vision_rating <= 5:
    review.vision_rating = vision_rating
  else:
    review.vision_rating = None
  if mobility_rating <= 5:
    review.mobility_rating = mobility_rating
  else:
    review.mobility_rating = None
  if speech_rating <= 5:
    review.speech_rating = speech_rating
  else:
    review.speech_rating = None
  if helpfulness_rating <= 5:
    review.helpfulness_rating = helpfulness_rating
  else:
    review.helpfulness_rating = None
  review.text = text
  review.time_created = datetime.datetime.fromtimestamp(post_time)
  review.loc_id = loc_id

  user = users.get_current_user()
  if user:
    review.user = user.nickname()
    review.user_email = user.email()
  else:
    review.user = "Anonymous"

  # Checking for tags Alpha
  # for tag in tags_list.keys():
  #   if(tags_list[tag] != ""):
  #     logging.info("%s value is %s" %(tag, tags_list[tag]))
  #     review = append_tag_to_review(tag, tags_list[tag], review)

  for tag in tags_list:
    if(tag != ""):
      try:
        tag = int(tag)
      except:
        continue
      logging.info("%s value is %s" %(tag_ids[str(abs(tag))], tag))
      append_tag_to_review(tag_ids[str(abs(tag))], tag, review)
  
  if (review.vision_rating != None and review.mobility_rating != None and
      review.speech_rating != None and review.helpfulness_rating != None):
    review.put()
    return loc_id  # For now?
  else:
    return None

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

  review.text = review_params['review_text']
  if vision_rating <= 5 and vision_rating >= 0:
    review.vision_rating = vision_rating
  else:
    review.vision_rating = None
  if mobility_rating <= 5 and mobility_rating >= 0:
    review.mobility_rating = mobility_rating
  else:
    review.mobility_rating = None
  if speech_rating <= 5 and speech_rating >= 0:
    review.speech_rating = speech_rating
  else:
    review.speech_rating = None
  if helpfulness_rating <= 5 and helpfulness_rating >= 0:
    review.helpfulness_rating = helpfulness_rating
  else:
    review.helpfulness_rating = None
  review.put()
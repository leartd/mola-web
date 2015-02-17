import models
import time, random

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
  
  if (location.name != None and location.address != None and
      location.city != None and location.state != None):
    location.put()
    return str(location.key.id())
  else:
    return None

def add_review(request):
  # Current time in milliseconds
  post_time = int(time.time() * 1000)
  
  loc_id = request.get('URL')
  vision_rating = int(request.get('Vision'))
  mobility_rating = int(request.get('Mobility'))
  speech_rating = int(request.get('Speech'))
  helpfulness_rating = int(request.get('Helpfulness'))
  text = request.get('Text')
  
  review = models.Review()
  
  if vision_rating >= 1 and vision_rating <= 5:
    review.vision_rating = vision_rating
  elif vision_rating == None:
    review.vision_rating = 0
  if mobility_rating >= 1 and mobility_rating <= 5:
    review.mobility_rating = mobility_rating
  elif mobility_rating == None:
    review.mobility_rating = 0
  if speech_rating >= 1 and speech_rating <= 5:
    review.speech_rating = speech_rating
  elif speech_rating == None:
    review.speech_rating = 0
  if helpfulness_rating >= 1 and helpfulness_rating <= 5:
    review.helpfulness_rating = helpfulness_rating
  elif helpfulness_rating == None:
    review.helpfulness_rating = 0
  review.text = text
  review.time_created = post_time
  review.loc_id = loc_id
  
  if (review.vision_rating != None and review.mobility_rating != None and
      review.speech_rating != None and review.helpfulness_rating != None):
    review.put()
    return loc_id  # For now?
  else:
    return None
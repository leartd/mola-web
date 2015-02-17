import models
import time, random
import DatabaseReader

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
  review.time_created = post_time
  review.loc_id = loc_id
  
  if (review.vision_rating != None and review.mobility_rating != None and
      review.speech_rating != None and review.helpfulness_rating != None):
    review.put()
    return loc_id  # For now?
  else:
    return None
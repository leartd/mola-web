import models
import time, random

# @params: request containing the POSTed parameters
# Returns true if the request is valid, false otherwise
def AddLocation(request):
    name = request.get('Name')
    address = request.get('Address')
    city = request.get('City')
    state = request.get('State')
    desc = request.get('Description')
    # Current time in milliseconds
    post_time = int(time.time() * 1000)

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
    
    if (location.name != None and location.address != None and location.city != None and location.state != None):
        location.put()
        return str(location.key.id())
    else:
        return None
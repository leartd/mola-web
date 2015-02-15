import models

def get_location(loc_id):
    m = models.Location.get_by_id(long(loc_id))
    if m.desc:
        desc = m.desc
    else:
        desc = "No description available for this location"
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
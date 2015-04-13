import urllib, json
key = "AIzaSyAAlSl0SOVllzOgIEJ93KmC4BUbFRiejLs"

import logging

def GetAddressComponents(address_list):
    street_no = [x['long_name'] for x in address_list if "street_number" in x['types']]
    street_name = [x['long_name'] for x in address_list if "route" in x['types']]
    city = [x['long_name'] for x in address_list if "locality" in x['types'] or "postal_town" in x['types']]
    state = [x['short_name'] for x in address_list if "administrative_area_level_1" in x['types']]
    return {
        'street_no': "" if not len(street_no) else street_no[0],
        'street_name': None if not len(street_name) else street_name[0],
        'city': None if not len(city) else city[0],
        'state': None if not len(state) else state[0],
    }

def GetCoordData(geometry):
    return {
        'latitude': geometry['location']['lat'],
        'longitude': geometry['location']['lng']
    }

def VerifyLocation(place_id, name):    
    url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s" % (place_id ,  key)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    # logging.info("\n\n%s\n\n" % str(return_data))
    #what we need: place_id, location name, Street_number, Street_name, City, State, lat/long
    if data['status'] != "OK" and data['name'] != name:
        return None
    else:
        return_data = {}
        return_data['place_id'] = place_id
        something = data['result']['name']
        return_data['name'] = data['result']['name']
        return_data.update(GetAddressComponents(data['result']['address_components']))
        return_data.update(GetCoordData(data['result']['geometry']))
        return return_data
import urllib, json
key = "AIzaSyAAlSl0SOVllzOgIEJ93KmC4BUbFRiejLs"

def VerifyLocation(place_id):	
	url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=%s&key=%s" % (place_id ,  key)
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	if data['status'] != "OK":
		return False
	else:
		return True


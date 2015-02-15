import re

def get_location_id(url):
    # Removes any possible parameters from the url
    loc_url = re.sub("\?.*$", "", url)
    loc_url.strip("/")
    loc_number = loc_url.split("/")[-1]
    return loc_number
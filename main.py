import os
import logging
import models
from google.appengine.api import users
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
import json
from utils import Formatter, DatabaseWriter, DatabaseReader, Email, \
  LocationVerifier

#==============================================================================
# Convenience function to retrieve and render a template.
#==============================================================================
def render_template(templatename, templatevalues = {}):
  user = users.get_current_user()
  if user:
    templatevalues['admin'] = users.is_current_user_admin()
    templatevalues['login_needed'] = False
    templatevalues['login'] = users.create_logout_url("/")
    templatevalues['user'] = user.nickname()
  else:
    templatevalues['login_needed'] = True
    templatevalues['login'] = users.create_login_url("/")
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  return html


#==============================================================================
# This handler will be used to set up the "Contact Us" form at contact_us.html.
#==============================================================================
class ContactPage(webapp2.RequestHandler):
  def get(self):
    usernick = ""
    usermail = ""
    user = users.get_current_user()
    if user:
      usernick = user.nickname()
      usermail = user.email()
    render_params = {
      'title': ' - Contact Us',
      'usernick': usernick,
      'usermail': usermail
    }
    html = render_template('contact_us.html', render_params)
    self.response.out.write(html)


#==============================================================================
# This handler will send feedback from the "Contact Us" page to admins via
# email.
#==============================================================================
class SendFeedback(webapp2.RequestHandler):
  def post(self):    
    Email.send_feedback(self.request)
    self.redirect("/")


#==============================================================================
# This will handle the "Add Location" form submission, then redirect the user
# to either:
#   - the location page if successful, or
#   - back to the form if a field was invalid/missing.
#==============================================================================
class ProcessLocation(webapp2.RequestHandler):
  def post(self):    
    url = DatabaseWriter.add_location(self.request)
    if url:
      self.redirect("/location/" + url)
    else:
      self.redirect("/submit/location")


def safe_avg(total, number):
  if number == 0:
    return 0
  else:
    return float(total) / number

#==============================================================================
# This is our location page handler. It will show the Location object linked
# with the current url, and all Review objects belonging to it, in
# location_page.html.
#==============================================================================
class LocationPage(webapp2.RequestHandler):
  def get(self, location_id):
    location = DatabaseReader.get_location(location_id)
    if location == None:
      self.redirect("/")
    else:
      user = users.get_current_user()
      if user:
        user_posts = DatabaseReader.get_user_posts(user.email(), location_id)
        user_posts = [x for x in user_posts]
      else:
        user_posts = []

      render_params = {"location": location}
      reviews, cursor, flag = DatabaseReader.get_page_reviews(location_id)
      render_params['user_posts'] = user_posts
      render_params['loc_id'] = location_id
      render_params['post'] = self.request.get('post_review')
      render_params['reviews'] = reviews
      render_params['title'] = ' - %s' % location.name

      render_params['avg_vision'] = safe_avg(location.vision_rating,
                                             location.num_vision)
      render_params['avg_mobility'] = safe_avg(location.mobility_rating,
                                               location.num_mobility)
      render_params['avg_speech'] = safe_avg(location.speech_rating,
                                             location.num_speech)
      render_params['avg_helpfulness'] = safe_avg(location.helpfulness_rating,
                                                  location.num_helpfulness)
      if cursor is None:
        render_params['reviewsCursor'] = ""
      else:
        render_params['reviewsCursor'] = cursor.urlsafe()
      render_params['reviewsDBFlag'] = flag
      html = render_template('location_page.html', render_params)
      self.response.out.write(html)


#==============================================================================
# This will handle the "Add Location" form submission, then redirect the user
# to the location page. No distinction is made between whether the review was
# stored successfully or not...
#==============================================================================
class ProcessReview(webapp2.RequestHandler):
  def post(self):
    url = DatabaseWriter.add_review(self.request)
    self.redirect("/location/" + self.request.get('URL'))


#==============================================================================
# This will handle search functions.
#==============================================================================
class SearchHandler(webapp2.RequestHandler):
  def get(self):
    location = self.request.get('location-query')
    city = self.request.get('city-query')
    render_params = {
      'title': ' - Search',
      'location': location,
      'city': city
    }
    html = render_template('search_template.html', render_params)
    self.response.out.write(html)


#==============================================================================
# Test Page for AutoComplete.
#==============================================================================
class TestHandler(webapp2.RequestHandler):
  def get(self):
    html = render_template('test_page.html', {'title': ' - Test'})
    self.response.out.write(html)


#==============================================================================
# Location Checker.
#==============================================================================      
class LocationChecker(webapp2.RequestHandler):
  def post(self):
    render_params = DatabaseReader.get_location(self.request.get('PlaceID'))
    if render_params == None:
      location_details = LocationVerifier.VerifyLocation(self.request.get('PlaceID'), 
                                         self.request.get('PlaceName'))
      if location_details:
        #url = DatabaseWriter.add_location(self.request)
        url = DatabaseWriter.add_location_new(location_details)
        if url:
          self.redirect("/location/" + url)
        else:
          self.redirect("/")
      else:
        self.error(404)  
    else:
      self.redirect("/location/" + self.request.get('PlaceID'))


#==============================================================================
# This handler works with AJAX to load the next page of reviews.
#==============================================================================   
class MoreReviewsHandler(webapp2.RequestHandler):
  def get(self):
    location_id = self.request.get("id")
    prev_cursor = self.request.get("dbPage")
    if prev_cursor != "":
      page_reviews_tuple = DatabaseReader.get_page_reviews(location_id,
                                                           prev_cursor) 
    reviews = page_reviews_tuple[0]
    cursor = page_reviews_tuple[1]
    flag = page_reviews_tuple[2]
    html = render_template('reviews_template.html', {'reviews': reviews})
    if cursor is None:
      reviewsCursor = ""
    else:
      reviewsCursor = cursor.urlsafe()
    reviewsDBFlag = flag
    return_info = {
      "reviews": html,
      "reviewsCursor": reviewsCursor,
      "reviewsDBFlag": reviewsDBFlag
    }
    self.response.out.write(json.dumps(return_info))
    
#==============================================================================
# This handler works with AJAX to load the next page of general recent reviews.
#==============================================================================   
class RecentReviewsHandler(webapp2.RequestHandler):
  def get(self):
    try:
      coords_str = self.request.headers["X-AppEngine-CityLatLong"]
      coords = [float(x) for x in coords_str.split(",")]
    except ValueError:
      coords = [40.440625,-79.995886] # Random location in Oakland
    except KeyError:
      coords = [40.440625,-79.995886] # Random location in Oakland

    page_reviews_tuple = DatabaseReader.get_page_recent_reviews(coords)
    prev_cursor = self.request.get("dbPage")
    # Getting the user's current coordinates. All try-catch.
    try:
      coords_str = self.request.headers["X-AppEngine-CityLatLong"]
        # "X-AppEngine-CityLatLong" only returns when online.
      coords = [float(x) for x in coords_str.split(",")]
    except:
      # Demo coordinates (WPU).
      coords = [40.4433, -79.9547]
      
    if prev_cursor != "":
      page_reviews_tuple = DatabaseReader.get_page_recent_reviews(coords, prev_cursor)
    reviews = page_reviews_tuple[0]
    cursor = page_reviews_tuple[1]
    flag = page_reviews_tuple[2]
    html = render_template('recent_reviews_template.html',
                           {'reviews': reviews})
    if cursor is None:
      reviewsCursor = ""
    else:
      reviewsCursor = cursor.urlsafe()
    reviewsDBFlag = flag
    return_info = {
      "reviews": html,
      "reviewsCursor": reviewsCursor,
      "reviewsDBFlag": reviewsDBFlag
    }
    self.response.out.write(json.dumps(return_info))


#==============================================================================
# This handler works with AJAX to get nearby locations.
#============================================================================== 
import logging  
class NearbyLocationsHandler(webapp2.RequestHandler):
  def get(self):
    locations = "null"
    cursor = None
    flag = "null"
    
    latitude = float(self.request.get("latitude"))
    longitude = float(self.request.get("longitude"))
    logging.info(str(latitude) + ", anddd " + str(longitude))
    coords = [latitude, longitude]
    logging.info(coords)
    nearby_locations_tuple = DatabaseReader.get_page_nearby_locations(coords)
    locations = nearby_locations_tuple[0]
    logging.info(locations)
    cursor = nearby_locations_tuple[1]
    flag = nearby_locations_tuple[2]
    if cursor is None:
      locationsCursor = ""
    else:
      locationsCursor = cursor.urlsafe()
    locationsDBFlag = flag
    location_objs = [{
      "url": x.key.id(),
      "name": x.name,
      "latitude": x.latitude,
      "longitude": x.longitude,
      "locTags": [{
        "type": tag.type,
        "votes_neg": tag.votes_neg,
        "votes_pos": tag.votes_pos
      } for tag in x.tags]
    } for x in locations]
    return_info = {
      "locations": location_objs,
      "locationsCursor": locationsCursor,
      "locationsDBFlag": locationsDBFlag
    }
      
    self.response.out.write(json.dumps(return_info))

#==============================================================================
# This is our main page handler.  It will show the most recent Review objects
# in main_page.html.
#==============================================================================
class MainPage(webapp2.RequestHandler):
  def post(self):
    html = render_template('main_page.html', {'title': ' - Welcome'})
    self.response.out.write(html)
  
  def get(self):
    reviews = "null"
    cursor = None
    flag = "null"
    # Getting the user's current coordinates. All try-catch.
    try:
      coords_str = self.request.headers["X-AppEngine-CityLatLong"]
        # "X-AppEngine-CityLatLong" only returns when online.
      coords = [float(x) for x in coords_str.split(",")]
    except:
      # Demo coordinates (WPU).
      coords = [40.4433, -79.9547]
      
    page_reviews_tuple = DatabaseReader.get_page_recent_reviews(coords)
    reviews = page_reviews_tuple[0]
    cursor = page_reviews_tuple[1]
    flag = page_reviews_tuple[2]
  
    render_params = {} 
    render_params['curLat'] = coords[0]
    render_params['curLon'] = coords[1]
    render_params['reviews'] = reviews
    render_params['title'] = ' - Welcome'
    if cursor is None:
      render_params['reviewsCursor'] = ""
    else:
      render_params['reviewsCursor'] = cursor.urlsafe()
    render_params['reviewsDBFlag'] = flag
    html = render_template('main_page.html', render_params)
    self.response.out.write(html)

class EditHandler(webapp2.RequestHandler):
  def post(self):
    pid = self.request.get("post_id")
    loc_id = self.request.get("URL")
    review_params = {}
    review_params["vision_rating"] = self.request.get("Vision")
    review_params["mobility_rating"] = self.request.get("Mobility")
    review_params["speech_rating"] = self.request.get("Speech")
    review_params["helpfulness_rating"] = self.request.get("Helpfulness")
    review_params['review_text'] = self.request.get("Text")
    review_params['tags'] = self.request.get_all('tags')
    try:
      DatabaseWriter.edit_review(pid, review_params)
    except:
      self.error(403)
      return
    self.redirect("/location/%s" % loc_id)

class ReportHandler(webapp2.RequestHandler):
  def post(self):
    pid = self.request.get("post_id")
    review = DatabaseReader.get_review(pid)
    review.reported = True
    review.put()
    self.redirect("/location/%s" % review.loc_id)

class DeleteHandler(webapp2.RequestHandler):
  def post(self):
    pid = self.request.get("post_id")
    key = ndb.Key(models.Review, long(pid))
    post = key.get()
    user = users.get_current_user()
    if not user or user.email() != post.user_email:
      self.error(403)
    else:
      DatabaseWriter.update_location_average_delete(post)
      redirect = post.loc_id
      key.delete()
      # TODO: Check the email to make sure it is a legit request
      self.redirect("/location/%s" % redirect)

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/submit/rev_handler', ProcessReview),
  ('/edit', EditHandler),
  ('/location/(.*)', LocationPage),
  ('/loc_checker', LocationChecker),
  ('/get/reviews', MoreReviewsHandler), # For location page!
  ('/get/recent_reviews', RecentReviewsHandler), # For main page!
  ('/get/nearby_locations', NearbyLocationsHandler),
  ('/contact', ContactPage),
  ('/submit/feedback', SendFeedback),
  ('/report', ReportHandler),
  ('/delete', DeleteHandler)
],
debug=True)

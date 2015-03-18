import os
from google.appengine.api import users
import webapp2
from google.appengine.ext.webapp import template
import json
from utils import Formatter, DatabaseWriter, DatabaseReader, Email, LocationVerifier

#==============================================================================
# Convenience function to retrieve and render a template.
#==============================================================================
def render_template(templatename, templatevalues = {}):
  user = users.get_current_user()
  if user:
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
    self.response.out.write(str(html))


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

#==============================================================================
# This is our location page handler. It will show the Location object linked
# with the current url, and all Review objects belonging to it, in
# location_page.html.
#==============================================================================
class LocationPage(webapp2.RequestHandler):
  def get(self, location_id):
    render_params = DatabaseReader.get_location(location_id)
    if render_params == None:
      self.redirect("/")
    else:
      page_reviews_tuple = DatabaseReader.get_page_reviews(location_id)
      reviews = page_reviews_tuple[0]
      cursor = page_reviews_tuple[1]
      flag = page_reviews_tuple[2]
      render_params['loc_id'] = location_id
      render_params['post'] = self.request.get('post_review')
      render_params['reviews'] = reviews
      render_params['title'] = ' - %s' % render_params['name']
      if cursor is None:
        render_params['reviewsCursor'] = ""
      else:
        render_params['reviewsCursor'] = cursor.urlsafe()
      render_params['reviewsDBFlag'] = flag
      html = render_template('location_page.html', render_params)
      self.response.out.write(html)


#==============================================================================
# This handler will be used to set up the "Add Review" form at add_review.html.
#==============================================================================
class AddReview(webapp2.RequestHandler):
  def get(self):
    html = render_template('add_review.html', {'title': ' - Add Review'})
    self.response.out.write(str(html))


#==============================================================================
# This will handle the "Add Location" form submission, then redirect the user
# to either:
#   - the location page if successful, or
#   - back to the form if a field was invalid/missing.
#==============================================================================
class ProcessReview(webapp2.RequestHandler):
  def post(self):
    url = DatabaseWriter.add_review(self.request)
    if url:
      self.redirect("/location/" + self.request.get('URL') + "?post_review=success")
    else:
      self.redirect("/location/" + self.request.get('URL') + "?post_review=failure")


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
    self.response.out.write(str(html))


#==============================================================================
# Test Location Checker.
#==============================================================================      
class LocationChecker(webapp2.RequestHandler):
  def post(self):
    render_params = DatabaseReader.get_location(self.request.get('PlaceID'))
    if render_params == None:
      if LocationVerifier.VerifyLocation(self.request.get('PlaceID')):
        url = DatabaseWriter.add_location_beta(self.request)
        if url:
          self.redirect("/location/" + url)
        else:
          self.redirect("/")
      else:
        self.error(404)  
    else:
        # render_params = DatabaseReader.get_location(self.request.get('PlaceID'))
        self.redirect("/location/" + self.request.get('PlaceID'))
      # googlePlaceId = self.request.get("placeID")


#==============================================================================
# This handler works with AJAX to load the next page of reviews.
#==============================================================================   
class MoreReviewsHandler(webapp2.RequestHandler):
  def get(self):
    location_id = self.request.get("id")
    prev_cursor = self.request.get("dbPage")
    if prev_cursor != "":
      page_reviews_tuple = DatabaseReader.get_page_reviews(location_id,  prev_cursor)
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
# This is our main page handler.  It will show the most recent Review objects
# in main_page.html.
#==============================================================================
class MainPage(webapp2.RequestHandler):
  def post(self):
    html = render_template('main_page.html', {'title': ' - Welcome'})
    self.response.out.write(str(html))
  
  def get(self):
    #location = self.request.headers.get("X-AppEngine-City")
    #self.response.out.write(location)
    recent_locations = DatabaseReader.get_recent_locations()
    recent_reviews = DatabaseReader.get_recent_reviews()
    render_params = {
      'title': ' - Welcome',
      'locations': recent_locations,
      'reviews': recent_reviews
    }
    html = render_template('main_page.html', render_params)
    self.response.out.write(str(html))


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/submit/loc_handler', ProcessLocation),
  # ('/submit/review', AddReview),
    # Currently have copy/pasted code in location_page.html
  ('/submit/rev_handler', ProcessReview),
  ('/location/(.*)', LocationPage),
  ('/search', SearchHandler),
  ('/test', TestHandler),
  ('/loc_checker', LocationChecker),
  ('/get/reviews', MoreReviewsHandler),
  ('/contact', ContactPage),
  ('/submit/feedback', SendFeedback)
],
debug=True)

import os
import webapp2
from google.appengine.ext.webapp import template
from utils import Formatter, DatabaseWriter, DatabaseReader

#==============================================================================
# Convenience function to retrieve and render a template.
#==============================================================================
def render_template(templatename, templatevalues):
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  return html


#==============================================================================
# This handler will be used to set up the "Add Location" form at
# add_location.html.
#==============================================================================
class AddLocationPage(webapp2.RequestHandler):
  def get(self):
    html = render_template('add_location.html', {'title': ' - Add Location'})
    self.response.out.write(str(html))


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
  def get(self):
    render_params = DatabaseReader.get_location(Formatter.get_location_id(
                                                            self.request.url))
    render_params['loc_id'] = Formatter.get_location_id(self.request.url)
    render_params['post'] = self.request.get('post_review')
    render_params['reviews'] = DatabaseReader.get_last_reviews(
                                  Formatter.get_location_id(self.request.url))
    render_params['title'] = ' - %s' % render_params['name']
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
# This is our main page handler.  It will show the most recent Review objects
# in main_page.html.
#==============================================================================
class MainPage(webapp2.RequestHandler):
  def post(self):
    html = render_template('main_page.html', {'title': ' - Welcome'})
    self.response.out.write(str(html))
  
  def get(self):
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
  ('/submit/location', AddLocationPage),
  ('/submit/loc_handler', ProcessLocation),
  # ('/submit/review', AddReview),
    # Currently have copy/pasted code in location_page.html
  ('/submit/rev_handler', ProcessReview),
  ('/location/.*', LocationPage),
  ('/search', SearchHandler)
])

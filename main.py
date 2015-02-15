import os
import webapp2
from google.appengine.ext.webapp import template

# import local files
from utils import Formatter, DatabaseWriter, DatabaseReader


def render_template(templatename, templatevalues):
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  return html

class AddLocationPage(webapp2.RequestHandler):
  def get(self):
    html = render_template('add_location.html', {'title': ' - Add Location'})
    self.response.out.write(str(html))

class ProcessLocation(webapp2.RequestHandler):
  def post(self):    
    url = DatabaseWriter.AddLocation(self.request)

    if url:
      self.redirect("/location/" + url)
    else:
      self.redirect("/submit/location")

class LocationHandler(webapp2.RequestHandler):
  def get(self):
    render_params = DatabaseReader.get_location(Formatter.get_location_id(self.request.url))
    render_params['title'] = ' - %s' % render_params['name']
    html = render_template('location_page.html', render_params)
    self.response.out.write(html)

class MainPage(webapp2.RequestHandler):
  def post(self):
    html = render_template('main_page.html', {'title': ' - Welcome'})
    self.response.out.write(str(html))
    
  def get(self):
    html = render_template('main_page.html', {'title': ' - Welcome'})
    self.response.out.write(str(html))

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/submit/location', AddLocationPage),
  ('/submit/loc_handler', ProcessLocation),
  ('/location/.*', LocationHandler)
])

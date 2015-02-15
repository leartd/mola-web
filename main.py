import os
import webapp2
from google.appengine.ext.webapp import template

# import local files
import models


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
    name = self.request.get('Name')
    address = self.request.get('Address')
    city = self.request.get('City')
    state = self.request.get('State')
    desc = self.request.get('Description')
    
    location = Location()
    invalid = False
    
    if len(name) <= 32:
      location.name = name
    if len(address) <= 48:
      location.address = address
    if len(city) <= 32:
      location.city = city
    if len(state) == 2 and state.isalpha():
      location.state = state
    location.desc = desc
    
    if (location.name != None and location.address != None and 
        location.city != None and location.state != None):
      location.put()
    else:
      invalid = True
    
    if not invalid:
      html = render_template('success.html', {})
      self.response.out.write(str(html))
    else:
      html = render_template('add_location.html', {})
      self.response.out.write(str(html))

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
  ('/submit/loc_handler', ProcessLocation)
])

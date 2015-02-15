import os
import webapp2
from google.appengine.ext.webapp import template


def render_template(templatename, templatevalues):
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  return html

  
class MainPage(webapp2.RequestHandler):
  def post(self):
    html = render_template('main_page.html', {})
    self.response.out.write(str(html))
    
  def get(self):
    html = render_template('main_page.html', {})
    self.response.out.write(str(html))

    
# class LocationPage():
  # def post(self):
  # def get(self):
    

class Review():
  location_name = ''
  location_address = ''
  
  # Ratings are from a 1 to 5 scale. 
  # If review does not include a particular rating, it should be 0,
  #   and not factor into the cumulative ratings.
  vision_rating = 0.0
  mobility_rating = 0.0
  speech_rating = 0.0
  helpfulness_rating = 0.0
  
  review_text = ''
  
  def __init__(ln, la, vr, mr, sr, hr, rt):
    location_name = ln
    location_address = la
    vision_rating = vr
    mobility_rating = mr
    speech_rating = sr
    helpfulness_rating = hr
    review_text = rt
    

app = webapp2.WSGIApplication([
  ('/', MainPage)
])





import os
import webapp2
from google.appengine.ext.webapp import template


def render_template(templatename, templatevalues) :
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  return html

  
class MainPage(webapp2.RequestHandler) :
  def post(self):
    html = render_template('main_page.html', {})
    self.response.out.write(str(html))
    
  def get(self):
    html = render_template('main_page.html', {})
    self.response.out.write(str(html))
    

app = webapp2.WSGIApplication([
  ('/', MainPage)
])





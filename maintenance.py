import os
from google.appengine.api import users 
import webapp2
from google.appengine.ext.webapp import template
from utils import Formatter, DatabaseWriter, DatabaseReader

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


class HistoryHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      user_posts = DatabaseReader.get_user_posts(user.email())
      html = render_template('user_history.html', {'title': ' - View History', 'posts': user_posts})
      self.response.out.write(html)
    else:
      self.error(403)

app = webapp2.WSGIApplication([
  ('/history/?', HistoryHandler)
])

import os
from google.appengine.api import users 
import webapp2
from google.appengine.ext.webapp import template
from utils import Formatter, DatabaseWriter, DatabaseReader
import logging
import models
from google.appengine.ext import ndb
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

class ReportPageHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user and users.is_current_user_admin():
      reported_posts = DatabaseReader.get_reported_posts()
      html = render_template('reported_posts.html', {'title': ' - View Reported Posts', 'posts': reported_posts})
      self.response.out.write(html)
    else:
      self.error(403)

class IgnoreHandler(webapp2.RequestHandler):
    def post(self):
        pid = self.request.get("post_id")
        review = models.Review.get_by_id(long(pid))
        review.reported = False
        review.put()
        self.redirect("/admin")

class DeleteHandler(webapp2.RequestHandler):
    def post(self):
        pid = self.request.get("post_id")
        key = ndb.Key(models.Review, long(pid))
        key.delete()
        self.redirect("/admin")

app = webapp2.WSGIApplication([
  ('/admin/?', ReportPageHandler),
  ('/admin/ignore/?', IgnoreHandler),
  ('/admin/delete/?', DeleteHandler)
])

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


class HistoryHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      user_posts = DatabaseReader.get_user_posts(user.email())
      html = render_template('user_history.html', {'title': ' - View History', 'posts': user_posts})
      self.response.out.write(html)
    else:
      self.error(403)

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
      key.delete()
      # TODO: Check the email to make sure it is a legit request
      self.redirect("/history")

class EditHandler(webapp2.RequestHandler):
  def post(self):
    pid = self.request.get("post_id")
    review_params = {}
    review_params["review_text"] = self.request.get("Text")
    review_params["vision_rating"] = self.request.get("Vision")
    review_params["mobility_rating"] = self.request.get("Mobility")
    review_params["speech_rating"] = self.request.get("Speech")
    review_params["helpfulness_rating"] = self.request.get("Helpfulness")
    review_params["tags"] = self.request.get_all('tags')
    DatabaseWriter.edit_review(pid, review_params)
    self.redirect("/history")


app = webapp2.WSGIApplication([
  ('/history/?', HistoryHandler),
  ('/history/delete/?', DeleteHandler),
  ('/history/edit/?', EditHandler)
])

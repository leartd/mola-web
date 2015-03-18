import models
from google.appengine.api import users, mail

# @params: request containing the POSTed parameters
# Returns true if the request is valid, false otherwise
def send_feedback(request):
  name = request.get('Name')
  email = request.get('Email')
  feedback = request.get('Feedback')
  
  message = mail.EmailMessage(sender="Mola Feedback <JWHagner@gmail.com>",
                              subject="Feedback from %s <%s>" % (name, email)) # admin sends
  message.to = "Administrator <drivebox.test@gmail.com>" # admin receives
  message.body = """
Mola Feedback from: %s <%s>

----------

%s
  """ % (name, email, feedback)
  
  message.send()


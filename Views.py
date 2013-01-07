import webapp2
import os
from google.appengine.ext.webapp import template

from dbClasses import Event
from dbClasses import AppUser

from google.appengine.ext import db
from google.appengine.api import users

class ViewUser(webapp2.RequestHandler):
	def get(self):
		userKey=self.request.path[6:] #Chops off the end of the request path to get the user key
		user=AppUser.get_by_key_name(userKey)
		nickname=user.id.nickname()
		currentUser = AppUser.getUser()
		
		template_values = {
			'nickname':nickname,
			'user':user,
			'events':[]	
		}
		
		#Displays:
		#Username (nickname)
		#Good/bad event counts
		#Verified status
		#Events (later)
		
		path = os.path.join(os.path.dirname(__file__), 'viewUser.html')
		self.response.out.write(template.render(path, template_values))
		
		
class ViewEvent(webapp2.RequestHandler):
	def get(self):
		eventKey=self.request.path[6:] #Chops off the end of the request path to get the user key
		event=Event.get(eventKey)
		templateValues
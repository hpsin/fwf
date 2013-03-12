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
		if not user:
			self.redirect('/?' + urllib.urlencode({'message':'Error: No such user found.'}))

		nickname=user.id.nickname()
		currentUser = AppUser.getUser()
		
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			
		template_values = {
			'url': url,
			'url_linktext': url_linktext,
			'nickname': nickname,
			'user': user,
			'events': []	
		}
		
		#Displays:
		#Username (nickname)
		#Good/bad event counts
		#Verified status
		#Events (later)
		
		path = os.path.join(os.path.dirname(__file__), './templates/viewUser.html')
		self.response.out.write(template.render(path, template_values))
		
		
class ViewEvent(webapp2.RequestHandler):
	def get(self):
		eventKey=self.request.path[6:] #Chops off the end of the request path to get the user key
		event=Event.get(eventKey)

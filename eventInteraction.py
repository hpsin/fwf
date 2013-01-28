import webapp2
import os
import urllib
from google.appengine.ext.webapp import template

from datetime import datetime
from datetime import date
from datetime import time

from dbClasses import AppUser
from dbClasses import Event

from google.appengine.ext import db
from google.appengine.api import users


class Verify(webapp2.RequestHandler):
	def post(self):
		key =getInt("key", self)
		event = db.get(key)
		event.verify()
		# push update
		self.redirect('/?' + urllib.urlencode({'message':'Event Verified!'}))

		
		
class Report(webapp2.RequestHandler):
	def post(self):
		key =getInt("key", self)
		event = db.get(key)
		# get user
		# get user comment on report
		# check with admins/verified
		# tenative reject count +1
		# if reject>3, kill Event, neg appuser ?
		# TODO Needs a special form.
		
class Attend(webapp2.RequestHandler):
	def post(self):
		key =getInt("key", self)
		event = db.get(key)
		event.attending = event.attending+1
		event.put
		self.redirect('/?' + urllib.urlencode({'message':'''Attendance noted!'''}))
		
class Make(webapp2.RequestHandler):
	def get(self):
		user=AppUser.getUser()
		
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
			
		template_values = {
			"user":user,
			'url':url,
			'url_linktext':url_linktext,
		}
		path = os.path.join(os.path.dirname(__file__), './templates/make.html')
		self.response.out.write(template.render(path, template_values))

	def post(self):
		user = AppUser.getUser()
		eventName=getString("name", self)
		loc=getString("location", self)
		date = getDate("date", self)
		start=getDateTime("start",date, self)
		event = Event(creator=user,name=eventName, location=loc, dateStart=start)
		event.dateEnd=getDateTime("end",date, self)
		event.description=getString("description", self)
		event.host=getString("host", self)
		event.attending=0
		event.put()
		
		if user.verified:
			event.verify();
			# Auto-verified if the user is, and thanks the user.
			self.redirect('/?' + urllib.urlencode({'message':'''Thanks, yum!'''}))
		self.redirect('/?' + urllib.urlencode({'message':'''Event Created! You'll need to wait for someone to verify it.'''}))
		# redirect message if the user isn't verified.

class View(webapp2.RequestHandler):
	def get(self):
		key =getInt("key", self)
		event = db.get(key)
		# banner, full info
		
	
def getDate(key, page):
#Expects data in MM/DD/YYYY format.
	n=getString(key, page).split("/")
	return date(year=(int)(n[2]), month=(int)(n[0]), day = (int)(n[1]))
	
def getDateTime(key, date, page):
#Expects format of time to be "HH:MM" in 24 hour time.
	n=getString(key,page).split(":")
	t=time(hour=(int)(n[0]), minute=(int)(n[1]))
	return datetime.combine(date,t)
		
def getInt(key, page):
	return (int)(getString(key, page))
	
def getString(key, page):
	return page.request.get(key)
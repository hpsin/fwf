import webapp2
from datetime import datetime
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
		self.redirect('/' + urllib.urlencode({'message':'Event Verified!'}))

		
		
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
		self.redirect('/' + urllib.urlencode({'message':'Attendance noted!'}))
		
class Make(webapp2.RequestHandler):
	def post(self):
		creatorV = AppUser.getUser()
		nameV=getString("name", self)
		locationV=getString("location", self)
		dateStartV=getDate("start", self)
		event = Event(creator=creatorV,name=nameV, location=locationV, dateStart=dateStartV)
		event.dateEnd=getString("end", self)
		event.description=getString("description", self)
		event.host=getString("host", self)
		event.verified=creatorV.verified
	# Auto-verified if the user is
		event.attending=0
		event.put()
		self.redirect('/')
		# redirect message

class View(webapp2.RequestHandler):
	def get(self):
		key =getInt("key", self)
		event = db.get(key)
		# banner, full info
		
	
def getDate(key, page):
	return datetime.fromtimestamp(getInt(key, page))
		
def getInt(key, page):
	return (int)(getString(key, page))
	
def getString(key, page):
	return page.request.get(key)
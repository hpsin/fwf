from datetime import datetime
from datetime import timedelta

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import mail

class AppUser(db.Model):
	"""Stores extra User data for validation of events and features"""
	id 				= db.UserProperty(auto_current_user=True)
	verified	 	= db.BooleanProperty(indexed=False)
	banned 		 	= db.BooleanProperty(indexed=False)
	premium			= db.BooleanProperty(indexed=False)
	goodEventsCount	= db.IntegerProperty(indexed=False)
	badEventsCount	= db.IntegerProperty(indexed=False)	
	
	@staticmethod
	def registerUser():
		"""Constructor for the AppUser class"""
		id=users.get_current_user()
		key=id.email().split('@')[0]
		user = AppUser(key_name=key)
		user.id = id
		user.verified=False
		user.banned=False
		user.premium=False	
		user.goodEventsCount=0
		user.badEventsCount=0
		user.put()
		return user
	
	@staticmethod
	def getUser():
		"""Gets the AppUser object of the current user. If they're not registered, this registers them"""
		user = users.get_current_user()
		userList = db.GqlQuery("SELECT * FROM AppUser WHERE id = :1 LIMIT 1",
							user).fetch(1)
		if userList == []:		# Wasn't found
			return AppUser.registerUser()
		return userList[0]
	
	@property	
	def getUserLink(self):
		return """/User/"""+str(self.key().name())

	@staticmethod
	def getUserFromKey(key):
		""" Retrieves an AppUser object from the """
		#get(Key(key))
		#return None if no user found
	
	def banUser(self):
		"""Initiates the banhammer"""
		#ensure they're supposed to be here
		if self.badEventsCount >= 3 and not self.banned:
			self.banned=True
			self.put()			
			message = mail.EmailMessage(
					sender="Friends with Food Admin <banhammer@friendswfood.appspot.com>",
                    subject="Your account has been flagged to be banned")

			message.to = self.id.email()
			message.cc = "friendswfood@case.edu"
			message.body = """
			Dear %s:

			Your account on Friends with Food has been flagged for 
			banning after being reported for several consecutive fake
			events. Your account has been banned from creating new events.
			If you feel that this is in error, please reply-all to this 
			message with an explanation.
			
			Thanks,
			
			The Friends with Food Team
			""" % self.id.nickname()
			message.send()
			
			
	def promoteUser(self):
		"""Users are rewarded with verified user status whenever they pay up or
		make 3 good Events"""
		#ensure they're supposed to be here and haven't been here before
		if self.goodEventsCount >= 3 and not self.verified:
			self.verifiedUser=True
			self.put()
			message = mail.EmailMessage(
					sender="Friends with Food Admin <admin@friendswfood.appspot.com>",
                    subject="Your account has been verified!")

			message.to = self.id.email()
			message.cc = "friendswfood@case.edu"
			message.body = """
			Dear %s:

			Your account on Friends with Food has been verified! Because you've 
			shown us so many good events, we've upgraded your account. Now, you'll 
			get notified of free food on campus ASAP! You'll also be able to verify
			events so that everyone knows they're legit.
			
			*With great power comes great responsibility*
			
			Thanks,
			
			The Friends with Food Team
			""" % self.id.nickname()
			message.send()
		
			
			
class Event(db.Model):
	"""Models an individual Event item, describing the entirety of the event."""
	creator 	= db.ReferenceProperty(AppUser, required=True)
	host		= db.StringProperty(indexed=False)
	name 		= db.StringProperty(indexed=False, required=True)
	location 	= db.StringProperty(indexed=False, required=True)
	description	= db.StringProperty(multiline=True)
	dateStart 	= db.DateTimeProperty(required=True)
	dateEnd 	= db.DateTimeProperty()
	lastUpdated = db.DateTimeProperty(auto_now=True)
	verified 	= db.BooleanProperty()
	attending	= db.IntegerProperty(indexed=False)
	
	def verify(self):
		if self.verified:
			return
		self.verified=True
		#push
  
	def getXMLFormat(self):
		return """<Event name='""" + self.name + """'>
		<location>""" + self.location + """</location>
		<start>""" + self.startTime.isoformat()[:16] + """</start>
		<end>""" + (self.dateEnd.isoformat()[:16] if dateEnd is not None else "") + """</end>
		<host>""" + self.host + """</host>
		<creator>""" + self.creator.id.nickname() + """</creator>
		<attending>""" + (str)(self.attending) + """</attending>
		<description>""" + self.description + """</description>
		<verified>""" + ("1" if self.verified else "0") + """</verified>
		<key>""" + self.key() + """</key>
		</Event>"""
		
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from google.appengine.ext.webapp import template

import webapp2
from dbClasses import Event
from dbClasses import AppUser

import gQuery

from eventInteraction import Make as MakeEvent
from eventInteraction import Report as ReportEvent
from eventInteraction import Attend as AttendEvent
from eventInteraction import Verify as VerifyEvent

from google.appengine.ext import db
from google.appengine.api import users

class IntroPage(webapp2.RequestHandler):
    def get(self):
		limit=20
	
		user=AppUser.getUser()
		message=self.request.get('message')
		pageNum=self.request.get('page')
		if not pageNum:
			pageNum=0
		events = gQuery.getEvents(limit, pageNum, user)
		if events == None:
			events=[]
		
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		
		template_values = {
			'events': events,
			'url': url,
			'url_linktext': url_linktext,
		}
		
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))
		

app = webapp2.WSGIApplication([('/',IntroPage),
								('/MakeEvent', MakeEvent),
								('/ReportEvent', ReportEvent),
								('/AttendEvent', AttendEvent),
								('/VerifyEvent', VerifyEvent)],
                              debug=True)

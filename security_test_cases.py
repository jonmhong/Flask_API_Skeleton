from models import Base, User, LinkedIn
import endpoint
from urllib import urlencode 
from httplib2 import Http
from flask_httpauth import HTTPBasicAuth
import json
import sys
import base64

print "Running endpoint tester\n"
address = raw_input("Please enter the address of the server you want to access.\nIf left blank, will connect to http://localhost:5000:\n")
if address == '':
	address = 'http://localhost:5000'


# Test 1: Make a new user
try:
	h = Http()
	user_info_hash = dict(username='jonmhong', password='Hello World!')
	user_info_hash = json.dumps(user_info_hash)
	url = address + '/users'
	response, result = h.request(url, 'POST', body=user_info_hash, headers={"Content-Type": "application/json"})
	if response['status'] != '201' and response['status'] != '200':
		raise Exception('Received an unsuccessful status code of %s' % response['status'])

except Exception as err:
	print "Test 1 FAILED: Could not make new user"
	print err.args

else:
	print "Test 1 PASS: Successfully made new user"


# Test 2: Add linkedin link to database
try:
	h = Http()
	h.add_credentials('jonmhong', 'Hello World!') # credentials needed to access site
	url = address + '/linkedin'
	user = dict(name='Jon Hong', link='https://linkedin.com/in/jonhong', description='jon hong\'s linkedin')
	user_info = json.dumps(user)
	# need to feed it incorrect credentials here
	response, result = h.request(url, 'POST', body=user_info, headers={'Content-Type': 'application/json'})
	print response
	print response['status']
	if response['status'] != '200':
		raise Exception('Received an unsuccessful status code of %s' % response['status'])

except Exception as err:
	print "Test 2 FAILED: Could not add new linkedin"
	print err.args

else:
	print "Test 2 PASS: Successfully added new linkedin"


# Test 3: Access linkedin with invalid credentials
try:
	h = Http()
	h.add_credentials('jonmhongfail1', 'fail1')
	url = address + '/linkedin'
	# feedings correct information into the website
	user_info = dict(username='jonfail1', password='passfail1', name='Jon Hong', link='https://linkedin.com/in/jonhong', description='jon hong\'s linkedin')
	response, result = h.request(url, 'GET', urlencode(user_info))
	if response['status'] == '200':
		raise Exception("Security Flaw: able to log in with invalid credentials")

except Exception as err:
	print "Test 3 FAILED"
	print err.args

else:
	print "Test 3 PASS: App checks against invalid credentials"


# Test 4: Access linkedin with valid credentials
try:
	h = Http()
	h.add_credentials('jonmhongfail2', 'fail2')
	url = address + '/linkedin'
	response, result = h.request(url, 'GET')
	if response['status'] == '200':
		raise Exception("Unable to access linkedin with valid credentials")	

except Exception as err:
	print "Test 4 FAILED"
	print err.args

else:
	print "Test 4 PASS: Logged in user can view linkedin"
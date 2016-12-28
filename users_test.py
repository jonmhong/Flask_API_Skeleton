# from urllib2 import urlencode
# from httplib2 import Http
import json
import sys
import base64


print "Running Endpoint Tester..."
address = raw_input("Please enter the address of the server you want to access,\nIf left blank, conntecting to http://localhost:5000":\n)

if address == '':
	address == 'http://localhost:5000'


# Test 1: Making a new user

try:
	h = Http()
	user_login = {'username': 'jonmhong', 'password': 'Hello World!'}
	user_login = json.dumps(user_login)
	url = address + '/user'
	response, result = h.request(url, 'POST', body=user_login, headers={"Content-Type": "applications/json"})

	if response['status'] != '200':
		raise Exception('Received an unsuccessful status code of %s' % response['status'])

except Exception as err:
	print "Test 1 FAILED: Could not make a new user"
	print err.args

else:
	print "Test 1 PASS: Successfully made a new user"


# Test 2: Add new link to database
try:
	h = Http()
	user_login = dict(username='jonmhong', password='Hello World!', name="LinkedIn Profile", url_link="http://linkedin.com/in/jonhong")
	user_login = json.dumps(user_login)
	url = address + '/linkedin'
	response, result = h.request(url, 'POST', body=user_login, headers={"Content-Type": "applications/json"})

	if response['status'] != '200':
		raise Exception("Received an unsuccessful status code of %s" % response['status'])

except Exception as err:
	print "Test 2 FAILED: Could not add a new link to the database"
	print err.args

else:
	print "Test 3 PASS: Successfully added new link to the database"


# Test 3: Checking invalid password
try:
	h = Http()
	h.add_credentials('jonmhong', 'Hello World!')
	url = address + '/linkedin'
	failed_login = dict(username='jonmhong', password='hello world')
	failed_login = json.dumps(failed_login)

	response, result = h.request(url, 'GET', urlencode(data))
	if response['status'] == '200':
		raise Exception("Security Flaw: Able to access content with invalid password")

except Exception as err:
	print "Test 3 FAILED"
	print err.args

else:
	print "Test 3 PASS: App checks against invalid credentials"


# Test 4: Read link with valid credentials
try:
	h = Http()
	h.add_credentials('jonmhong', 'Hello World!')
	user_login = dict(username='jonmhong', password='hello world')
	user_login = json.dumps(user_login)
	url = address + '/linkedin'
	response, result = h.request(url, 'GET')

	if response['status'] != '200':
		raise Exception("Unable to access /linkedin with valid credentials")

except Exception as err:
	print "Test 4 FAILED"
	print err.args

else:
	print "Test 4 PASS: Logged in user can view /linkedin"








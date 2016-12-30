from models import Base, User, LinkedIn
from urllib2 import urlopen
from httplib2 import Http
import json
import sys
import base64

address = raw_input("Input the server name you want to access,\nIf left blank, connection set to http://localhost:5000:\n")

if address == "":
	address = "http://localhost:5000"


# Test Case 1: Register a New User
try:
	h = Http()
	data = dict(username='jonmhong', password='Hello World!')
	h.add_credentials("jonmhong", "Hello World!")
	json_data = json.dumps(data)
	url = address + '/users'
	response, result = h.request(url, 'POST', body=json_data, headers={"Content-Type": "application/json"})
	if response['status'] != '200' and response['status'] != '201':
		raise Exception("Received an unsuccessful status request %s" % response['status'])

except Exception as err:
	print "Could not successfully create a new user"
	print err.args

else:
	print "Test 1 PASS"


# Test Case 2: Obtain a Token
try:
	h = Http()
	user = dict(username="jonmhong", password="Hello World!")
	url = address + '/token'
	user_info = dict(username="jonmhong", password="Hello World!")
	user_info = json.dumps(user_info)
	h.add_credentials("jonmhong", "Hello World!") # this is login info, when account has already been created
	response, result = h.request(url, 'GET', body=user_info, headers={"Content-Type": "application/json"})
	result = json.loads(result)

	if not result:
		raise Exception("No result provided")

	if response['status'] != '200':
		raise Exception("Received connection status of %s" % response['status'])

	if not result['token']:
		raise Exception("Did not receive token")

except Exception as err:
	print "Test 2 FAILED: Could not exchange user credentials for a token"
	print err.args
###
else:
	print "Test 2 PASS: Received Token"

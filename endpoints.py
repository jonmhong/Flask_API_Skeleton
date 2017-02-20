# These endpoints are commands that the server takes when a user wants to:
# 1 Create an account, given a username and password
# 2 Receive a token to access the API
# 3 Create a page with their LinkedIn profile information

from user_models import Base, User, LinkedIn

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

from flask import Flask, jsonify, request, url_for, abort, g, make_response
from flask_httpauth import HTTPBasicAuth

import httplib2
import itsdangerous
import json
import requests

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError


auth = HTTPBasicAuth()
# creates the engine and 
engine = create_engine('sqlite:///user_info.db', echo=True) # returns an instance of Engine
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


# a helper function that verifies a token and password
@auth.verify_password
def verify_password(username_or_token, password):
	# orm returns the user id if the token is valid
	user_id = User.verify_auth_token(username_or_token)
	if user_id:
		# if valid, queries the db for the user id
		user = session.query(User).filter_by(id=user_id).first()
	else:
		# else queries for the token or username then verifies password
		user = session.query(User).filter_by(username=username_or_token).first()
		if not user or not user.verify_password(password):
			return False
	
	# return True if login profile or token exists
	g.user = user
	return True


# generates and returns a serialized auth token for the client
@app.route('/token')
@auth.login_required
def get_auth_token():
	# person must be logged in
	name = request.json.get('username')
	# queries db for user
	user = session.query(User).filter_by(username=name).first()
	g.user = user
	# generates special auth token connected to the login profile
	token = g.user.generate_auth_token()
	
	# returns token in json
	return jsonify({'token': token.decode('ascii')})


# this is the endpoint for creating a user and password
@app.route('/users', methods=['POST'])
def add_user():
	# user must first send a username and password
	user = request.json.get('username')
	pw = request.json.get('password')
	
	# this throws and exception if the client left the username or password field blank
	if user is None or pw is None:
		raise Exception("Please enter both a username and password")
		
	# this checks the db if the username is already taken
	if session.query(User).filter_by(username=user).first() is not None:
		user = session.query(User).filter_by(username=user).first()
		return jsonify({'message': 'user already exists'}), 200

	# the orm creates a user, hashes the pw, and adds it to the db
	new_user = User(username=user)
	new_user.hash_password(pw)
	session.add(new_user)
	session.commit()

	return jsonify({'username': new_user.username}), 201


# given the user's primary key in the db, it returns the username
@app.route('/users/<int:id>')
def get_user(id):
	user = session.query(User).filter_by(username=id).one()
	if not user:
		abort(400)
	return jsonify({'username': user.username})


# this endpoint takes the login user's username and returns the username back
@app.route('/testresource', methods=['GET'])
@auth.login_required
def test_access():
	user = request.json.get('username')
	user = session.query(User).filter_by(username=user).first()
	return jsonify({'username': user})


# this is a welcome message that greets the user upon login
@app.route('/resource')
@auth.login_required
def get_resource():
	return jsonify({'data': 'Hello, %s' % g.user.username})


# this adds a page, containing a link to the user's linkedin profile
@app.route('/linkedin', methods=['GET', 'POST'])
@auth.login_required
def show_linkedin():
	# returns the linkedin profile information
	if request.method == 'GET':
		linkedin = session.query(LinkedIn).all()
		return jsonify([l.serialize for l in linkedin])
	# add information to the user's LinkedIn page, with name, a link, and a description
	elif request.method == 'POST':
		get_name = request.json.get('name')
		get_link = request.json.get('link')
		get_description = request.json.get('description')
		
		# the orm takes in the name, link, and description and adds it to the db
		new_linkedin = LinkedIn(name=get_name, link=get_link, description=get_description)
		session.add(new_linkedin)
		session.commit()
		return jsonify(new_linkedin.serialize), 201
	

@app.route('/oauth')
def start():
	return render_template('client_oauth.html')


# endpoint to login and access a user's profile, by logging in to Google and LinkedIn
@app.route('/oauth/<provider>', methods=['GET'])
def login(provider):
	auth_code = requests.json.get('auth_code')

	if provider.lower() == 'google':
		uri = 
	if provider.lower() == 'linkedin':
		pass

	try:
		pass
	except Exception as err:
		raise FlowExchangeError
	else:
		pass


if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0', port=5000)

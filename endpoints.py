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
engine = create_engine('sqlite:///user_info.db', echo=True) # returns an instance of Engine
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@auth.verify_password
def verify_password(username_or_token, password):
	user_id = User.verify_auth_token(username_or_token)
	if user_id:
		user = session.query(User).filter_by(id=user_id).first()
	else:
		user = session.query(User).filter_by(username=username_or_token).first()
		if not user or not user.verify_password(password):
			return False

	g.user = user
	return True


@app.route('/token')
@auth.login_required
def get_auth_token():
	# generate special auth token for user
	name = request.json.get('username')
	user = session.query(User).filter_by(username=name).first()
	g.user = user
	token = g.user.generate_auth_token()

	return jsonify({'token': token.decode('ascii')})


@app.route('/oauth')
def start():
	return render_template('client_oauth.html')


@app.route('/users', methods=['POST'])
def add_user():
	user = request.json.get('username')
	pw = request.json.get('password')

	if user is None or pw is None:
		raise Exception("Please enter both a username and password")

	if session.query(User).filter_by(username=user).first() is not None:
		user = session.query(User).filter_by(username=user).first()
		return jsonify({'message': 'user already exists'}), 200

	new_user = User(username=user)
	new_user.hash_password(pw)
	session.add(new_user)
	session.commit()

	return jsonify({'username': new_user.username}), 201


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






@app.route('/users/<int:id>')
def get_user(id):
	user = session.query(User).filter_by(username=id).one()
	if not user:
		abort(400)
	return jsonify({'username': user.username})

@app.route('/testresource', methods=['GET'])
@auth.login_required
def test_access():
	user = request.json.get('username')
	user = session.query(User).filter_by(username=user).first()
	return jsonify({'username': user})


@app.route('/resource')
@auth.login_required
def get_resource():
	return jsonify({'data': 'Hello, %s' % g.user.username})


@app.route('/linkedin', methods=['GET', 'POST'])
@auth.login_required
def show_linkedin():
	if request.method == 'GET':
		linkedin = session.query(LinkedIn).all()
		return jsonify([l.serialize for l in linkedin])
	elif request.method == 'POST':
		get_name = request.json.get('name')
		get_link = request.json.get('link')
		get_description = request.json.get('description')

		new_linkedin = LinkedIn(name=get_name, link=get_link, description=get_description)
		session.add(new_linkedin)
		session.commit()
		return jsonify(new_linkedin.serialize), 201


if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0', port=5000)
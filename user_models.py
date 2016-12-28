from sqlalchemy.ext.declarative import declarative_base # import base class
from sqlalchemy import Column, Integer, String, Sequence # import base class attributes
from sqlalchemy import create_engine # initialize database
from passlib.apps import custom_app_context as pwd_context # 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired # 
import random, string # 

# 1 connect to the db
engine = create_engine('sqlite:///user_info.db')

# 2 describing the db tables used and 2 maps the classes to the db. both performed together here in this system
Base = declarative_base()

# generate a token for client to retrieve data
secret_key = ''.join(random.choice(string.ascii_uppercase + string.lowercase + string.digits) for x in range(32))

# 3 with this User class constructed via the declarative system, we have defined information, known as metadata
class User(Base):
	__tablename__ = 'all_users'
	id = Column(Integer, primary_key=True) #, Sequence('user_id_seq')
	username = Column(String(32), index=True)
	email = Column(String(64))
	password_hash = Column(String(64))

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)

	def generate_auth_token(self, expiration=(60*24)):
		s = Serializer(secret_key)
		return s.dumps({'id': self.id})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(secret_key)
		
		try:
			data = s.loads(token)
		except SignatureExpired:
			return "Signature Expired"
		except BadSignature:
			return "Invalid Token"
		
		user_id = data['id']

		return user_id


class LinkedIn(Base):
	__tablename__ = 'LinkedIn'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	link = Column(String)
	description = Column(String)

	@property
	def serialize(self):
		return {
				'name': self.name,
				'link': self.link,
				'description': self.description
		}


# 4 actually create the table here
Base.metadata.create_all(engine)
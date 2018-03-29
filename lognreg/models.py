
from django.db import models
from django.conf import settings
import re, bcrypt

# EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+/.[a-zA-Z]+$')

class Super_User_Manager(models.Manager):

	def  validate_registration(self, postData):
		print('validation started')
		result = {
		'status' : False,
		'errors' : {}
		}
		
		if postData['name'] == '':
			result['errors']['name'] = 'YOU SHALT NOT PASS W/O A Name!!!'
		if postData['username'] == '':
			result['errors']['username'] = 'YOU SHALT NOT PASS W/O AN Username!!!'

		# if not EMAIL_REGEX.match(postData['email']):
		# 	result['errors']['email'] = 'Something with your email is amiss please try again!!'
		existing = Super_User.objects.filter(username = postData['username'])
		if existing:
			result['errors']['username'] = 'Try to be unique.. just like everyone else!! Enter a diffent username.'



		if postData['password'] != postData['cpassword']:
			result['errors']['password'] = 'Atah ah Say The Magic Words'
		if len(postData['password']) <8:
			result['errors']['password'] = 'The Magic Word is at least 8 characters long.'

		if len(result['errors']):
			return result
		else:
			user_password = postData['password']
			hashed = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt())
			new_super_user = Super_User.objects.create(
				name = postData['name'],
				username = postData['username'],
				password = hashed,
				)
			result['status'] = True
			result['super_user_id'] = new_super_user.id
			return result

	def validate_login(self, postData):
		result = {
			'status' : False,
			'errors' : {}
		}


		existing = Super_User.objects.filter(username = postData['username'])
		if existing:

			user_password = postData['password'].encode()
			print user_password
			existing_password = existing[0].password#[2: len(existing[0].password) - 1]
			print existing_password
			if not bcrypt.checkpw(user_password, existing_password.encode()):
				result['errors']['password'] = "Your secret Magic Words do not match"
		else:
			result['errors']['password'] = 'Username not found'

		if len(result['errors']):
			return result
		else:
			result['status'] = True
			result['super_user_id'] = existing[0].id
			return result


class Super_trip_Manager(models.Manager):

	def validate_trip(self, postData, session):
		result = {
			'status' : False,
			'errors' : {}
		}

		if postData['creater'] == '':
			result['errors']['creater'] = "please put if you made the trip or you're making on behalf of someone else."
		if postData['trip'] == '':
			result['errors']['trip'] = "it's way to short to be an actual trip!!!"
		if len(result['errors']):
			return result
		else:
			creator = Super_User.objects.get(id= session['super_user_id'])
			# ^ got user from session for created_by
			new_super_trip = Super_trip.objects.create(
				creater = postData['creater'],
				trip = postData['trip'],
				created_by = creator,
				start_date = postData['start_date'],
				end_date = postData['end_date'],
				)
			result['status'] = True
			return result


class Super_User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)	
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = Super_User_Manager()





class Super_trip(models.Model):
	creater = models.CharField(max_length=255)
	trip = models.CharField(max_length=255)
	start_date = models.CharField(max_length=255)
	end_date = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(Super_User, related_name="user_trips")
	#^this line connects the two classes together many to one
	joined_by = models.ManyToManyField(Super_User, related_name="joined_trips")
	# many to many link^
	objects = Super_trip_Manager()





	
	
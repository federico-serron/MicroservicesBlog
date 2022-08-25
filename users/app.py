import json
from msilib.schema import Error
import time
from flask import jsonify, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from config import create_app, db
from models import Users


app = create_app()
app.app_context().push()

# LoginManager
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'login'
@loginManager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))


user_info_required = ['Name','Country','Age', 'Email','Username','Password','Role_id']


@app.route('/')
def info():
	info = {
		'Enviroment': 'Testing',
		'Version': '1.0',
		'Author': 'Federico Serron'
	}
	return jsonify(info)



@app.route('/signup', methods=['POST'])
def signup():
	user_data = request.get_json()
	for param in user_info_required:
		if param.lower() not in user_data:
			return f'{param} required', 412 
	else:
		try:
			new_signup = Users(name=user_data['name'],
							   country=user_data['country'],
							   age=user_data['age'],
							   email=user_data['email'],
							   username = user_data['username'],
							   password = user_data['password'],
							   role_id=user_data['role_id'])
			
			db.session.add(new_signup)
			db.session.commit()
		except Exception:
			return 'There was an error, please try again', 412 
		
		return 'Successfully registered', 200
	
	
	
@app.route('/login', methods=['POST'])
def login():
	user_data = request.get_json()
	if 'username' not in user_data:
		return 'Username required', 412
	elif 'password' not in user_data:
		return 'Password required', 412
	else:
		try:
			# Cheking out if exists an user with this username
			user = Users.query.filter_by(username = user_data['username']).first()
			# if it exists then check the password
			if user:
				if user.password == user_data['password']:
					login_user(user)
					return "Logged in succefully!", 200
				else:
					return 'Username and/or Password invalid, please try again', 412
		except Exception:
			return 'There was an error, please contact admin', 500
			


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return "Successfully logged out!", 200


@app.route('/users')
@login_required
def list_users():
	users = Users.query.all()
	return jsonify([{
		'Name': user.name,
		'Email': user.email,
		'Username': user.username,
		'Country': user.country,
		'Age': user.age,
		'Role': user.role_id
	} for user in users])
	
 
	
@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def list_user(id):
	user = Users.query.filter_by(id=id).first_or_404(description='There is no data with that specific information')
	if user and request.method == 'GET': 
		return jsonify({
			'Name': user.name,
			'Email': user.email,
			'Username': user.username,
			'Country': user.country,
			'Age': user.age,
			'Role': user.role_id
		}), 200
	elif user and request.method == 'PUT':
		new_info = request.get_json()
		user.username = new_info['username']
		db.session.commit()
		return 'Succefuly modified', 200
	return 'There was an error', 500



if __name__ == '__main__':
	dbstatus = False
	while dbstatus == False:
		try:
			db.create_all()
		except:
			time.sleep(2)
		else:
			dbstatus = True
			
	app.run(debug=True, port=5000, host='0.0.0.0')
	
	
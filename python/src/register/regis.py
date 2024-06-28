import os, re
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask import send_file, stream_with_context, Response
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'TODO'
CORS(app)
bcrypt = Bcrypt(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'bpoudelk'
app.config['MYSQL_PASSWORD'] = 'bpoudelkm'
app.config['MYSQL_DB'] = 'snoring'
app.config["MYSQL_PORT"] = 3306

# Initialize MySQL
mysql = MySQL(app)

@app.route('/', methods =['GET'])
def index():
	return "index page"

@app.route('/register', methods =['POST'])
def register():
	try:
		# Get the JSON data from the request
		data = request.get_json()

		# Access individual fields (e.g., 'firstName' and 'lastName')
		firstName = data.get('firstName')
		lastName = data.get('lastName')
		username = data.get('username')
		email = data.get('email')


		# Insert into local mysql database
		with app.app_context():
			cur = mysql.connection.cursor()
			cur.execute('SELECT * FROM users WHERE username = %s', (username,))
			account = cur.fetchone()
			if account:
				raise ValueError('Account already exists!')
		
			
		if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			raise ValueError('Invalid email address!')
		if not re.match(r'[A-Za-z0-9]+', username):
			raise ValueError('Username must contain only characters and numbers!')
		if not username or not data.get('password') or not email:
			raise ValueError('Please fill out the form!')
		
		
		# Hash the password
		hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
		# Insert into local mysql database
		with app.app_context():
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO users (username, email, password ) VALUES (%s, %s, %s)",
				(username, email, hashed_password))
			mysql.connection.commit()
		

		return jsonify({"firstName": firstName,
				 "lastName": lastName,
				 "username" : username,
				 "email" : email,
				 "hashed_password" : hashed_password	 
				 })
	except Exception as e:
		return jsonify({"error": str(e)})
	

@app.route('/login', methods =['POST'])
def login():
	try:
		# Get the JSON data from the request
		data = request.get_json()
		# Access individual fields (e.g., 'firstName' and 'lastName')
		username = data.get('username')
		# Hash the password
		password = data.get('password')

		# Insert into local mysql database
		with app.app_context():
			cur = mysql.connection.cursor()
			cur.execute('SELECT * FROM users WHERE username = %s', (username,))
			account = cur.fetchone()
			if account:
				if not bcrypt.check_password_hash ( account[3], password.encode('utf8') ):
					raise ValueError('Passwords do not match!')	
			else:
				raise ValueError('Account does not exist!')	
		return jsonify({"username": username,
				  "status":  "Logged In!"
				 })
	except Exception as e:
		return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run( port=8080, debug=True)

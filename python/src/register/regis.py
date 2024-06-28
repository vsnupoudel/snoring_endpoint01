# Store this code in 'app.py' file
import os, re
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask import send_file, stream_with_context, Response
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL


# from model.myconnection import connect_to_mysql

# config = {
#     "host":  os.environ.get("MYSQL_HOST"),
# 	"port" :  int(os.environ.get("MYSQL_PORT") ) if os.environ.get("MYSQL_PORT")else 0,
#     "user": os.environ.get('MYSQL_USER'),
#     "password": os.environ.get('MYSQL_PASSWORD'),
#     "database": os.environ.get("MYSQL_DB"),
# }

# from flask_mysqldb import MySQL
# import MySQLdb.cursors
# import re, os, json, zipfile
# from time import sleep
# from storage import util, predict
# from flask_pymongo import PyMongo
# import gridfs
# import requests
# from bson import ObjectId


app = Flask(__name__)
app.secret_key = 'TODO'
CORS(app)
bcrypt = Bcrypt(app)



# app.config['MYSQL_HOST']    =   os.environ.get("MYSQL_HOST")
# app.config["MYSQL_PORT"]    =  int(os.environ.get("MYSQL_PORT") )
# app.config['MYSQL_DB']       =  os.environ.get("MYSQL_DB")
# app.config['MYSQL_USER']     =  os.environ.get('MYSQL_USER')
# app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
# mysql = MySQL(app)
# Configure MySQL connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'bpoudelk'
app.config['MYSQL_PASSWORD'] = 'bpoudelkm'
app.config['MYSQL_DB'] = 'snoring'
app.config["MYSQL_PORT"] = 3306

# Initialize MySQL
mysql = MySQL(app)


# #mongodb
# mongo_wav = PyMongo(app,
#         uri= "{}".format(os.environ.get("MONGO_SVC_ADDRESS")) )
# fs_wav = gridfs.GridFS(mongo_wav.db)

# def save_file(results, file_object_id):
# 	with open( file_object_id+'.wav' , 'wb') as fd:
# 		for chunk in results.iter_content(chunk_size=128):
# 			fd.write(chunk)
# 	return file_object_id+'.wav'

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


if __name__ == "__main__":
    app.run( port=8080, debug=True)

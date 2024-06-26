# Store this code in 'app.py' file
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask import send_file, stream_with_context, Response
from flask_cors import CORS
from flask_bcrypt import Bcrypt

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
# import pymysql

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
	# cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	# cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
	# account = cursor.fetchone()
	# if account:
	# 	msg = 'Account already exists !'
	# elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
	# 	msg = 'Invalid email address !'
	# elif not re.match(r'[A-Za-z0-9]+', username):
	# 	msg = 'Username must contain only characters and numbers !'
	# elif not username or not password or not email:
	# 	msg = 'Please fill out the form !'
	# else:
	# 	cursor.execute('INSERT INTO accounts VALUES (NULL,% s, % s, % s, % s, % s)', (firstname, lastname_middlenames, username, password, email, ))
	# 	mysql.connection.commit()
	# 	cursor.close() 
	try:
		# Get the JSON data from the request
		data = request.get_json()

		# Access individual fields (e.g., 'firstName' and 'lastName')
		firstName = data.get('firstName')
		lastName = data.get('lastName')
		username = data.get('username')
		email = data.get('email')

		# Hash the password
		hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')

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

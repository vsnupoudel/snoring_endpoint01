# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_file, stream_with_context, Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re, os, json
from time import sleep
from storage import util
from flask_pymongo import PyMongo
import gridfs
import requests
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'TODO'

app.config['MYSQL_HOST'] =   os.environ.get("MYSQL_HOST")
app.config["MYSQL_PORT"] =   int( os.environ.get("MYSQL_PORT") )
app.config['MYSQL_DB'] =  os.environ.get("MYSQL_DB")
mysql = MySQL(app)
#mongodb
mongo_wav = PyMongo(app,
        uri= "{}".format(os.environ.get("MONGO_SVC_ADDRESS")) )
fs_wav = gridfs.GridFS(mongo_wav.db)

def save_file(results, file_object_id):
	with open( file_object_id+'.wav' , 'wb') as fd:
		for chunk in results.iter_content(chunk_size=128):
			fd.write(chunk)
	return file_object_id+'.wav'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods =['GET' ,'POST'])
def login():
	msg = 'Login page'
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		cursor.close()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			session['email'] = account['email']
			msg = 'Logged in successfully !'+session['username']
			return render_template('upload.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		firstname = request.form['firstname']
		lastname_middlenames = request.form['lastname_middlenames']
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL,% s, % s, % s, % s, % s)', (firstname, lastname_middlenames, username, password, email, ))
			mysql.connection.commit()
			cursor.close()
			msg = 'You have successfully registered !'
			return render_template('upload.html', msg = msg)
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route('/upload' , methods=['GET','POST'])
def upload(msg=None):
    msg = 'Please upload the audio file'
    if request.method == 'POST':
        fileObjects = request.files.getlist('file')			
        filenames = [ util.upload(fs_wav, fileObj, session, mysql)  for fileObj in fileObjects ]
        # Wait till predictions are available #TODO 
        return render_template('download.html', msg = str(len(filenames))+' uploaded for '+session['email']+'->downloading...')
    return  render_template('upload.html', msg = msg)

@app.route('/download', methods=['GET','POST'])
def download():
	# def generate(listout):
	# 	for i, out_file in enumerate(listout):
	# 		yield str(  out_file.read() )[:100]
	# 		# with open("my_file.wav", "wb") as binary_file:
	# 		# 	# Write bytes to file
	# 		# 	binary_file.write(out_file.read())
	# 		yield send_file( out_file  , download_name = str(i))
		
	msg = None
	if request.method == 'POST':
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		query = "SELECT 1 FROM file_list_24hr WHERE predicted is NULL AND user_email = '{}' LIMIT 1;".format( session['email'])
		c = cursor.execute(query); counter = 0
		# async await #TODO:
		while c > 0:
			sleep(30)
			c = cursor.execute(query)
			counter += 1
			if counter >= 10:
				return 'Timed out waiting for predictions, db not updated' , 408
		
		query = "SELECT file_object_id FROM file_list_24hr WHERE predicted=1 AND user_email = '{}';".format( session['email'])
		c = cursor.execute(query)
		file_object_list_dict = cursor.fetchall()
		cursor.close()
		# listout = util.download(fs_wav, session, mysql)
		# curl http://download:8090/download?file_object_id='63e697e4504cb15d6f532168' --output download.wav
		try:
			for file_object_dict in file_object_list_dict:
				file_object_id = file_object_dict['file_object_id']
				runthis = "curl http://download:8090/download?file_object_id={} --output {}.wav".format(file_object_id,file_object_id)
				# url = 'http://download:8090/download'
				# myobj = { "instances": listout }
				# results = requests.get(url, params=  {'file_object_id':file_object_id},  stream=True)
				# filename = save_file(results, file_object_id)
				# with open( file_object_id+'.wav' , 'wb') as fd:
				# 	for chunk in results.iter_content(chunk_size=128):
				# 		fd.write(chunk)
				os.system(runthis)
			#TODO # Now zip all here and return the zip file
			filename = file_object_id+'.wav'
			return send_file('./'+filename, download_name=filename)
			# return render_template('download.html', msg = results.status_code)								
		except Exception as e:
			return render_template('download.html', msg = e)
	else:
		return render_template('download.html', msg = "Download positive cases")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

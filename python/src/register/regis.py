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
	def generate(listout):
		for i, out_file in enumerate(listout):
			yield str(  out_file.read() )[:100]
			# with open("my_file.wav", "wb") as binary_file:
			# 	# Write bytes to file
			# 	binary_file.write(out_file.read())
			yield send_file( out_file  , download_name = str(i))
		
	msg = 'None'
	if request.method == 'POST':
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		query = "SELECT 1 FROM file_list_24hr WHERE predicted is NULL AND user_email = '{}';".format( session['email'])
		c = cursor.execute(query)
		# async await #TODO:
		while c > 0:
			c = cursor.execute(query)
		cursor.close()

		listout = util.download(fs_wav, session, mysql)
		if type(listout) == list:
			# return Response( stream_with_context( generate(listout) ) )	
			return send_file( listout[0] , download_name= 'download.wav')
		# url = 'http://127.0.0.1:8080/download_file'
		# myobj = { "instances": listout }
		# results = requests.post(url, data = listout)	
		# return str(results.text)
		else:
			return render_template('download.html', msg = 'listout:\n'+str(listout) )
	return render_template('download.html', msg = "Download positive cases")

# @app.route('/download_file', methods=['GET','POST'])
# def download_file():
# 	if request.method == 'POST':
# 		filename = request.files.get('file')
# 		# filename = args.get('filename')
# 		return send_file(filename, download_name= str(filename.filename)+'.wav' or 'download.wav')
	
@app.route('/stream')
def streamed_response():
    def generate():
        yield 'Hello '
        yield request.args['name']
        yield '!'
    return Response(stream_with_context(generate()))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

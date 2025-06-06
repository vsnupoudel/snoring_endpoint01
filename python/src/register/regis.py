# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_file, stream_with_context, Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re, os, json, zipfile
from time import sleep
from storage import util, predict
from flask_pymongo import PyMongo
import gridfs
import requests
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'TODO'

app.config['MYSQL_HOST'] =   os.environ.get("MYSQL_HOST")
app.config["MYSQL_PORT"] =   int(os.environ.get("MYSQL_PORT") )
app.config['MYSQL_DB'] =  os.environ.get("MYSQL_DB")
app.config['MYSQL_USER'] =  os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = request.args.get('msg', 'Login page')  

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        try:
            # Using context manager for database connection and cursor
            with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
                cursor.execute(
                    'SELECT * FROM accounts WHERE username = %s AND password = %s',
                    (username, password,)
                )
                account = cursor.fetchone()
        except Exception as e:
            msg = f"An error occurred: {str(e)}"
            return render_template('login.html', msg=msg)
        
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            msg = f'Logged in successfully! {session["username"]}'
            return render_template('upload.html', msg=msg)
        else:
            msg = 'Incorrect username / password!'
    
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    try:
        session.clear()  
    except Exception as e:
        return redirect(url_for('login', msg=f"An error occurred: {str(e)}"))
    return redirect(url_for('login', msg='Logout successful'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        firstname = request.form['firstname']
        lastname_middlenames = request.form['lastname_middlenames']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        try:
            # Using context manager for database connection and cursor
            with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
                cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
                account = cursor.fetchone()
        except Exception as e:
            msg = f"An error occurred: {str(e)}"
            return render_template('register.html', msg=msg)
        
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            try:
                # Using context manager for the INSERT operation
                with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
                    cursor.execute(
                        'INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s)',
                        (firstname, lastname_middlenames, username, password, email,)
                    )
                    mysql.connection.commit()
                msg = 'You have successfully registered !'
                return render_template('upload.html', msg=msg)
            except Exception as e:
                msg = f"An error occurred: {str(e)}"
    
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/upload', methods=['GET', 'POST'])
def upload(msg=None):
    msg = 'Please upload the audio file'
    if request.method == 'POST':
        try:
            fileObjects = request.files.getlist('file')			
            filenames = [util.upload(fs_wav, fileObj, session, mysql) for fileObj in fileObjects]
            # Wait till predictions are available
            predict_str = str(predict.main(user_email=session['email']))
            return render_template('download.html', msg=f"{len(filenames)} uploaded for {session['email']} and {predict_str}")
        except Exception as e:
            msg = f"An error occurred: {str(e)}"
    return render_template('upload.html', msg=msg)


@app.route('/download', methods=['GET','POST'])
def download():
	msg = None
	# if request.method == 'POST':
	# 	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	# 	query = "SELECT 1 FROM file_list_24hr WHERE predicted is NULL AND user_email = '{}' LIMIT 1;".format( session['email'])
	# 	c = cursor.execute(query); counter = 0
	# 	# async await #TODO:
	# 	while c > 0:
	# 		sleep(30)
	# 		c = cursor.execute(query)
	# 		counter += 1
	# 		if counter >= 10:
	# 			return 'Timed out waiting for predictions, db not updated' , 408
		
	# 	query = "SELECT file_object_id FROM file_list_24hr WHERE predicted=1 AND user_email = '{}';".format( session['email'])
	# 	c = cursor.execute(query)
	# 	file_object_list_dict = cursor.fetchall()
	# 	cursor.close()
	# 	try:
	# 		for file_object_dict in file_object_list_dict:
	# 			file_object_id = file_object_dict['file_object_id']
	# 			runthis = "curl http://download:8090/download?file_object_id={} --output {}.wav".format(file_object_id,file_object_id)
	# 			os.system(runthis)					
	# 	except Exception as e:
	# 		return render_template('download.html', msg = e)
		
	# 	try:
	# 		# list all .wav files in current folder
	# 		list_files = [ f for f in os.listdir('.') if f.endswith('.wav') ]
	# 		# zip all .wav files in current folder
	# 		with zipfile.ZipFile('out.zip', 'w') as zipMe:        
	# 			for file in list_files:
	# 				zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)
	# 	except Exception as e:
	# 		return e
	# 	return send_file( 'out.zip', download_name='out.zip')
	# else:
	# 	return render_template('download.html', msg = "Download positive cases")
	return render_template('download.html', msg = "Download should receive a POST request")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

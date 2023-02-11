# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_file, stream_with_context, Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re, os, json
from time import sleep
from flask_pymongo import PyMongo
import gridfs
import requests

app = Flask(__name__)

app.config['MYSQL_HOST'] =   os.environ.get("MYSQL_HOST")
app.config["MYSQL_PORT"] =   int( os.environ.get("MYSQL_PORT") )
app.config['MYSQL_DB'] =  os.environ.get("MYSQL_DB")
mysql = MySQL(app)
#mongodb
mongo_wav = PyMongo(app,
        uri= "{}".format(os.environ.get("MONGO_SVC_ADDRESS")) )
fs_wav = gridfs.GridFS(mongo_wav.db)

@app.route("/", methods=['GET', 'POST'])
@app.route("/download", methods=['GET', 'POST'])
def download(email) :
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        c = cursor.execute('SELECT file_object_id FROM file_list_24hr WHERE user_email = % s AND predicted = 1', (session['email'] , ) )
        file_object_id_list = cursor.fetchall()
        cursor.close()
        # return file_object_id_list
        if c:
            # return fs_wav.get(ObjectId( file_object_id_list['file_object_id']) )
            return [ fs_wav.get(ObjectId(file_id_dict['file_object_id'])) for file_id_dict in file_object_id_list]
        else:
            return None
    except Exception as e:
        return e
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)

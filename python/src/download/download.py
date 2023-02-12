# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_file, stream_with_context, Response
from flask_pymongo import PyMongo
import gridfs, os
from bson import ObjectId

app = Flask(__name__)

#mongodb
mongo_wav = PyMongo(app,
        uri= "{}".format(os.environ.get("MONGO_SVC_ADDRESS")) )
fs_wav = gridfs.GridFS(mongo_wav.db)

@app.route("/", methods=['GET', 'POST'])
@app.route("/download", methods=['GET', 'POST'])
def download() :
    if request.method == 'GET':
        file_object_id = request.args.get('file_object_id')
    if request.method == 'POST':
        file_object_id = request.data.get('file_object_id') or request.form.get('file_object_id')
    try:
        gridout_file = fs_wav.get( ObjectId(file_object_id) )
        return send_file(gridout_file, download_name= str(gridout_file.filename) or  'download.wav')
    except Exception as e:
        return e
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090)

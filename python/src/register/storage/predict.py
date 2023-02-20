from scipy.io import wavfile
from scipy.signal import resample
import numpy as np
from pymongo import MongoClient
import requests
import pymysql.cursors
import pymysql
import os, json,  gridfs
from bson import ObjectId

# mongodb
client = MongoClient(os.environ.get('MONGO_SVC_ADDRESS'))
db_wav = client.wav
# gridfs for mongodb
fs_wav = gridfs.GridFS(db_wav)

#mysql
# Connect to the database
def get_connection():
    return pymysql.connect(host= os.environ.get('MYSQL_HOST'),
                                #  user='user',
                                #  password='passwd',
                                database= os.environ.get('MYSQL_DB'),
                                port= int( os.environ.get('MYSQL_PORT') ),
                                cursorclass=pymysql.cursors.DictCursor)

#functions
def ensure_sample_rate(original_sample_rate, waveform,desired_sample_rate=16000):
    if original_sample_rate != desired_sample_rate:
        desired_length = int(round(float(len(waveform)) /
                                original_sample_rate * desired_sample_rate))
        waveform = resample(waveform, desired_length)
    return desired_sample_rate, waveform


def read_and_normalise(file):
    sample_rate, wav_data = wavfile.read(file, 'rb')
    wav_data = wav_data.mean( axis=1)
    sample_rate, wav_data = ensure_sample_rate(sample_rate, wav_data)
    wav_data = np.array(wav_data)
    waveform = wav_data /  wav_data.max()
    return waveform

def update_mysql(gridfs_object_id):
    #update the rows
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "UPDATE `file_list_24hr` SET `predicted`=1 WHERE `file_object_id` IN ('{}');".format(gridfs_object_id)
            cursor.execute(sql)
            connection.commit()
            # cursor deletes within context manager
        connection.close()
        return None
    except Exception as e:
        return e

def delete_mysql_mongodb(gridfs_object_id):
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "DELETE FROM `file_list_24hr` WHERE `file_object_id`IN ('{}');".format(gridfs_object_id)
            cursor.execute(sql)
            connection.commit()
            
        connection.close()
        fs_wav.delete(ObjectId(gridfs_object_id))
        return None
    except Exception as e:
        return e

def main(user_email=None):
    connection = get_connection()
    cursor = connection.cursor()
    # Read all records and predict each of them
    sql = "SELECT `user_email`, `file_object_id` ,`predicted` FROM `file_list_24hr`\
            WHERE `predicted` is NULL AND user_email= TRIM('{}');".format(user_email.strip() )
    countrows = cursor.execute(sql)
    # one = cursor.fetchone()
    all_rows = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()  # use context manager later # with keyworkd
    if all_rows:       
        for rowdict in all_rows:
            gridfs_object_id = rowdict['file_object_id']
            file = fs_wav.get( ObjectId(gridfs_object_id) )
            waveform = read_and_normalise(file)
            waveform = waveform.tolist()
            print(rowdict)
            # send request to serving
            url = 'http://snoring:8501/v1/models/snoring_or_not:predict'
            myobj = { "instances": waveform }
            results = requests.post(url, json = myobj)
            results = json.loads(results.text)['predictions']
            if results[0] > results[1]:
                e = update_mysql(gridfs_object_id)
                if e:
                    return e
            else:
                e = delete_mysql_mongodb(gridfs_object_id)
                if e:
                    return e
        return "{} predicted: as {} ".format(countrows, results[0] > results[1])
    return "No uploaded files were found in sql db."



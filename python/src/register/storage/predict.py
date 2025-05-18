from scipy.io import wavfile
from scipy.signal import resample
import numpy as np
from pymongo import MongoClient
import requests
import pymysql.cursors
import pymysql
import os, json, gridfs
from bson import ObjectId

# MongoDB setup
client = MongoClient(os.environ.get('MONGO_SVC_ADDRESS'))
db_wav = client.wav
fs_wav = gridfs.GridFS(db_wav)

# MySQL connection helper
def get_connection():
    try:
        return pymysql.connect(
            host=os.environ.get('MYSQL_HOST'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB'),
            port=int(os.environ.get('MYSQL_PORT')),
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        raise RuntimeError(f"Failed to connect to MySQL: {str(e)}")

# Helper function to ensure sample rate
def ensure_sample_rate(original_sample_rate, waveform, desired_sample_rate=16000):
    if original_sample_rate != desired_sample_rate:
        desired_length = int(round(len(waveform) / original_sample_rate * desired_sample_rate))
        waveform = resample(waveform, desired_length)
    return desired_sample_rate, waveform

# Helper function to read and normalize audio
def read_and_normalise(file):
    try:
        sample_rate, wav_data = wavfile.read(file, 'rb')
        wav_data = wav_data.mean(axis=1)  # Convert to mono
        sample_rate, wav_data = ensure_sample_rate(sample_rate, wav_data)
        wav_data = np.array(wav_data)
        waveform = wav_data / wav_data.max()
        return waveform
    except Exception as e:
        raise RuntimeError(f"Error reading and normalizing audio: {str(e)}")

# Update MySQL record
def update_mysql(gridfs_object_id):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                sql = "UPDATE `file_list_24hr` SET `predicted`=1 WHERE `file_object_id`=%s;"
                cursor.execute(sql, (gridfs_object_id,))
                connection.commit()
        return None
    except Exception as e:
        return f"Error updating MySQL: {str(e)}"

# Delete MySQL record and corresponding MongoDB file
def delete_mysql_mongodb(gridfs_object_id):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `file_list_24hr` WHERE `file_object_id`=%s;"
                cursor.execute(sql, (gridfs_object_id,))
                connection.commit()
        fs_wav.delete(ObjectId(gridfs_object_id))
        return None
    except Exception as e:
        return f"Error deleting MySQL/MongoDB record: {str(e)}"

# Main function to process predictions
def main(user_email=None):
    if not user_email:
        return "User email is required."

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                sql = """
                    SELECT `user_email`, `file_object_id`, `predicted`
                    FROM `file_list_24hr`
                    WHERE `predicted` IS NULL AND `user_email`=TRIM(%s);
                """
                countrows = cursor.execute(sql, (user_email.strip(),))
                all_rows = cursor.fetchall()

        if not all_rows:
            return "No uploaded files were found in the SQL database."

        for rowdict in all_rows:
            gridfs_object_id = rowdict['file_object_id']
            try:
                file = fs_wav.get(ObjectId(gridfs_object_id))
                waveform = read_and_normalise(file)
                waveform = waveform.tolist()

                # Send request to the prediction service
                url = 'http://snoring:8501/v1/models/snoring_or_not:predict'
                payload = {"instances": waveform}
                response = requests.post(url, json=payload)
                response.raise_for_status()
                results = json.loads(response.text)['predictions']

                if results[0] > results[1]:
                    error = update_mysql(gridfs_object_id)
                    if error:
                        return error
                else:
                    error = delete_mysql_mongodb(gridfs_object_id)
                    if error:
                        return error
            except Exception as e:
                return f"Error processing file {gridfs_object_id}: {str(e)}"

        return f"{countrows} files processed successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"
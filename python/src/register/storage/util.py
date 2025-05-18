import MySQLdb.cursors
from datetime import datetime, timezone, timedelta
from bson import ObjectId

def upload(fs_wav, fileObj, session, mysql):
    try:
        # Save the file to MongoDB GridFS
        fid = fs_wav.put(fileObj)
        if not fid:
            return "Failed to upload file to GridFS."

        # Fetch the user's email from the MySQL database
        with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute('SELECT email FROM accounts WHERE username = %s', (session['username'],))
            account = cursor.fetchone()

        if not account:
            return "Username not found."

        email = account['email']

        # Insert record into the `file_list_24hr` table
        with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
            try:
                cursor.execute(
                    '''
                    INSERT INTO file_list_24hr (id, user_email, start_date, end_date, file_object_id, predicted)
                    VALUES (NULL, %s, %s, %s, %s, %s)
                    ''',
                    (
                        email,
                        datetime.now(tz=timezone(timedelta(0), 'GMT')),
                        datetime.now(tz=timezone(timedelta(0), 'GMT')) + timedelta(hours=24),
                        str(fid),
                        None
                    )
                )
                mysql.connection.commit()
            except Exception as e:
                return f"Error inserting record into MySQL: {str(e)}"

        return fid, email
    except Exception as e:
        return f"An error occurred during upload: {str(e)}"

def download(fs_wav, session, mysql):
    try:
        # Fetch file object IDs for the user from the MySQL database
        with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute(
                'SELECT file_object_id FROM file_list_24hr WHERE user_email = %s AND predicted = 1',
                (session['email'],)
            )
            file_object_id_list = cursor.fetchall()

        if not file_object_id_list:
            return None

        # Retrieve files from MongoDB GridFS
        try:
            return [fs_wav.get(ObjectId(file_id_dict['file_object_id'])) for file_id_dict in file_object_id_list]
        except Exception as e:
            return f"Error retrieving files from GridFS: {str(e)}"
    except Exception as e:
        return f"An error occurred during download: {str(e)}"
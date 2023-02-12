import MySQLdb.cursors
from datetime import datetime, timezone , timedelta
from bson import ObjectId

def upload(fs_wav, fileObj, session, mysql) :
    fid = fs_wav.put(fileObj)
    if fid:
        # Insert record into the  file_list_24hr people
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT email FROM accounts WHERE username = % s ', (session['username'], ))
            account = cursor.fetchone()
           
            if account:
                email = account['email']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                try:
                    cursor.execute('INSERT INTO file_list_24hr ( id, user_email, start_date, end_date,  file_object_id, predicted \
                    )VALUES (NULL,% s, % s, % s, % s, % s)', (email
                    , datetime.now(tz=timezone(timedelta(0),'GMT'))
                    , datetime.now(tz=timezone(timedelta(0),'GMT')) + timedelta(hours=24)
                    , str(fid)
                    , None )
                    )
                    mysql.connection.commit()
                except Exception as e:
                    return e
                return fid , email #, "File uploaded successfully - {fileObj}"
            else:
                return 'Username not found'
        except Exception as e:
            return e
        
# def download(fs_wav, session, mysql) :
#     try:
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         c = cursor.execute('SELECT file_object_id FROM file_list_24hr WHERE user_email = % s AND predicted = 1', (session['email'] , ) )
#         file_object_id_list = cursor.fetchall()
#         cursor.close()
#         # return file_object_id_list
#         if c:
#             # return fs_wav.get(ObjectId( file_object_id_list['file_object_id']) )
#             return [ fs_wav.get(ObjectId(file_id_dict['file_object_id'])) for file_id_dict in file_object_id_list]
#         else:
#             return None
#     except Exception as e:
#         return e

        


    


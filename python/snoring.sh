# replicaset initiate config
rs.initiate( {_id: "rs0",members: [{ _id: 0,host: 'mongodb-0.mongodb:27017',},]} )

# MongoDB statefulset upload successful- first
[(ObjectId('63b9397ad0bd7c55e29968ab'), 'File uploaded successfully - {fileObj}')]

#Connection string without username, password that worked - first
  MONGO_SVC_ADDRESS: "mongodb://mongodb-0.mongodb:27017/wav?replicaSet=rs0"

# download k9s

# kubectl login to shell
kubectl exec --stdin --tty mysql-0 -- /bin/bash
kubectl exec --stdin --tty mongodb-0 -- /bin/bash

kubectl exec -it register-785b4567dd-xmxz2 -- sh
kubectl exec -it mysql-0 -- sh


kubectl exec --stdin --tty predict-598d9fd9f4-hww9k -- /bin/bash


# docker change to minikube cli
@FOR /f "tokens=*" %i IN ('minikube -p minikube docker-env --shell cmd') DO @%i
#powershell
& minikube -p minikube docker-env --shell powershell | Invoke-Expression



# mongodb replicaset initiate
rs.reconfig(
   {
      _id: "rs0",
      version: 1,
      members: [
         { _id: 0, host : "mongodb-0.mongodb:27017" }
      ]
   }
)

# curl request to tfserving
curl -d '{"instances": [1.0, 2.0, 5.0]}' -X POST http://snoring:8501/v1/models/snoring_or_not:predict
{"predictions": [4.97395563, 1.37558985]}


# mysql test

# Connect to the database
connection = pymysql.connect(host= "34.121.11.218",
                             database='test',
                             port = 3306,
							 user='bpoudel',
                             password='bpoudel',
                             cursorclass=pymysql.cursors.DictCursor)
							 
with connection.cursor() as cursor:
    # Read a single record
    sql = "SELECT * FROM accounts;"
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
    
							 

# Download test
file_object_id = "63e697e4504cb15d6f532168"
url = 'http://download:8090/download'
results = requests.get(url, params=  {'file_object_id':file_object_id},  stream=True)
with open( file_object_id+'.wav' , 'wb') as fd:
    for chunk in results.iter_content(chunk_size=128):
        fd.write(chunk)
        
        
# Project
docker tag   us-central1-docker.pkg.dev/turnkey-banner-371806/hello-repo
 
 
gcloud container clusters get-credentials snoring --region us-central1
 
client = pymongo.MongoClient("mongodb+srv://bpoudel:bpoudel@cluster0.m8xjg5h.mongodb.net/?retryWrites=true&w=majority")
db = client.wav

us-central1-docker.pkg.dev/turnkey-banner-371806/hello-repo

gcloud container clusters get-credentials snoring --region=us-central1


#mongurl parse

mongo_uri = "mongodb://username:" + urllib.parse.quote("p@ssword") + "@127.0.0.1:27001/"

#authorise and login to gke
gcloud container clusters get-credentials snoring --zone us-central1


cfg = rs.conf()
cfg.members[0].priority = 1
cfg.members[1].priority = 0.5
cfg.members[2].priority = 0.5
rs.reconfig(cfg)


# mongodb
client = MongoClient("mongodb://mongodb-0.mongodb:27017/wav?replicaSet=rs0")
db_wav = client.wav
# gridfs for mongodb
fs_wav = gridfs.GridFS(db_wav)


url = 'http://127.0.0.1:8080/download_file'
myobj = { "instances": out_file }
results = requests.get(url, data = myobj)


curl -X POST https://reqbin.com/echo/post/form -H "Content-Type: application/x-www-form-urlencoded" -d "username=bpoudel&password=bpoudel" 


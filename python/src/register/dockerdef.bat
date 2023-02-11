# download k9s


# kubectl login to shell
kubectl exec --stdin --tty mysql-0 -- /bin/bash
kubectl exec --stdin --tty mongodb-0 -- /bin/bash

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
connection = pymysql.connect(host= "mysql-0.mysql",
                             database='test',
                             port = 3306,
                             cursorclass=pymysql.cursors.DictCursor)
							 
with connection.cursor() as cursor:
    # Read a single record
    sql = "SELECT `user_email`, `file_object_id` ,`predicted` FROM `file_list_24hr` WHERE `predicted` is NULL;"
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
    
							 



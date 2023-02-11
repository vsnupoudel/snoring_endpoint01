# replicaset initiate config
rs.initiate( {_id: "rs0",members: [{ _id: 0,host: 'mongodb-0.mongodb:27017',},]} )

# MongoDB statefulset upload successful- first
[(ObjectId('63b9397ad0bd7c55e29968ab'), 'File uploaded successfully - {fileObj}')]

#Connection string without username, password that worked - first
  MONGO_SVC_ADDRESS: "mongodb://mongodb-0.mongodb:27017/wav?replicaSet=rs0"

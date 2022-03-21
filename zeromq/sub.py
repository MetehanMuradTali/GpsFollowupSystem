import pymongo
import zmq

client = pymongo.MongoClient()
mydb=client["mydb"]
mycol=mydb["Cars"]

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://127.0.0.1:2000')
socket.setsockopt_string(zmq.SUBSCRIBE,'')

while(True):
    message = socket.recv_pyobj()
    mycol.insert_one(message)
    print(message)
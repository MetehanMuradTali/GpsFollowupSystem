import zmq,csv
from time import sleep

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://127.0.0.1:2000')

last=0
with open ('last.txt') as f:
    lines = f.readlines()
    last=(int(lines[0]))
    f.close()

file  = open('C://Users//Acer//Desktop//yazlab2//1.0//zeromq//arabalar.csv', 'r')
type(file)
csvreader = csv.reader(file)
header=["Date","Nat","Lang","Id"]

x = 0
result = []
while(True):
    try:
        for row in csvreader:
            if (x < last):
                x += 1
            else:
                socket.send_pyobj(dict(zip(header, row)))
                x+=1
                print(x,last,row)
                sleep(0.2)
    except KeyboardInterrupt:
        with open ('last.txt','w') as f:
            f.write(str(x))
        f.close()
        exit(0)



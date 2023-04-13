import socket
from _thread import *

server = "10.68.67.68"
port = 5555
start = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
allready = 0
try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection, Server Started")
teams=["",""]
def threaded_client(conn,id):
    global allready, teams
    conn.send(str.encode("Connected"+str(id)))
    reply=""
    lock = False
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
            else:
                print(("Recieved: " + reply))
                if reply == "ready":
                    if start:
                        conn.send(str.encode("start"))
                    else:
                        conn.send(str.encode("wait"))
                if reply == "Ready":
                    if allready == 2:
                        conn.send(str.encode("fight"))
                    else:
                        if not lock:
                            allready+=1
                            lock = True
                        else:
                            pass
                        conn.send(str.encode("wait"))
                if reply[0] == "£":
                    teams[id] = reply
                    print(teams)
                    if id == 0:
                        conn.send(str.encode(teams[1]))
                        print("sent to player " + str(id+1))
                    else:
                        conn.send(str.encode(teams[0]))
                        print("sent to player " + str(id+1))
                    allready = 0
                    lock = False





        except:
            break
    print("Lost connection")
    conn.close()
i=0
while True:
    conn, addr = s.accept()
    print("connected to: ", addr)
    print(i)
    start_new_thread(threaded_client, (conn,i))
    i+=1
    if i == 2:
        start = True
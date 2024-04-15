import socket
import threading
from auth import *
import time

#IP = socket.gethostbyname(socket.gethostname())
IP = "192.168.1.38"
PORT = 4003
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "quit"
nb_clients = 0
firstconnectionlist = []
clientposes = []
pseudos = []
chats = []

def handle_client(conn, addr):
    global chats
    newclient = 0
    last_pseudosend = 0
    connected = True
    clientname = ""
    chatmsgsent = 0
    chatactualize = 0
    while connected:
        
        msg = conn.recv(SIZE).decode(FORMAT)
        #print(msg)
        if len(chats)>6:
            chats.pop(0)
        if msg == "quit":
            
            print(str(clientname) +" left the game")
            index = 0
            for clientpos in clientposes:
                if clientpos[0] == addr[1]:
                    del clientposes[index]
                index += 1
            index = 0
            for pseudo in pseudos:
                if pseudo[1] == addr[1]:
                    del pseudo
                index += 1
            
            connected = False
        if msg != "":
            if str(msg)[0] == "p":
                if not [msg.replace("p",""),addr[1]] in pseudos:
                    pseudos.append([msg.replace("p",""),addr[1]])
                    clientname = (msg.replace("p",""))
                    print(f"{clientname} joined the game.")
                    createclientdata(clientname)
                
                newclient = 1
            
            if str(msg) == "!chat?":
                conn.send(bytes("a"+str(chats),"utf-8"))
                chatmsgsent = 1
            if str(msg)[0] == "a":
                
                    
                chats.append(str(clientname)+" : "+str(msg)[1:])
                
            
            if str(msg)[0] == "c":
                
                #print(f"[{addr}] {msg}")
                msg = msg.replace("c","")
                
                if [addr[1],msg] in clientposes:
                    pass
                else:
                    index = 0
                    dontadd = 0
                    for clientpos in clientposes:
                        if clientpos[0] == addr[1]:
                            clientposes[index] =[addr[1],str(msg)]
                            
                            dontadd = 1
                        index += 1
                    if dontadd == 0:
                        clientposes.append([addr[1],str(msg)])
                
                if addr[1] in firstconnectionlist:
                    if chatmsgsent == 0:
                        if newclient==1:
                            
                            conn.send(bytes("pseudos"+str(pseudos),"utf-8"))
                            newclient = 0
                        else:
                            conn.send(bytes(str(clientposes),"utf-8"))
                            firstconnectionlist.append(addr[1])
                    else:
                        chatmsgsent = 0
                else:
                    
                    conn.send(bytes("first"+str(addr[1]),"utf-8"))
                    firstconnectionlist.append(addr[1])
                    
            if str(msg)[0] == "l":
                success = handle_authentication("login", msg)
                conn.send(bytes(success,"utf-8"))
            if str(msg)[0] == "r":
                success = handle_authentication("register", msg)        
                conn.send(bytes(success,"utf-8"))

    conn.close()

def main():
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
        
        
        nb_clients = threading.active_count() - 1
        
        
if __name__ == "__main__":
    main()

    
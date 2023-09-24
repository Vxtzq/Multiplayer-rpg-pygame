import socket
import threading
from auth import *


#IP = socket.gethostbyname(socket.gethostname())
IP = "localhost"
PORT = 4003
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
nb_clients = 0
firstconnectionlist = []
clientposes = []
pseudos = []


def handle_client(conn, addr):
    #print(f"[NEW CONNECTION] {addr} connected.")
    newclient = 0
    last_pseudosend = 0
    connected = True
    while connected:
        
        msg = conn.recv(SIZE).decode(FORMAT)
        #print(msg)
        if msg == "quit":
            connected = False
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
            print(pseudos)
        if msg != "":
            if str(msg)[0] == "p":
                if not [msg.replace("p",""),addr[1]] in pseudos:
                    pseudos.append([msg.replace("p",""),addr[1]])
                print(pseudos)
                newclient = 1
            
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
                            #print(clientposes)
                            dontadd = 1
                        index += 1
                    if dontadd == 0:
                        clientposes.append([addr[1],str(msg)])
                
                if addr[1] in firstconnectionlist:
                    if newclient==1:
                        
                        conn.send(bytes("pseudos"+str(pseudos),"utf-8"))
                        newclient = 0
                    else:
                        conn.send(bytes(str(clientposes),"utf-8"))
                        firstconnectionlist.append(addr[1])
                else:
                    #print("sus")
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
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("server is listening")
    #print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        #print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        
        
        nb_clients = threading.active_count() - 1
        #print(nb_clients)
        
if __name__ == "__main__":
    main()

    
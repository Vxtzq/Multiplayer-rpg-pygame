import os

def handle_authentication(authtype, msg):
    f = open("users.txt", 'a+')
    f.close()    
    
    if authtype == "register":
        f = open("users.txt", 'r')
        valid = 1
        for line in f:
            
            if line.split(',')[0] == msg.replace("r,","").split(',')[0]:
                valid = 0
        f.close()
        if valid == 1:
            f = open("users.txt", 'a+')
            f.write(msg.replace("r,","")+"\n")
            f.close()
            return "registervalid"
        else:
            f.close()
            return "registerinvalid"
    if authtype == "login":
        f = open("users.txt", 'r')
        valid = 0
        for line in f:
            
            if line == msg.replace("l,","")+"\n":
                valid = 1
        f.close()
        if valid == 1:
            return "loginvalid"
        else:
            return "logininvalid"

def createclientdata(usr):
    print("creating data")
    if os.path.exists("playersaves/"+str(usr)+".txt"):
        pass
    else:
        f = open("playersaves/"+str(usr)+".txt", 'w')
        f.close()

def handle_authentication(authtype, msg):
    f = open("users.txt", 'a+')
    f.close()    
    
    if authtype == "register":
        f = open("users.txt", 'r')
        valid = 1
        for line in f:
            print(line)
            if line == msg.replace("r,","")+"\n":
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
            print(line)
            print(msg.replace("l,",""))
            if line == msg.replace("l,","")+"\n":
                valid = 1
        f.close()
        if valid == 1:
            return "loginvalid"
        else:
            return "logininvalid"

    

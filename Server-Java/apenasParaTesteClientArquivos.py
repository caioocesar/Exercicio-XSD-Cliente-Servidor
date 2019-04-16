# TCP Client Code

host="127.0.0.1"            # Set the server address to variable host

port=4446               # Sets the variable port to 4444

from socket import *             # Imports socket module

s=socket(AF_INET, SOCK_STREAM)      # Creates a socket

s.connect((host,port))          # Connect to server address

#msg=s.recv(1024)            # Receives data upto 1024 bytes and stores in variables msg

ctrl = input("começar a enviar?")
while(ctrl == ''):
    f = open('./arquivos/12345.xml','rb')
    l = f.read(8192)
    while (l):
        s.send(l)
        l = f.read(8192)
    print("leu")
    f.close()
    
    print(str(s.recv(8192)))
    ctrl = input("proximo envio?")
    

#s.send(bytes("out", 'utf-8'))
s.close()                            # Closes the socket 
# End of code

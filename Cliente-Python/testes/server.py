import time
from lxml import etree
from sys import exit
from socket import *
from threading import *
import time

TESTE = True

###########
host = "127.0.0.1"
port = 4446
###########

lock = Lock()

xml_arq = open("historico.xml", "r+")

xml_doc = etree.parse(xml_arq)


class MySocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            return True
        except Exception as e:
            print("Falha na tentativa de conexção:" + str(e))
            return False

    def bind(self, host, port):
        try:
            self.sock.bind((host, port))
        except Exception as e:
            print(str(e))

    def listen(self, times):
        self.sock.listen(times)

    def accept(self):
        return self.sock.accept()

    def mysend(self, msg):
        totalsent = 0
        #cod = msg.encode('utf-8')
        cod = msg

        MSGLEN = len(cod)
        while totalsent < MSGLEN:
            sent = self.sock.send(cod[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        MSGLEN = 1024
        while bytes_recd < MSGLEN:
            print(bytes_recd)
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")

            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

        return b''.join(chunks)

    def receive(self):
        data = self.sock.recv(2048)
        return data.decode('utf-8')

'''
class myThread(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        global item
        global on
        print("Iniciando thread " + self.name)
        while on:
            pass
'''

serverSocket = MySocket()

serverSocket.bind(host, port)

serverSocket.listen(1)

sock, adds = serverSocket.accept()

print("conexao aceita com :" + adds[0])

sClientSocket = MySocket(sock)

msg = sClientSocket.receive()

print("Mensagem recebida:\n" + msg)

time.sleep(0.5)

data_send = etree.tostring(xml_doc)

print("Enviando:\n" + str(data_send))

sClientSocket.mysend(data_send)

print("Programa acaba")

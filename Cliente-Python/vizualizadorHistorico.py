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

on = True

class MySocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket(AF_INET, SOCK_STREAM)
            if TESTE:
                pass
        else:
            self.sock = sock
        print("Socket iniciado")

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            return True

        except Exception as e:
            return False


    def mysend(self, msg):
        ''' Método para envio de mensagens'''
        totalsent = 0
        #cod = msg.encode('utf-8')
        cod = msg

        MSGLEN = len(cod)
        while totalsent < MSGLEN:
            sent = self.sock.send(cod[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

        if TESTE:
            print("mensagem :\"" + str(msg) + "\" enviada com sucesso")

    def receive(self):
        ''' Ignorar esse método'''
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

    def myreceive(self):
        data = self.sock.recv(2048)
        return data.decode('utf-8')

    def tryConnection(self, host, port):
        ''' Método que tenta conectar com o host'''
        while True:
            if self.connect(host, port):
                self.echo("Conectado ao host")
                self.rcvThread = myThread('rcv', self.sock)
                self.rcvThread.start()
                break

            else:
                self.echo("Falha na conexao, tente novamente")
                time.sleep(0.5)
                self.tryConnection(host, port)

    def echo(self, msg):
        ''' Só foi criado para ter que dar um [Enter] toda vez que uma mensagem for exibida, questões de teste'''
        print(msg)
        input()


class myThread(Thread):
    def __init__(self, name, sock):
        super().__init__()
        self.name = name
        self.socket = MySocket(sock)

    def run(self):
        global on
        global received_msg

        if TESTE:
            print("Iniciando thread " + self.name)

        while on:
            received_msg = self.socket.myreceive()
            if not received_msg:
                exit(0)

def run():
    ''' Abrindo o arquivo xsd '''
    xsd_arq = open("arquivo.xsd", "r+")

    ''' Transformando o arquivo aberto em arvore de elementos '''
    xsd_doc = etree.parse(xsd_arq)

    ''' Método da biblioteca que Guarda que o arquivo lido é um XML Schema que vai ser usado para validação '''
    xsd = etree.XMLSchema(xsd_doc)

    xml_arq = open("arquivo.xml", "r+")

    xml_doc = etree.parse(xml_arq)

    if xsd.validate(xml_doc) is True:
        print('True')
    else:
        print('False')


    clientSocket = MySocket()

    clientSocket.tryConnection(host, port)

    dataSend = etree.tostring(xml_doc)
    clientSocket.mysend(dataSend)

run()
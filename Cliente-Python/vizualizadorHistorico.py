import locale
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
received_msg = ''
lock = Lock()

print(locale.getpreferredencoding(False))

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
        data = self.sock.recv(4096)
        return data.decode('utf-8')

    def tryConnection(self, host, port):
        ''' Método que tenta conectar com o host'''
        while True:
            if self.connect(host, port):
                if TESTE:
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
            msg = self.socket.myreceive()
            with lock:
                received_msg = str(msg)
            if not received_msg:
                exit(0)

def run():

    global received_msg

    waiting_HE = False

    xsd = carregarXSD("he_schema.xsd")

    clientSocket = MySocket()

    clientSocket.tryConnection(host, port)

    while True:
        ans = input("1 - Acessar histórico\n 2 - Sair do programa")

        if ans == '1':
            data_send = etree.tostring(carregarXML("getHistorico.xml"))

            clientSocket.mysend(data_send)

            waiting_HE = True

            break

        elif ans == '2':
            break

        else:
            print("Entrada inválida")

    while waiting_HE:

        with lock:
            if received_msg != '':

                if TESTE:
                    print("Olha: " + received_msg)

                if validate(received_msg, xsd):
                    imprimir(received_msg)
                else:

                    print("Algo de errado não está certo, XML não corresponde ao Schema")


                received_msg = ''
                waiting_HE = False


def carregarXML(nome_arq):
    # Abrindo o arquivo xml
    xsd_arq = open(nome_arq, "r+")

    # Transformando o arquivo aberto em arvore de elementos
    return etree.parse(xsd_arq)

def validate(msg, xsd):

    #xml_doc = etree.parse(msg)
    xml_doc = etree.fromstring(msg)

    return xsd.validate(xml_doc)

def carregarXSD(nome_arq):
    # Abrindo o arquivo xsd
    xsd_arq = open(nome_arq, "r+")

    # Transformando o arquivo aberto em arvore de elementos
    xsd_doc = etree.parse(xsd_arq)

    # Método da biblioteca que Guarda que o arquivo lido é um XML Schema que vai ser usado para validação
    return etree.XMLSchema(xsd_doc)

def imprimir(XMLdoHistorico):  # passar nome do arquivo xml ja salvo em memoria!! Nao adianta passar string e tentar usar fromstring ou fazer aqui o arquivo

    #xml_arq = etree.parse(XMLdoHistorico)
    xml_arq = etree.fromstring(XMLdoHistorico)
    xml = xml_arq.getroot()

    print("------------------------------------------------------------------------")
    print(xml[0][0].text)
    print(xml[0][1].text)
    print("Curso: " + xml[1].text)
    print("Aluno: " + xml[2].text)
    print("Matricula: " + xml[3].text)
    print("Cr medio: " + xml[4].text)
    print("Data geracao: " + xml[5].text)
    print("Hora geracao: " + xml[6].text)
    print("Cod autenticacao: " + xml[7].text)
    print("------------------------------------------------------------------------")
    print("\n")
    listaPeriodos = xml[8].findall('Periodo')
    for i in range(len(listaPeriodos)):
        print("Ano Semestre: " + listaPeriodos[i][0].text)
        print("Creditos solicitados: " + listaPeriodos[i][1].text)
        print("Creditos acumulados: " + listaPeriodos[i][2].text)
        print("Creditos obtidos: " + listaPeriodos[i][3].text)
        print("Cr periodo: " + listaPeriodos[i][4].text)
        print("\n")

        listaDisciplinasAA = listaPeriodos[i][5].findall('AtividadeAcademica')
        for j in range(len(listaDisciplinasAA)):
            print("\tCodigo disciplina: " + listaDisciplinasAA[j][0].text)
            print("\tNome disciplina: " + listaDisciplinasAA[j][1].text)
            print("\tCreditos: " + listaDisciplinasAA[j][2].text)
            print("\tNota: " + listaDisciplinasAA[j][3].text)
            print("\tSituacao: " + listaDisciplinasAA[j][4].text)
            print("\n")

        listaDisciplinas = listaPeriodos[i][5].findall('Disciplina')
        for j in range(len(listaDisciplinas)):
            print("\tCodigo disciplina: " + listaDisciplinas[j][0].text)
            print("\tNome disciplina: " + listaDisciplinas[j][1].text)
            print("\tCreditos: " + listaDisciplinas[j][2].text)
            print("\tNota: " + listaDisciplinas[j][3].text)
            print("\tSituacao: " + listaDisciplinas[j][4].text)
            print("\n")

        print("------------------------------------------------------------------------")

run()
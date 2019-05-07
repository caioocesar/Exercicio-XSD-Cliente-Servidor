#!/usr/bin/python3.6
import locale
from io import StringIO

from lxml import etree

from sys import exit
from socket import *
from threading import *
import time
import os

TESTE = False

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
        data = self.sock.recv(8192)
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

def imprimir(XMLdoHistorico): #parametro: string
    
    #xml_arq = open(XMLdoHistorico, "r",-1,"utf-8")
    xml_arq = etree.parse(StringIO(XMLdoHistorico))
    xml = xml_arq.getroot()
    
    print("------------------------------------------------------------------------")
    print(xml.find('universidade').find('nome').text)
    print(xml.find('universidade').find('abreviacao').text)
    print("Curso: "+xml.find('curso').text)
    print("Aluno: "+xml.find('aluno').text)
    print("Matricula: "+xml.find('matricula').text)
    print("Cr medio: "+xml.find('crMedio').text)
    print("Data geracao: "+xml.find('dataGeracao').text)
    print("Hora geracao: "+xml.find('horaGeracao').text)
    print("Cod autenticacao: "+xml.find('codigoAutenticacao').text)
    print("------------------------------------------------------------------------")
    print("\n")
    listaPeriodos = xml.find('periodos').findall('Periodo')
    for i in range(len(listaPeriodos)):
        print("Ano Semestre: "+listaPeriodos[i].find('anoSemestre').text)
        print("Creditos solicitados: "+listaPeriodos[i].find('creditosSolicitados').text)
        print("Creditos acumulados: "+listaPeriodos[i].find('creditosAcumulados').text)
        print("Creditos obtidos: "+listaPeriodos[i].find('creditosObtidos').text)
        print("Cr periodo: "+listaPeriodos[i].find('crPeriodo').text)
        print("\n")
        
        listaDisciplinasAA = listaPeriodos[i].find('disciplinas').findall('AtividadeAcademica')
        for j in range(len(listaDisciplinasAA)):
            print("\tCodigo disciplina: "+listaDisciplinasAA[j].find('codigo').text)
            print("\tNome disciplina: "+listaDisciplinasAA[j].find('nome').text)
            print("\tCreditos: "+listaDisciplinasAA[j].find('creditos').text)
            print("\tNota: "+listaDisciplinasAA[j].find('nota').text)
            print("\tSituacao: "+listaDisciplinasAA[j].find('situacaoAA').text)
            print("\n")
            
        listaDisciplinas = listaPeriodos[i].find('disciplinas').findall('Disciplina')
        for j in range(len(listaDisciplinas)):
            print("\tCodigo disciplina: "+listaDisciplinas[j].find('codigo').text)
            print("\tNome disciplina: "+listaDisciplinas[j].find('nome').text)
            print("\tCreditos: "+listaDisciplinas[j].find('creditos').text)
            print("\tNota: "+listaDisciplinas[j].find('nota').text)
            print("\tSituacao: "+listaDisciplinas[j].find('situacao').text)
            print("\n")
            
        print("------------------------------------------------------------------------")


def geraHtml(XMLdoHistorico): #parametro: string
    
    #xml_arq = open(XMLdoHistorico, "r",-1,"utf-8")
    xml_arq = etree.parse(StringIO(XMLdoHistorico))
    xml = xml_arq.getroot()
    texto = []
    name = "historico"
    name = name + '.html'
    arq = open(name, 'w',-1,"utf-8")

    print('Gerando',name,'...\n')

    
    texto.append("<!DOCTYPE html>\n<html lang='pt-BR'>\n\n<html>\n\n")
    texto.append("\t<head>\n\t\t<title>Histórico</title>\n\t\t<meta charset = 'utf-8'>\n\t\t<link rel=\"stylesheet\" type=\"text/css\" href=\"styles.css\">\n"+"\t\t<link rel=\"shortcut icon\" href=\"ufrrj.jpg\" type=\"image/jpg\"/>\n\t</head>\n")
    texto.append("\n\t<body>\n")
    texto.append("\n\t\t<header>\n")
    texto.append("\t\t<a href=\"http://portal.ufrrj.br\" title=\"UFRRJ\"><img src=\"ufrrj.jpg\" class = \"imagem\" align = \"left\" alt=\"Falha na imagem\"></a>\n")
    texto.append("\t\t<h1><br>"+xml.find('universidade').find('nome').text+"</h1>\n")
    texto.append("\t\t<h1>"+xml.find('universidade').find('abreviacao').text+"</h1><br><br>\n")
    texto.append("\t\t</header>\n\n")
    texto.append("\n\t\t<div>\n")
    texto.append("\t\t<img src=\"perfil.jpg\" class = \"imagemPerfil\" align = \"left\" title=\"Perfil\" alt=\"Falha na imagem\"><br>Curso: "+xml.find('curso').text+"<br>\n")
    texto.append("\t\tAluno: "+xml.find('aluno').text+"<br>\n")
    texto.append("\t\tMatrícula: "+xml.find('matricula').text+"<br>\n")
    texto.append("\t\tCR médio: "+xml.find('crMedio').text+"<br>\n")
    texto.append("\t\tData geração: "+xml.find('dataGeracao').text+"<br>\n")
    texto.append("\t\tHora geração: "+xml.find('horaGeracao').text+"<br>\n")
    texto.append("\t\tCód. autenticação: "+xml.find('codigoAutenticacao').text+"<br><br>\n")
    texto.append("\t\t</div>\n")


    texto.append("\n\t\t<section>\n")
    listaPeriodos = xml.find('periodos').findall('Periodo')
    texto.append("\t\t\t<img src=\"legenda.png\" class = \"imagemLegenda\" align = \"right\" title=\"legenda\" alt=\"Falha na imagem\">\n")
    for i in range(len(listaPeriodos)):
        texto.append("\t\t\t<br><br><table>\n")#\n\t\t\t<tr><th>Ano Semestre</th><th>Creditos solicitados</th><th>Creditos acumulados</th><th>Creditos obtidos</th><th>Cr periodo</th></tr><br>\n")
        texto.append("\t\t\t<tr><th>"+listaPeriodos[i].find('anoSemestre').text+"</th></tr>\n")
        
        texto.append("\t\t\t\t<tr><th>Código disciplina</th>"+"<th>Nome disciplina</th>"+"<th>Créditos</th>"+"<th>Nota</th>"+"<th>Situação</th></tr>\n")
        
        listaDisciplinasAA = listaPeriodos[i].find('disciplinas').findall('AtividadeAcademica')
        for j in range(len(listaDisciplinasAA)):
            texto.append("\t\t\t\t<tr><td>"+listaDisciplinasAA[j].find('codigo').text+"</td>\n")
            texto.append("\t\t\t\t<td>"+listaDisciplinasAA[j].find('nome').text+"</td>\n")
            texto.append("\t\t\t\t<td>"+listaDisciplinasAA[j].find('creditos').text+"</td>\n")
            texto.append("\t\t\t\t<td>"+listaDisciplinasAA[j].find('nota').text+"</td>\n")
            texto.append("\t\t\t\t<td>"+listaDisciplinasAA[j].find('situacaoAA').text+"</td></tr>\n\n")

            
        listaDisciplinas = listaPeriodos[i].find('disciplinas').findall('Disciplina')
        for j in range(len(listaDisciplinas)):
            texto.append("\t\t\t\t<tr><td>"+listaDisciplinas[j].find('codigo').text+"</td>\n")
            texto.append("\t\t\t\t<td>"+listaDisciplinas[j].find('nome').text+"</td>\n")
            texto.append("\t\t\t\t<td>"+listaDisciplinas[j].find('creditos').text+"</td>\n")
            texto.append("\t\t\t\t<td>"+listaDisciplinas[j].find('nota').text+"</td>\n")
            texto.append("\t\t\t\t<td>"+listaDisciplinas[j].find('situacao').text+"</td></tr>\n\n")

        texto.append("\t\t\t</tr><td></td><td>Créditos solicitados: "+listaPeriodos[i].find('creditosSolicitados').text+"</td>\n")
        texto.append("\t\t\t<td>Créditos acumulados: "+listaPeriodos[i].find('creditosAcumulados').text+"</td>\n")
        texto.append("\t\t\t<td>Créditos obtidos: "+listaPeriodos[i].find('creditosObtidos').text+"</td>\n")
        texto.append("\t\t\t<td>CR período: "+listaPeriodos[i].find('crPeriodo').text+"</td></tr>\n\n")
        texto.append("\t\t\t</table>\n\n")

    texto.append("\n\t\t</section>\n")
    texto.append("\n\t\t<footer>\n")
    texto.append("\t\t\t<br>Grupinho de TEDB, 2019.")
    texto.append("\n\t\t</footer>\n")
    texto.append("\t</body>\n")
    texto.append("\n</html>")

            


    arq.writelines(texto)

    print(name,"gerado com sucesso.\nSalvo em:", os.path.abspath(name))

    arq.close()

    flag = False

    while(flag == False):

    	option = input("\nDeseja abrir o histórico gerado? (S / N)\n")

    	if(option == 's' or option == 'S' or option == 'sim' or option == 'yes' or option == 'y'):
    		os.startfile(os.path.abspath(name))
    		flag = True

    	elif(option == 'n' or option == 'N' or option == 'nao' or option == 'not' or option == 'no'):
    		flag = True

    	if(flag == False):
    		print("Opção inválida. Tente novamente...")

    print("Visualização encerrada.")

run()

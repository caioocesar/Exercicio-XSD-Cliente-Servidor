# Exercício XSD Cliente Servidor

Trabalho feito para a disciplina de "Tópicos Especiais em Banco de Dados". Objetivo é implementar um Servidor de uma universidade e executar uma determinada tarefa quando algum Cliente realiza uma requisição que envia um arquivo xml que contém o nome do método a ser executado no Servidor e seus parâmetros.
Aqui, só será realizada a implementação do método de obter um histórico escolar dado uma matrícula.

O Cliente terá o XML Schema(XSD) de um histórico escolar, para que possa interpretar o que receberá do Servidor como resposta a sua requisição.
O Servidor terá um conjunto de arquivos XML de históricos escolares, onde o mesmo fará uma busca pela matrícula por este conjunto para encontrar o histórico escolar correspondente, e depois envia o correspondente ao cliente. Além disso, o Servidor terá o XSD da requisição do método, o qual o cliente irá enviar para solicitar um histórico escolar.

Cliente - Escrito em Python

Servidor - Escrito em Java

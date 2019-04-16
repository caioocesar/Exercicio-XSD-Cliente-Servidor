# Parte referente ao servidor em java

- Para executar o servidor entre nesta pasta e execute o comando: ./run-server.hs
- em seguida execute o cliente


# Detalhes do desenvolvimento

O método "handleClientRequestMessage" é apenas para um teste mais simplificado com mensagens
textuais ao invés de arquivos.

# Possíveis problemas conhecidos

1) se o arquivo for maior que 8192 bytes ele vai ignorar

solved:
1) os arquivos que ele recebe e grava, por algum motivo, estão vazios qnd eu abro eles por algum editor de texto
    - ele rodava mais uma vez a criação do arquivo antes de ficar preso no read, então quando ele dava a exception para
    finalizar a thread de resposta do cliente o arquivo estava apagado. Agora a criação do arquivo só ocorre depois que a
    leitura dos dados do socket acontece, desta forma enquanto nada for lido o arquivo da ultima requisição não será sobrescrito
2) por algum motivo ta sendo adicionado um b' no inicio e um ' no final do arquivo (pode ser a forma que eu imprimo no python
    - realmente era um problema da imressão no python ele estava marcando que o arquivo enviado era um binário
3) qnd termina ele lança um index out of bounds exception
    - o problema vinha do momento que o cliente cancelava a conexão e o read do serv era liberado com a quantidade de bytes -1.
    isso fazia um index out of bounds na hora de converter os bytes para string, então usei isso como condição de parada para
    a thread que atende o cliente.
4) absolute path hardcoded
    - a pasta na raiz resolveu o problema, porque assim o './' funciona
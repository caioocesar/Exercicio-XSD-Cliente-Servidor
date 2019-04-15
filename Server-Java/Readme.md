# Parte referente ao servidor em java

Ao pegar este código, o primeiro passo é se certificar de alterar a váriavel "absolutePath" 
com o diretório absoluto de onde você irá guardar e buscar os arquivos que precisar.

O método "handleClientRequestMessage" é apenas para um texte mais simplificado com mensagens 
simples ao invés de arquivos.

Usar o código em python para teste, também é preciso definir o caminho absoluto.

# Possíveis problemas conhecidos

1) se o arquivo for maior que 4096 bytes ele vai ignorar
2) por algum motivo ta sendo adicionado um b' no inicio e um ' no final do arquivo (pode ser a forma que eu imprimo no python
3) qnd termina ele lança um index out of bounds exception
4) absolute path hardcoded

solved:
1) os arquivos que ele recebe e grava, por algum motivo, estão vazios qnd eu abro eles por algum editor de texto
  - ele rodava mais uma vez a criação do arquivo antes de ficar preso no read, então quando ele dava a exception para 
  finalizar a thread de resposta do cliente o arquivo estava apagado. Agora a criação do arquivo só ocorre depois que a 
  leitura dos dados do socket acontece, desta forma enquanto nada for lido o arquivo da ultima requisição não será sobrescrito

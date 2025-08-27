Análise de Dados COVID-19 por Cidade no Brasil

Sobre o Projeto



Este projeto tem como objetivo analisar os dados de COVID-19 em cidades brasileiras, utilizando Python para manipulação de dados, MySQL para armazenamento e consulta, e bibliotecas como Matplotlib e Seaborn para visualização dos resultados.



O que o script faz?



Leitura e limpeza dos dados

O script carrega o arquivo caso\_full.csv.gz, realiza a limpeza e ajustes necessários para garantir que os dados estejam prontos para análise.



Armazenamento no banco de dados MySQL

Os dados limpos são inseridos na tabela covid\_city do banco MySQL. Para melhorar o desempenho e evitar problemas, a inserção é feita em blocos.



Geração de relatórios e gráficos

O script cria relatórios com:



Total de mortes por cidade.



População estimada antes e depois dos casos confirmados por cidade.



Cidade com maior número de casos.



Cidade com menor número de casos (com pelo menos um caso).



Além disso, gera gráficos que ilustram essas informações de forma visual.



Arquivos do projeto



covid.py: Script principal para processamento dos dados, inserção no banco e geração de relatórios e gráficos.



caso\_full.csv.gz: Arquivo compactado contendo os dados brutos da COVID-19 por cidade.



README.txt: Este arquivo com as instruções e informações sobre o projeto.



relatorio.pdf: Documento PDF com imagens dos gráficos e tabelas geradas.



Requisitos



Antes de rodar o projeto, certifique-se de ter instalado:



Python 3.13



MySQL Server



Bibliotecas Python necessárias, que podem ser instaladas com:



pip install pandas sqlalchemy mysql-connector-python matplotlib seaborn



Como executar



Verifique se o MySQL está ativo e crie o banco de dados com o comando:



CREATE DATABASE covid\_db;





Configure os dados de conexão no arquivo covid.py, alterando as variáveis:



usuario = 'root'

senha = 'root'

host = 'localhost'

banco = 'covid\_db'





Execute o script com:



python covid.py





O script irá:



Limpar a tabela covid\_city, se ela já existir.



Inserir os dados do arquivo CSV no banco de dados em blocos.



Gerar e exibir relatórios e gráficos.



Resultados esperados



Gráfico mostrando as 10 cidades com mais mortes por COVID-19.



Gráfico comparando a população antes e depois dos casos para as 10 maiores cidades.



Relatórios com as cidades que têm o maior e menor número de casos.



Impressão dos relatórios no terminal.



Observações



Para montar o relatório final em PDF, capture imagens (prints) dos gráficos e tabelas exibidos pelo script.



Envie o PDF junto com o link para o repositório do projeto na entrega.


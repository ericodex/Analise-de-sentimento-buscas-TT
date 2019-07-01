# Desenvolvido por Eric Oliveira Lima - @ericodigos - 2019-06-26
# 
# Sistema que usa a API do twitter com configuração legal para extração de dados de acordo 
# com uma chave de busca dentro do código, utiliza o biblioteca vaderSentiment salvando em TXT 
# informações sobre a análise.

# Dependências
import regex, re
import pandas as pd
import tweepy # http://docs.tweepy.org/en/v3.7.0/api.html
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os.path
from pathlib import Path
import time
import numpy as np

linguagem =  'pt' # De acordo com o ISO 639-1 code
query_search_string = 'eric'

# Variáves de identificação da API do Twitter
consumer_key = '3QwXMb6vVf0ntv'
consumer_secret = '8OqhQAYs2AKR5wTXMYqJUTi4VVeSv2yglI0'
access_token = '20087738-bldoRF9Mntpwe2JXGIbzHxirP6PWFYRA8'

def tempo_log():
    ''' Retorna tempo para informações de log'''
    return str(time.strftime("%Y/%m/%d %H:%M:%S -->",time.localtime()))
    
def novo_nome_arquivo_log():
    ''' Retorna nome com data para arquivo de informações '''
    return str(time.strftime("%Y%m%d %H %M log_vaderSentiment_twitter",time.localtime()))

# Diretório para salvar informações da raspagem. (troque o '\' por '/' para as URL de diretórios do windows.)
diretorio = Path('C:/Users/Eric/Anaconda3/envs/analise_de_sentimento_twitter/sistema/retorno_respostas')

# Criar arquivo log de atividade do sistema.
novo_arquivo_estrutura = os.path.join(diretorio, novo_nome_arquivo_log() + '.txt')
arquivo = open(novo_arquivo_estrutura,"w")

arquivo.write('Inicio de extração de sentimentos do twitter' + str(time.strftime("%Y/%m/%d %H:%M:%S",time.localtime()))+ '\n')

# Autentico com o Twitter
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

# Definindo função de limpeza de dados
def limparTweet(tweet):
    ''' Função utilitária, limpa o texto de um tweet removendo caracteres especiais e links utilizando regex '''
    return ' '.join(re.sub('(@[A-ZÇÃá@ãçâÂa-z0-9]+)|([^0-9@ÇÃáãçâÂA-Za-z \t])|(\w+:\/\/\S+)'," ",
    tweet).split())

# - Encontro tweets relacionados com a chave - Limitado a 100 por evento
tweets = api.search(query_search_string,lang=linguagem,rpp=1000)

# Crio e limpo dataframe com pandas
data = pd.DataFrame(data=[limparTweet(tweet.text) for tweet in tweets],columns=['Tweets'])

#nltk.download('vader_lexicon')

# Percorre tweets analisando sentimentos de 0 a 1 em positivo, neutro e negativo.
sid = SentimentIntensityAnalyzer()

list = []
for index, row in data.iterrows():
  ss = sid.polarity_scores(row['Tweets'])
  list.append(ss)
se = pd.Series(list)
data['polarity'] = se.values

arquivo.write('-- Todos os erros são responsabilidades de @ericódigos\n')

# Lista e Classifica os sentimentos no twitter em ordem decrescente com sentimento negativo
lista = []
ind = 0
for e in data.polarity:
  ind += 1
  lista.append([ind,e["neg"],e["pos"],e["neu"]])

lista = sorted(lista,key=lambda x: x[1], reverse=True)

for e in range(0,lista.len()):
    arquivo.write('\n\n[' + str(lista[e][1]) +']Negativo \n[' + 
          str(lista[e][2]) +"]positivo\n[" + 
          str(lista[e][3]) +"]Neutro\n" + 
          'Texto: ' + limparTweet(tweets[lista[e][0]].text))

arquivo.write(str(tempo_log() + '--> Fim teste de análise de sentimentos '))

arquivo.close()

#!/usr/bin/env python
# coding: utf-8

# # <font color='blue'>Coleta de dados no Twitter utilizando pacote Tweepy do Python</font>

# <b>Professora:</b> <i>Fernanda Farinelli</i>

# Este notebook demonstra os seguintes exemplos:<br>
# 1. Buscar os tweets de um determinado usuário (timeline)
# 2. Realizar a busca dos trends tweets
#   * Trends em múltiplas localizações
#   * Trends no Brasil
# 3. Realizar a busca por palavra chave
# 4. Armazenar o tweets coletados em arquivo JSON
#   

# 
# <b>OBSERVAÇÃO: Antes de utilizar qualquer pacote, é <font color='red'>SEMPRE necessário instalar</font> o(s) pacote(s) previamente. A instalação só é necessária uma única vez.</b>
# 
# * Para instalar pelo Jupyter, utilize o comando abaixo:<br>
#  * <font color='green'>!pip install nome_do_pacote</font>
#     
# 

# In[ ]:


#Instalação de pacotes
#Deve ser realizado apenas na primeira vez que for utilizar

get_ipython().system('pip install tweepy')

get_ipython().system('pip install pymongo')


# **OBSERVAÇÃO:**
# A documentação completa do pacote *tweepy* está disponível no link abaixo:
# * http://docs.tweepy.org/en/v3.5.0/api.html

# **<font color='red'>SEMPRE é necessário importar</font>**  o(s) pacote(s) que serão usados no seu script.

# In[ ]:


#Import package

import tweepy


# In[ ]:





# ### <font color='blue'>Credenciais para utilização da API do Twitter</font>

# Para utilizar a API do twitter, é necessário ter uma conta no twitter, solicitar o acesso de desenvolvedor, criar sua aplicação, gerar suas credenciais.

# In[ ]:


# Credenciais para utilização da API do Twitter

# Observação, as credenciais abaixo são falsas.
# Para este notebook funcionar você precisa criar suas próprias credenciais e informá-las nas respectivas variáveis abaixo:

API_Key = ""
API_secret_key = ""
access_token = ""
access_token_secret = ""


# Fazer a autenticação na API usando suas credenciais

# In[ ]:


#Realizar autenticação no Twitter
auth = tweepy.OAuthHandler(API_Key, API_secret_key)
auth.set_access_token(access_token, access_token_secret)

# Construir uma instancia da API
api = tweepy.API(auth)


# No exemplo acima, criamos a variável api que é uma instância/token já autenticado no twitter. Neste caso, o token usará as configurações padrões para busca de tweets.

# ### Realizar a busca de tweets de um usuário.

# In[ ]:


userName = "ProfessoraIGTI"
userID = "IgtiProfessora"


# In[ ]:


#Buscar tweets de um determinado usuário (timeline do usuário)

user_tweets = api.user_timeline(screen_name=userID,                            
                           count=200, # Buscar no máximo 200 tweets
                           include_rts = False, #Não incluir retweets                           
                           tweet_mode = 'extended' # Necessario para buscar o full_text (280 caracteres)
                           )


# In[ ]:


len(user_tweets)


# In[ ]:


#Exibir o 3 tweets mais atuais

for user_tweet in user_tweets[:3]:
    print("ID: {}".format(user_tweet.id))
    print(user_tweet.created_at)
    print(user_tweet.full_text + "\n")


# ### Realizar a busca dos trends tweets.

# ##### Trends em múltiplas localizações

# In[ ]:


# To fetch the Available Locations that Twitter has trending topic information for.

available_loc = api.trends_available()


# In[ ]:


#Print first vector element
available_loc[0]


# In[ ]:


print("The number of locations available are : " + str(len(available_loc)))


# In[ ]:


print("Some of the locations are : ") 
for i in range(0, 400, 20): 
    print("Place : " + available_loc[i]['name'] +
          ", Country : " + available_loc[i]['country']) 


# ##### Trends no Brasil

# In[ ]:


# WOEID (Where On Earth IDentifier) do Brasil: 23424768
# Veja: https://en.wikipedia.org/wiki/WOEID

BRAZIL_WOEID = 23424768


# In[ ]:


brazil_trends = api.trends_place(BRAZIL_WOEID)


# In[ ]:


print("O nummero de trends para esta localização é: " + str(len(brazil_trends)))


# In[ ]:


#Imprimir primeiro elemento do vetor

brazil_trends[0]["trends"][0]


# In[ ]:


# #Imprimir 5 primeiros elementos do vetor 

print("Os top 5 trends desta localização são:\n")
for i in range(0, 5): 
    print(str(i) + ' - ' + brazil_trends[0]['trends'][i]['name']) 
    #print(brazil_trends[0]['trends'][i]) 


# In[ ]:


#Imprimir todo o vetor, apenas a coluna 'name'

print("Os top trends desta localização são: \n") 
  
for value in brazil_trends: 
    for trend in value['trends']: 
        print(trend['name'])


# Os métodos <i>trends_available</i> e <i>trends_place</i> retorna um conjunto de objetos com informações dos tópicos no formato JSON.

# ### Realizar a busca por palavra chave.

# In[ ]:


#Define palavra chave da busca

keyword = ("'irpf' OR 'imposto de renda' OR '#IRPF2021' OR '#ImpostoDeRenda'")

#keyword = ('vacina')
#keyword = ("covid-19  OR  covid  OR  coronavirus OR pandemic")


# In[ ]:


# Define listas de armazenamento

tweets = []   # apenas tweet text
info = []     # todo o resultado da busca (JSON)


# Nova autenticação para buscar mais tweets que a taxa limite da chamada.
# 
# <font color=red><b>onde:</b></font>
# * <b><i>retry_count</i></b> - número padrão de tentativas para tentar quando ocorrer um erro
# * <b><i>retry_delay</i></b> - número de segundos para aguardar entre tentativas
# * <b><i>wait_on_rate_limit</i></b> - se deve ou não esperar automaticamente a reposição dos limites de taxa
# * <b><i>wait_on_rate_limit_notify</i></b> - Imprima ou não uma notificação quando o Tweepy estiver aguardando a reposição dos limites de taxa

# In[ ]:


# Construir a instancia da API (Já foi realizado antes)

token  = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


# In[ ]:


# Executa a busca por palavra chave

for tweet in tweepy.Cursor(token.search,
                           q=keyword, tweet_mode='extended',
                           rpp=20, #busca até 2000 tweets, no máximo 100 por chamada, limitado a 18000 a cada 15 minutos
                           result_type="mixed", # popular, recent ou mixed
                           lang='pt', #serão solicitados apenas tweets em português
                           include_entities=True).items(20):   
        
    if 'retweeted_status' in dir(tweet): # Checa se é Retweet
        
        # Se status é um Retweet, status.full_text (tweet.full_text) pode estar truncado.
        # Assim, nó buscamos o campo retweeted_status.full_text
        aux=tweet.retweeted_status.full_text       
    
    else: # Não é um Retweet
        aux=tweet.full_text
        
    newtweet = aux.replace("\n", " ")
   
    tweets.append(newtweet) #anexar o texto do tweet a essa lista
    info.append(tweet) #anexar todo o resultado deste tweet a essa lista
    
    #open arquivo txt no modo anexar (append "a") e escrever o resultado no arquivo
    
    file = open("tweets_Keyword_irpf.txt", "a", -1, "utf-8")    
    file.write(newtweet+'\n')
    file.close()


# In[ ]:


info


# Para realizar a busca por palavra chave vamos utilizar a função abaixo:<br>
# * <font color=green>API.search(q[, lang][, locale][, rpp][, page][, since_id][, geocode][, show_user])</font><br><br>
# **onde os principais parâmetros que serão usados são:**
# 
# * <font color=blue>q</font> - a string de consulta de pesquisa
# * <font color=blue>lang</font> - Restringe os tweets para o idioma especificado, fornecido por um código ISO 639-1.
#   - lang=pt -> Português
#   - lang=en -> Inglês
# * <font color=blue>rpp</font> - O número de tweets a serem retornados por página, até no máximo 100.
# * <font color=blue>page</font> - O número da página (começando em 1) a ser retornado, até um máximo de aproximadamente 1500 resultados (com base na página rpp).
# * <font color=blue>since_id</font>  - Retorna apenas status com um ID maior que (ou seja, mais recente que) o ID especificado.
# * <font color=blue>geocode</font>  - Retorna tweets de usuários localizados em um determinado raio da latitude / longitude especificada.
# * <font color=blue>show_user</font>  - Quando verdadeiro, precede "<user>:" no início do tweet. O padrão é falso.
# * <font color=blue>include_entities</font> - O nó de entidades não será incluído quando definido como false. O padrão é true. 
#     - Detalhes sobre este nó, acesse https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/entities-object
# 
# * <font color=blue>tweet_mode</font> - Define qual o campo de texto que será recuperado, texto completo (280 caracteres) ou busca o texto do tweet truncado( 140 caracteres).
#     - tweets = token.search(q=keyword,lang='pt') --> 140 caracteres 
#     - tweets = token.search(q=keyword,tweet_mode='extended') -->280 caracteres
# 
# * <font color=blue>result_type</font> - Define o tipo do tweet a ser recuperado, onde pode ser o mais popular (result_type="popular"), mais recente (result_type="recent") ou uma combinação dos dois (result_type="mixed")    
#     

# In[ ]:


# Para verificar a quantidade de tweets coletado use a função "len()"

print("Total de tweets coletados %s." % (len(info)))


# In[ ]:


tweets


# ### <font color=blue>Armazenar o tweets coletados</font> 

# ##### <font color=red>Armazenar em arquivo JSON</font>

# In[ ]:


#Install
#!pip install json

#Import
import json


# In[ ]:


# writing a JSON file that has the available trends around the world

with open("tweets_irpf_pt.json","w") as filename: #open file in write mode


    for tweet in info: #para cada tweet no vetor de resultados tweets
        
        status = tweet
        
        #converte para string        
        json_str = json.dumps(status._json)
        
        #deserializa a string para um objeto python do tipo dict        
        parsed = json.loads(json_str)
        
        #grava o tweet deserializado no arquivo
        filename.write(json.dumps(parsed, indent=4))

    


# ##### <font color=red>Armazenar em arquivo CSV</font>

# In[ ]:


#Install
#!pip install pandas
#!pip install numpy

#Import
import pandas as pd
import numpy as np


# Para mais detalhes sobre o pacote **Pandas** acesse:
# * https://pandas.pydata.org/
# * https://medium.com/data-hackers/uma-introdu%C3%A7%C3%A3o-simples-ao-pandas-1e15eea37fa1
# 
# Para mais detalhes sobre o pacote **Numpy** acesse:
# * https://numpy.org/
# * https://medium.com/ensina-ai/entendendo-a-biblioteca-numpy-4858fde63355

# In[ ]:


#Define um dataframe para armazenar os dados dos tweets

tweets_df = pd.DataFrame(tweets, columns=['Tweets']) #Store tweet text from tweets list

tweets_df['len']  = np.array([len(tweet) for tweet in tweets])  #Store tweet text size from tweets list

tweets_df['ID']   = np.array([tweet.id for tweet in info])
tweets_df['USER']   = np.array([tweet.user.screen_name for tweet in info])
tweets_df['userName'] = np.array([tweet.user.name for tweet in info])
tweets_df['User Location']    = np.array([tweet.user.location for tweet in info])
tweets_df['Language'] = np.array([tweet.user.lang for tweet in info])
tweets_df['Date'] = np.array([tweet.created_at for tweet in info])
tweets_df['Source'] = np.array([tweet.source for tweet in info])
tweets_df['Likes']  = np.array([tweet.favorite_count for tweet in info])
tweets_df['Retweets']    = np.array([tweet.retweet_count for tweet in info])


# Escrever/gravar arquivo CSV a partir do dataframe
tweets_df.to_csv("tweets_Keyword_IRPF.csv")


# In[ ]:


#Print first 3 rows of dataframe
tweets_df.head(3)


# In[ ]:


#Podemos imprimir o nome do usuário (screen_name) e o texto do tweet
tweet = info[0]

print("Usuário: %s "% {tweet.user.screen_name})
print("  Tweet: %s"  % {tweet.full_text}) #No caso da busca em tweet_mode='extended' (até 280 caracteres)

#print("  Tweet: %s"  % {tweet.text}) # Se a busca não foi em tweet_mode='extended'  (até 140 caracteres)


# FIM!

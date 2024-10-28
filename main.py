import pandas as pd
import requests
from bs4 import BeautifulSoup

from extract import extrair_tabela
from convert import converter_pesos
from convert import converter_datas

url_santos = 'https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga/'
url_paranagua = 'https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo'




# Como as 2 fontes de dados são diferentes, crio 2 maneiras de coletar os dados, uma para cada porto. 

######------------------------------- SANTOS -------------------------#

#Extrai a tabela de Importação do Porto de Santos e filtra as colunas
df = extrair_tabela(url_santos, 'GRANEIS SOLIDOS - IMPORTACAO')
df_santos_import = df[[4, 8, 9]]

#Formata a tabela no padrão 
df_santos_import = pd.DataFrame({
    
    'Produto':df_santos_import[8],
    'Data': df_santos_import[4],
    'Peso': df_santos_import[9],
    'Exp/Imp': 'Imp',
     'Porto': 'Santos' }) 

#Extrai a tabela de Exportação do Porto de Santose filtra as colunas
df = extrair_tabela(url_santos, 'GRANEIS SOLIDOS - EXPORTACAO')
df_santos_export = df[[4, 8, 9]]

#Formata a tabela no padrão
df_santos_export = pd.DataFrame({
    
    'Produto': df_santos_export[8],
    'Data': df_santos_export[4],
    'Peso': df_santos_export[9],
    'Exp/Imp': 'Exp',
     'Porto': 'Santos' }) 

######---------------------------------------------------------------------#

######------------------------------- PARANAGUA -------------------------#
df_paranagua = extrair_tabela(url_paranagua, 'ESPERADOS')

df_paranagua = pd.DataFrame({
    
    'Produto':df_paranagua[11],
    'Data': df_paranagua[12],
    'Peso': df_paranagua[15],
    'Exp/Imp': df_paranagua[8],
     'Porto': 'Paranagua' }) 


######---------------------------------------------------------------------#
#Concatena os DataFrames em um só
df_portos = pd.concat([df_santos_export, df_santos_import, df_paranagua])

#Converte as Datas e Pesos para um padrão unico 
df_portos = converter_datas(df_portos)
df_portos = converter_pesos(df_portos)

#Mostra na tela as tabelas unidas
print(df_portos)


#Cria um arquivo .CSV com as informações
df_portos.to_csv('portos.csv', index=False)


#Problemas encontrados:
#1 - Como encontrar ou puxar as informações somente com o nome da coluna 
#2 - Padrozinar as coletas de dados de diferentes sites usando um método simples que funcione em todos, (Por exemplo nesse caso, em santos tinha 1 tabela pra exportação e outra para importação,
#     e o outro tem uma coluna única que junta essas informações)
#3 - Remover as linhas indesejadas na hora da coleta de informações e não após ja ter coletado a tabela toda ( Como no caso ele puxa o titulo da tabela e o titulo da coluna e após eu removo)
#4 - Padronização dos pesos, algumas informações estão em Kg, Tons, e no caso de Conteiners em Movs.

import pandas as pd
import requests
from bs4 import BeautifulSoup

from extract import extrair_tabela

url_santos = 'https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga/'
url_paranagua = 'https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo'




# Como as 2 fontes de dados são diferentes, crio 2 maneiras de coletar os dados, uma para cada porto. 

######------------------------------- SANTOS -------------------------#
#Extrai a tabela de Importação do Porto de Santos
df = extrair_tabela(url_santos, 'GRANEIS SOLIDOS - IMPORTACAO')
df_santos_import = df[[4, 8, 9]]

#Extrai a tabela de Exportação do Porto de Santos
df = extrair_tabela(url_santos, 'GRANEIS SOLIDOS - EXPORTACAO')
df_santos_export = df[[4, 8, 9]]

df_filtrado_import = pd.DataFrame({
    #'ID': range(1, len(df_santos_import) + 1),
    'Produto':df_santos_import[8],
    'Data': df_santos_import[4],
    'Peso': df_santos_import[9],
    'Exp/Imp': 'Imp',
     'Porto': 'Santos' }) 

df_filtrado_export = pd.DataFrame({
    #'ID': range(1, len(df_santos_export) + 1),
    'Produto': df_santos_export[8],
    'Data': df_santos_export[4],
    'Peso': df_santos_export[9],
    'Exp/Imp': 'Exp',
     'Porto': 'Santos' }) 
#Junta os 2 DF em um só
df_final_Santos = pd.concat([df_filtrado_export, df_filtrado_import])

######---------------------------------------------------------------------#

######------------------------------- PARANAGUA -------------------------#
df_paranagua = extrair_tabela(url_paranagua, 'ESPERADOS')

df_paranagua = pd.DataFrame({
    #'ID': range(1, len(df_santos_import) + 1),
    'Produto':df_paranagua[11],
    'Data': df_paranagua[12],
    'Peso': df_paranagua[15],
    'Exp/Imp': df_paranagua[8],
     'Porto': 'Paranagua' }) 



df_portos = pd.concat([df_final_Santos, df_paranagua])
print(df_portos)



#Problemas encontrados:
#1 - Como encontrar ou puxar as informações somente com o nome da coluna 
#2 - Padrozinar as coletas de dados de diferentes sites usando um método simples que funcione em todos, (Por exemplo nesse caso, em santos tinha 1 tabela pra exportação e outra para importação,
#     e o outro tem uma coluna única que junta essas informações)
#3 - Remover as linhas indesejadas na hora da coleta de informações e não após ja ter coletado a tabela toda ( Como no caso ele puxa o titulo da tabela e o titulo da coluna e após eu removo)
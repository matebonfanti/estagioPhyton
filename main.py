import pandas as pd
import requests
from bs4 import BeautifulSoup

from extract import extrair_tabela

url_santos = 'https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga/'
url_paranagua = 'https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo'


df = extrair_tabela(url_santos, 'GRANEIS SOLIDOS - IMPORTACAO')



print(df)
# Mostrar os dados na tela
# for linha in dados_tabela:
#     print('\t'.join(linha))
import pandas as pd
import requests
from bs4 import BeautifulSoup

#Função para extrair a tabela de um site, com a URL e o nome da tabela, e retorna um Data Frame com as informações
def extrair_tabela(url, nome):
        # Fazer a requisição HTTP para obter o conteúdo da página
    resposta = requests.get(url, verify=False)

    # Analisar o HTML da página
    soup = BeautifulSoup(resposta.content, 'html.parser')

    # Encontrar a tabela desejada (exemplo com id)
    #tabela = soup.find('table')
    #tab_exp = tabela[2]

    # Encontrar todas as tabelas
    tabelas = soup.find_all('table')

    # Filtrar a tabela desejada
    tabela_desejada = None
    for tabela in tabelas:
        if tabela.find(text=nome):
            tabela_desejada = tabela
            break

    # se encontrou a tabela extrai os dados
    if tabela_desejada:
        
        linhas = tabela_desejada.find_all('tr')
        dados_tabela = []
        for linha in linhas:
            celulas = linha.find_all(['td', 'th'])
            linha_dados = [celula.get_text().strip() for celula in celulas]
            dados_tabela.append(linha_dados)

    else:
        print('Tabela não encontrada')


    #Criar um Data Frame
    return pd.DataFrame(dados_tabela)
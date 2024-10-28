import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


#Função para converter as datas em um padrão recebendo um Dataframe como parametro

def converter_datas(df):
    # Converter as colunas para datetime com formato misto e primeiro o dia 
    df['Data'] = pd.to_datetime(df['Data'], format='mixed', dayfirst=True) 
    # Formatar para exibir somente a data 
    df['Data'] = df['Data'].dt.date

    return (df)


   
def converter_pesos(df):

    # Aplicar a função à coluna 'Peso'
    df['Peso'] = df['Peso'].apply(padronizar_peso)

    return (df)


def padronizar_peso(peso):
    if peso is None: 
        return ('0')
    
    # Substituir vírgula por ponto e ponto por nada nos milhares para padronizar o formato numérico 
    peso = peso.replace('.', '').replace(',', '.')

    # Usar regex para extrair números e unidade
    match = re.match(r'(\d+(\.\d+)?)\s*([a-zA-Z]*)', peso)
    if match:
        numero = float(match.group(1))
        unidade = match.group(3).lower() if match.group(3) else ''

        # Converter para quilos
        if unidade == 'kg':
            return numero
        elif unidade == 'g':
            return numero / 1000
        elif unidade == 'lbs':
            return numero * 0.453592
        elif unidade == 'tons':
            return numero * 1000
        else:
            return numero  # Caso não tenha unidade, assumimos que já está em kg
    return peso  # Caso não seja possível converter


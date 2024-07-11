import requests
import time
import os
import json
import warnings
import urllib3
import datetime

# Tira avisos de InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Defininindo variaveis

api_arbor = 'https://<ARBOR DDOS HOST-IP HERE>/api/sp/alerts'
headers_arbor = {
    "X-Arbux-APIToken": "<ARBOR TOKEN HERE>"
}

api_soar = 'https://<FORTISOAR HOST-IP HERE>/api/triggers/1/deferred/<api-name-here>'
headers_soar = {'Content-Type': 'application/json'}

dir = '<dir where registros.log and ultimoID.txt file it's located'

ultimoID = None

def log(mensagem):
    data_atual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log = f"{data_atual} - {mensagem}\n"

    with open(dir + "registros.log", "a") as arquivolog:
        arquivolog.write(log)

def pegaUltimoID():
    with open(dir + "ultimoID.txt", "r") as arquivo:
        ultimoID = arquivo.read()
        ultimoID = int(ultimoID)
    return ultimoID

def buscaAlertas():
    response = requests.get(api_arbor, headers=headers_arbor)  # faz a requisição API
    if response.status_code == 200:  # verificar se o status code foi 200, ou seja, sucesso
        return response.json()  # Retorna os dados da resposta JSON em dicionario Python
    else:
        log(f"funcao buscaAlertas - Erro ao acessar a API, erro número {response.status_code}")

def salvaNovoUltimoID(novoID):
    with open(dir + "ultimoID.txt", "w") as arquivo:
        arquivo.write(str(novoID))

def main():
    dados = buscaAlertas()  # armazena o dicionario do resultado da funcao em uma variavel
    ultimoID = pegaUltimoID()  # armazena o ultimo ID utilizado
    novosID = []  # inicia a lista de IDs coletados durante o for
    log (f"Iniciando dump de alertas, ultimo ID enviado: {ultimoID}")
    for objeto in reversed(dados.get('data')):  # percorre os objetos dentro do array data
        objeto_id = int(objeto.get('id'))  # pega o ID de cada objeto
        if objeto_id > ultimoID:  # verifica se o ID é maior que o ultimo, se for faz a chamada
             novosID.append(objeto_id)
             objeto_json = json.dumps(objeto)
             post = requests.post(api_soar, data=objeto_json, headers=headers_soar, verify=False, auth=("<FORTISOAR USERNAME>", "<FORTISOAR PASSWORD>"))
             if post.status_code == 200:
                  log(f"ID {objeto_id} enviado com sucesso.")
             else:
                  log(f"Erro ao enviar o alerta ID {objeto_id}, erro número {post.status_code}: {post.text}")

    if novosID:
         novo_ultimoID = max(novosID)
         salvaNovoUltimoID(novo_ultimoID)
    else:
         log("Nao foram encontrados novos alertas")
         
main()

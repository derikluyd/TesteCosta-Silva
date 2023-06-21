import requests
from bs4 import BeautifulSoup
import json

def consultar_processos(parametros):
    url = "https://eproc.trf2.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"
    response = requests.post(url, data=parametros)
    return response.content

def extrair_processos(html):
    soup = BeautifulSoup(html, "html.parser")
    processos = []

    # Extrair informações dos processos listados na página de consulta
    # Preencha as informações de acordo com a estrutura da página HTML
    for processo_html in soup.find_all("div", class_="processo"):
        processo = {
            "numero_processo": processo_html.find("span", class_="numero_processo").text.strip(),
            "autor": processo_html.find("span", class_="autor").text.strip(),
            "reu": processo_html.find("span", class_="reu").text.strip()
        }
        processos.append(processo)

    return processos

def extrair_detalhes_processo(html):
    soup = BeautifulSoup(html, "html.parser")
    detalhes = {}

    # Extrair informações detalhadas do processo
    # Preencha as informações de acordo com a estrutura da página HTML
    detalhes["numero_processo"] = soup.find("span", class_="numero_processo").text.strip()
    detalhes["data_autuacao"] = soup.find("span", class_="data_autuacao").text.strip()
    detalhes["situacao"] = soup.find("span", class_="situacao").text.strip()

    # Extrair informações das partes e representantes
    detalhes["envolvidos"] = []
    for envolvido_html in soup.find_all("div", class_="envolvido"):
        envolvido = {
            "papel": envolvido_html.find("span", class_="papel").text.strip(),
            "nome": envolvido_html.find("span", class_="nome").text.strip()
        }
        detalhes["envolvidos"].append(envolvido)

    # Extrair informações das movimentações
    detalhes["movimentacoes"] = []
    for movimentacao_html in soup.find_all("div", class_="movimentacao"):
        movimentacao = {
            "data": movimentacao_html.find("span", class_="data").text.strip(),
            "texto": movimentacao_html.find("span", class_="texto").text.strip()
        }
        detalhes["movimentacoes"].append(movimentacao)

    return detalhes
def persistir_dados(processos):
    with open("dados.jsonl", "a") as file:
        for processo in processos:
            file.write(json.dumps(processo) + "\n")

# Exemplo de consulta por número do processo
parametros = {
    "numero_processo": "5012208-69.2019.4.02.0000"
}
html = consultar_processos(parametros)
processos = extrair_processos(html)
persistir_dados(processos)


parametros = {
    "cnpj": "33.649.575/0001-99"
}
html = consultar_processos(parametros)
processos = extrair_processos(html)
persistir_dados(processos)


parametros = {
    "nome_parte": "Nome da Parte"
}
html = consultar_processos(parametros)
processos = extrair_processos(html)
persistir_dados(processos)


parametros = {
    "chave_processo": "Chave do Processo"
}
html = consultar_processos(parametros)
processos = extrair_processos(html)
persistir_dados(processos)


parametros = {
    "oab": "Número da OAB"
}
html = consultar_processos(parametros)
processos = extrair_processos(html)
persistir_dados(processos)

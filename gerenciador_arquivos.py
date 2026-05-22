import json
import os
from datetime import datetime

# Caminhos dos arquivos
ARQUIVO_JSON = "historico.json"
ARQUIVO_LOG = "erros.txt"

def salvar_historico(dados_clima):
    """
    Salva a consulta de clima no arquivo historico.json.
    Requisito: Manipulação de arquivos .json e estruturas JSON.
    """
    historico = []
    
    # Se o arquivo já existir, lê o conteúdo atual
    if os.path.exists(ARQUIVO_JSON):
        try:
            with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
                historico = json.load(f)
        except Exception:
            historico = []

    # Adiciona a nova consulta com data e hora
    dados_clima["data_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    historico.append(dados_clima)

    # Requisito: Estrutura de repetição (exemplo simples de limpeza opcional se histórico for muito longo)
    if len(historico) > 50:
        historico = historico[-50:]

    # Salva de volta no arquivo
    try:
        with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
            json.dump(historico, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        registrar_erro(f"Erro ao salvar JSON: {e}")
        return False

def registrar_erro(mensagem):
    """
    Registra erros em um arquivo de log .txt.
    Requisito: Manipulação de arquivos .txt.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(ARQUIVO_LOG, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {mensagem}\n")
    except Exception as e:
        print(f"Erro crítico ao escrever log: {e}")

def carregar_historico():
    """Lê e retorna o histórico completo."""
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

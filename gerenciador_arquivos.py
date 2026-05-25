import json
import os
from datetime import datetime

ARQUIVO_JSON = "historico.json"
ARQUIVO_LOG = "erros.txt"

def salvar_historico(dados_clima):
    historico = []
    
    if os.path.exists(ARQUIVO_JSON):
        try:
            with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
                historico = json.load(f)
        except Exception:
            historico = []

    dados_clima["data_hora"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    historico.append(dados_clima)

    if len(historico) > 50:
        historico = historico[-50:]

    try:
        with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
            json.dump(historico, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        registrar_erro(f"Erro ao salvar JSON: {e}")
        return False

def registrar_erro(mensagem):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(ARQUIVO_LOG, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {mensagem}\n")
    except Exception as e:
        print(f"Erro crítico ao escrever log: {e}")

def carregar_historico():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

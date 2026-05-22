import requests
import os
from dotenv import load_dotenv

load_dotenv()

def enviar_para_ia_n8n(dados_clima):
    """
    Envia os dados do clima para o n8n via Webhook para obter uma recomendação de IA real.
    Exige que a URL do Webhook esteja configurada no arquivo .env.
    """
    webhook_url = os.getenv("N8N_WEBHOOK_URL")
    
    if not webhook_url or "SUA_URL" in webhook_url or not webhook_url.strip():
        return "Erro de Configuração: A variável de ambiente N8N_WEBHOOK_URL não foi configurada ou está vazia no seu arquivo .env. Por favor, configure-a com a URL do seu Webhook do n8n para obter o retorno real da IA."

    webhook_url = webhook_url.strip()
    print(f"DEBUG: Enviando dados do clima para o n8n ({webhook_url})...")
    try:
        import time
        start_time = time.time()
        response = requests.post(webhook_url, json=dados_clima, timeout=20)
        duration = time.time() - start_time
        print(f"DEBUG: Resposta do n8n recebida em {duration:.2f}s (Status: {response.status_code})")
        
        if "application/json" in response.headers.get("Content-Type", ""):
            if response.status_code == 200:
                resultado = response.json()
                # Tenta obter a recomendação a partir de campos comuns retornados pelo n8n
                ia_msg = resultado.get("recomendacao") or resultado.get("output") or resultado.get("text")
                if ia_msg:
                    return ia_msg
                else:
                    return f"Erro de Resposta: O n8n respondeu com sucesso, mas o JSON retornado não contém as chaves esperadas ('recomendacao', 'output' ou 'text'). Resposta crua: {resultado}"
            else:
                return f"Erro no Servidor n8n (Status {response.status_code}): {response.text[:100]}"
        else:
            return f"Erro no Formato da Resposta: O n8n respondeu com o status {response.status_code}, mas o conteúdo retornado não é JSON. Verifique a configuração do nó 'Respond to Webhook' no seu workflow do n8n."
            
    except requests.exceptions.Timeout:
        return "Erro de Conexão: A requisição ao n8n atingiu o tempo limite (Timeout de 20s). Verifique se o seu servidor n8n está ativo e respondendo."
    except Exception as e:
        return f"Falha Crítica na Conexão com n8n: {e}. Verifique se a URL do Webhook está correta e se há conectividade com a internet."


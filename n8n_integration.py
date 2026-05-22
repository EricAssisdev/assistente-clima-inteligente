import requests
import os
from dotenv import load_dotenv

load_dotenv()

def enviar_para_ia_n8n(dados_clima):
    """
    Envia os dados do clima para o n8n via Webhook para obter uma recomendação de IA.
    Se não houver URL configurada, simula uma resposta da IA.
    """
    webhook_url = os.getenv("N8N_WEBHOOK_URL")
    
    # Se não houver URL ou for o placeholder, simula a IA (Requisito: Simulação ou Consumo de IA)
    if not webhook_url or "SUA_URL" in webhook_url:
        return simular_ia(dados_clima)

    print(f"DEBUG: Enviando dados para {webhook_url}...")
    try:
        import time
        start_time = time.time()
        response = requests.post(webhook_url, json=dados_clima, timeout=20)
        duration = time.time() - start_time
        print(f"DEBUG: Resposta recebida em {duration:.2f}s (Status: {response.status_code})")
        
        if "application/json" in response.headers.get("Content-Type", ""):
            if response.status_code == 200:
                resultado = response.json()
                # Tenta pegar a resposta em diferentes campos comuns do n8n/IA
                ia_msg = resultado.get("recomendacao") or resultado.get("output") or resultado.get("text")
                if ia_msg:
                    return ia_msg
                else:
                    # Se não achar campos conhecidos, retorna o JSON inteiro formatado
                    return f"IA: {resultado}"
            else:
                return f"Erro n8n (Status {response.status_code}): {response.text[:100]}"
        else:
            return f"Erro: Resposta não é JSON. Verifique o nó de Resposta no n8n. (Status {response.status_code})"
            
    except requests.exceptions.Timeout:
        return "Erro: O n8n demorou demais para responder (Timeout de 20s)."
    except Exception as e:
        return f"Falha na conexão com n8n: {e}"

def simular_ia(dados_clima):
    """Gera uma recomendação baseada em lógica simples caso a IA/n8n esteja indisponível."""
    temp = dados_clima["temperatura"]
    desc = dados_clima["descricao"].lower()
    
    # Requisito: Estruturas condicionais
    if "chuva" in desc:
        return "IA Sugere: Não esqueça o guarda-chuva e evite atividades ao ar livre."
    elif temp > 25:
        return "IA Sugere: Está calor! Use roupas leves e mantenha-se hidratado."
    elif temp < 15:
        return "IA Sugere: Está frio. Recomendo um casaco reforçado."
    else:
        return "IA Sugere: O tempo está agradável. Uma ótima oportunidade para uma caminhada!"

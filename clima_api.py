import requests
import os
from dotenv import load_dotenv

load_dotenv()

def buscar_clima(cidade):
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("Erro: Chave de API não encontrada no arquivo .env")
        return None
        
    api_key = api_key.strip()
    cidade_query = cidade.replace(" ", "%20")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade_query}&appid={api_key}&units=metric&lang=pt_br"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            dados = response.json()
            return {
                "cidade": dados["name"],
                "temperatura": dados["main"]["temp"],
                "descricao": dados["weather"][0]["description"],
                "umidade": dados["main"]["humidity"]
            }
        elif response.status_code == 404:
            print(f"Erro: Cidade '{cidade}' não encontrada.")
            return None
        else:
            print(f"Erro na API: Status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return None

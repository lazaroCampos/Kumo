import requests
import os
from dotenv import load_dotenv

# 1. Carrega a tua senha do arquivo .env
load_dotenv()

def obter_clima(cidade):
    chave_api = os.getenv("API_KEY")
    
    # Verificação de segurança básica
    if not chave_api:
        return {"sucesso": False, "erro": "Chave API não encontrada (.env)"}

    # 2. Monta a URL (O endereço da API)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave_api}&units=metric&lang=pt_br"

    try:
        # 3. Faz o pedido (Request)
        response = requests.get(url)
        
        # 4. Transforma a resposta bruta em Dicionário Python (O tal do JSON!)
        dados_brutos = response.json()

        # Se o site respondeu "OK" (Código 200)
        if response.status_code == 200:
            return {
                "sucesso": True,
                "cidade": dados_brutos["name"],
                "temperatura": dados_brutos["main"]["temp"],
                "descricao": dados_brutos["weather"][0]["description"],
                # AQUI está o segredo: pegamos o código (ex: "04d", "09n")
                "icone_id": dados_brutos["weather"][0]["icon"] 
            }
        
        # Se deu erro 404 (Cidade não existe)
        elif response.status_code == 404:
            return {"sucesso": False, "erro": "Cidade não encontrada."}
        
        else:
            return {"sucesso": False, "erro": "Erro na API."}

    except Exception as e:
        return {"sucesso": False, "erro": f"Erro de conexão: {e}"}

# Bloco de teste: Só roda se executares este arquivo diretamente
if __name__ == "__main__":
    # Teste rápido para ver o JSON a funcionar
    resultado = obter_clima("Lisboa")
    print(resultado)
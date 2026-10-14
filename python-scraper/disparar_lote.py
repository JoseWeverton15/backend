import os
import json
import requests

def disparar_extracao_lote():
    # Caminho do arquivo de links gerado na busca
    caminho_links = os.path.join(os.path.dirname(os.path.abspath(__file__)), "links_encontrados.json")
    
    if not os.path.exists(caminho_links):
        print("❌ Arquivo 'links_encontrados.json' não encontrado. Execute a busca primeiro.")
        return

    # Lê os links salvos
    with open(caminho_links, "r", encoding="utf-8") as f:
        dados_busca = json.load(f)
        lista_links = dados_busca.get("links", [])

    if not lista_links:
        print("❌ A lista de links está vazia.")
        return

    print(f"🚀 Enviando {len(lista_links)} links para o endpoint de extração em lote...")

    url_endpoint = "http://localhost:5001/api/scraper/extrair-lote"
    payload = {"links": lista_links}

    try:
        # Faz a requisição POST para o Flask
        response = requests.post(url_endpoint, json=payload, timeout=120)
        
        if response.status_code == 200:
            resultado = response.json()
            print(resultado)
            print("\n" + "="*50)
            print("✅ SUCESSO! LOTE EXTRAÍDO COM SUCESSO:")
            print(f"-> Total processados: {resultado.get('total_processados')}/{resultado.get('total_links_origem')}")
            print(f"-> Falhas finais: {resultado.get('falhas_finais')}")
            print(f"-> Tempo de execução: {resultado.get('tempo_execucao_segundos')}s")
            print("="*50)
        else:
            print(f"❌ Erro HTTP {response.status_code}: {response.text}")

    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    disparar_extracao_lote()
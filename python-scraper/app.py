import time
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
from buscador_olx import extrair_links_pagina_busca
from scraper_teste import extrair_anuncio_olx  # Importa seu extrator otimizado com cache

app = Flask(__name__)
MAX_WORKERS = 20  # Número de threads paralelas

@app.route('/api/scraper/buscar-links', methods=['POST'])
def buscar_links():
    """
    Passos 1 e 2: Recebe a URL de busca da OLX e retorna os links encontrados.
    """
    data = request.get_json()
    if not data or 'url_busca' not in data:
        return jsonify({"erro": "O campo 'url_busca' é obrigatório no corpo da requisição."}), 400

    url_busca = data['url_busca']
    print(f"📥 [Busca] Processando URL: {url_busca}")
    
    links = extrair_links_pagina_busca(url_busca)
    
    return jsonify({
        "url_busca": url_busca,
        "total_links": len(links),
        "links": links
    }), 200

@app.route('/api/scraper/anuncio', methods=['POST'])
def extrair_anuncio_unico():
    """
    Recebe a URL de um único anúncio e retorna seus dados detalhados.
    """
    data = request.get_json()
    if not data or 'url_anuncio' not in data:
        return jsonify({"erro": "O campo 'url_anuncio' é obrigatório no corpo da requisição."}), 400

    url_anuncio = data['url_anuncio']
    print(f"📥 [Anúncio Único] Processando URL: {url_anuncio}")
    
    try:
        dados_anuncio = extrair_anuncio_olx(url_anuncio)
        return jsonify(dados_anuncio), 200
    except Exception as e:
        print(f"❌ Erro ao extrair anúncio {url_anuncio}: {e}")
        return jsonify({"erro": str(e)}), 500

@app.route('/api/scraper/extrair-lote', methods=['POST'])
def extrair_lote():
    """
    Passos 3 e 4: Recebe a lista de links de anúncios selecionados,
    executa o scraping em paralelo (com cache e retries) e devolve o lote bruto completo.
    """
    data = request.get_json()
    if not data or 'links' not in data:
        return jsonify({"erro": "O campo 'links' (lista de URLs) é obrigatório."}), 400

    links_pendentes = data['links']
    total_links_origem = len(links_pendentes)
    
    if not links_pendentes:
        return jsonify({"erro": "A lista de links enviada está vazia."}), 400

    print("=" * 60)
    print(f"🚀 [Lote] INICIANDO EXTRAÇÃO DE {total_links_origem} ANÚNCIOS")
    print(f"⚡ THREADS PARALELAS: {MAX_WORKERS}")
    print("=" * 60)

    resultados_finais = {}
    inicio_total = time.time()
    max_tentativas_lote = 100  # Limite de rodadas de retry para links que falharem

    for rodada in range(1, max_tentativas_lote + 1):
        if not links_pendentes:
            break

        print(f"🔄 --- RODADA {rodada}/{max_tentativas_lote} (Pendentes: {len(links_pendentes)}) ---")

        tarefas = [(idx, len(links_pendentes), url) for idx, url in enumerate(links_pendentes, 1)]
        falhas_rodada = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Reutiliza o worker individual que você já usa no seu script
            futures = [executor.submit(_processar_anuncio_worker_remoto, tarefa) for tarefa in tarefas]
            for future in as_completed(futures):
                res = future.result()
                if res["status"] in ["SUCESSO", "CACHE"]:
                    resultados_finais[res["url"]] = res["dados"]
                else:
                    falhas_rodada.append(res["url"])

        links_pendentes = falhas_rodada
        

    tempo_total = time.time() - inicio_total
    sucessos = list(resultados_finais.values())

    # Monta a estrutura final idêntica ao lote_bruto_extraido.json
    relatorio_consolidado = {
        "total_links_origem": total_links_origem,
        "total_processados": len(sucessos),
        "falhas_finais": len(links_pendentes),
        "tempo_execucao_segundos": round(tempo_total, 2),
        "anuncios": sucessos
    }

    print("=" * 60)
    print(f"✅ [Lote] CONCLUÍDO! Sucessos: {len(sucessos)}/{total_links_origem} em {round(tempo_total, 2)}s")
    print("=" * 60)

    # Retorna o JSON completo diretamente para o backend Java (ou cliente)
    return jsonify(relatorio_consolidado), 200


def _processar_anuncio_worker_remoto(args):
    """Função auxiliar interna para rodar a extração unitária reaproveitando o scraper existente."""
    idx, total, url = args
    try:
        dados_brutos = extrair_anuncio_olx(url)
        # Se veio do cache ou sucesso, o scraper já lida com isso
        status = "CACHE" if dados_brutos.get("_origem_cache") else "SUCESSO"
        return {
            "status": status,
            "url": url,
            "dados": dados_brutos
        }
    except Exception as e:
        return {
            "status": "ERRO",
            "url": url,
            "erro": str(e)
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
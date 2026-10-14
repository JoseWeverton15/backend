import os
import re
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper_teste import extrair_anuncio_olx

# Configurações do Pipeline Worker
MAX_WORKERS = 20  # Número de navegadores/threads rodando em paralelo
ARQUIVO_LINKS_ENTRADA = "links_encontrados.json"
ARQUIVO_LOTE_SAIDA = "lote_bruto_extraido.json"


def extrair_id_da_url(url):
    """
    Extrai o ID numérico ao final da URL da OLX.
    """
    match = re.search(r"-(\d+)(\?|$)", url)
    return match.group(1) if match else None


def carregar_links_entrada():
    """
    Lê o arquivo JSON gerado pelo buscador_olx.py contendo a lista de links.
    """
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    caminho_json = os.path.join(diretorio_script, ARQUIVO_LINKS_ENTRADA)

    if not os.path.exists(caminho_json):
        print(f"❌ Erro: Arquivo de entrada '{ARQUIVO_LINKS_ENTRADA}' não encontrado.")
        return []

    try:
        with open(caminho_json, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados.get("links", [])
    except Exception as e:
        print(f"❌ Erro ao ler '{ARQUIVO_LINKS_ENTRADA}': {e}")
        return []


def processar_anuncio_worker(args):
    """
    Função de worker executada individualmente por cada thread.
    """
    idx, total, url = args
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    id_anuncio = extrair_id_da_url(url)

    # VERIFICAÇÃO DE CACHE: Checa se a pasta e o arquivo dados_brutos.json já existem
    if id_anuncio:
        caminho_json_existente = os.path.join(diretorio_script, ".temp", id_anuncio, "dados_brutos.json")
        if os.path.exists(caminho_json_existente):
            try:
                with open(caminho_json_existente, "r", encoding="utf-8") as f:
                    dados_existentes = json.load(f)
                
                #print(f"⚡ [{idx}/{total}] Anúncio [{id_anuncio}] já existe em cache. Pulando navegação...")
                return {
                    "status": "CACHE",
                    "url": url,
                    "dados": dados_existentes
                }
            except Exception as e:
                print(f"⚠️ Erro ao ler cache do anúncio [{id_anuncio}]: {e}. Re-executando scraping...")

    #print(f"🚀 [{idx}/{total}] Disparando extração: {url}")
    
    try:
        dados_brutos = extrair_anuncio_olx(url)
        return {
            "status": "SUCESSO",
            "url": url,
            "dados": dados_brutos
        }
    except Exception as e:
        #print(f"❌ Erro ao extrair anúncio {url}: {e}")
        return {
            "status": "ERRO",
            "url": url,
            "erro": str(e)
        }

def executar_pipeline_scraping(max_tentativas_lote=400):
    print("=" * 60)
    print(" INICIANDO PIPELINE DE SCRAPING RESILIENTE")
    print(" QUANTIDADE DE THREADS: ", MAX_WORKERS)
    print("=" * 60)

    links_pendentes = carregar_links_entrada()
    if not links_pendentes:
        print("Nenhum link encontrado. Encerrando.")
        return

    total_links_origem = len(links_pendentes)
    resultados_finais = {}
    inicio_total = time.time()

    for rodada in range(1, max_tentativas_lote + 1):
        if not links_pendentes:
            break

        print(f"\n🔄 --- RODADA {rodada}/{max_tentativas_lote} (Links pendentes: {len(links_pendentes)}) ---")

        tarefas = [(idx, len(links_pendentes), url) for idx, url in enumerate(links_pendentes, 1)]
        falhas_rodada = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(processar_anuncio_worker, tarefa) for tarefa in tarefas]
            for future in as_completed(futures):
                res = future.result()
                if res["status"] in ["SUCESSO", "CACHE"]:
                    resultados_finais[res["url"]] = res["dados"]
                else:
                    falhas_rodada.append(res["url"])

        links_pendentes = falhas_rodada
        if links_pendentes and rodada < max_tentativas_lote:
            print(f"⚠️ {len(links_pendentes)} falhas ocorridas. Aguardando 2s antes da próxima rodada...")
            

    tempo_total = time.time() - inicio_total

    # Consolidação do Relatório Final
    sucessos = list(resultados_finais.values())
    relatorio_consolidado = {
        "total_links_origem": total_links_origem,
        "total_processados": len(sucessos),
        "falhas_finais": len(links_pendentes),
        "tempo_execucao_segundos": round(tempo_total, 2),
        "anuncios": sucessos
    }

    caminho_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), ARQUIVO_LOTE_SAIDA)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(relatorio_consolidado, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(" RESUMO DA EXECUÇÃO FINAL:")
    print(f" -> Sucessos obtidos: {len(sucessos)} / {total_links_origem}")
    print(f" -> Falhas não resolvidas: {len(links_pendentes)}")
    print(f" -> Tempo total acumulado: {round(tempo_total, 2)}s")
    print(f" -> Relatório salvo em: {caminho_saida}")
    print("=" * 60)

if __name__ == "__main__":
    executar_pipeline_scraping()
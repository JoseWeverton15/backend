import os
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from scrapper_perfil import extrair_perfil_olx, extrair_uuid_da_url_perfil

MAX_WORKERS = 10
ARQUIVO_ANUNCIOS_ENTRADA = "lote_bruto_extraido.json"
ARQUIVO_PERFIS_SAIDA = "lote_perfis_extraido.json"


def carregar_links_perfis_unicos():
    diretorio = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(diretorio, ARQUIVO_ANUNCIOS_ENTRADA)

    if not os.path.exists(caminho):
        print(f"❌ Erro: Arquivo '{ARQUIVO_ANUNCIOS_ENTRADA}' não encontrado.")
        return []

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            data = json.load(f)
            anuncios = data.get("anuncios", [])
            
            # Coleta apenas URLs de perfil válidas e remove duplicatas
            urls_unicas = set()
            for anuncio in anuncios:
                url_p = anuncio.get("vendedor_url_perfil")
                if url_p:
                    urls_unicas.add(url_p)
            
            return list(urls_unicas)
    except Exception as e:
        print(f"❌ Erro ao ler perfis dos anúncios: {e}")
        return []


def processar_perfil_worker(args):
    idx, total, url_perfil = args
    uuid_p = extrair_uuid_da_url_perfil(url_perfil)

    # Verificação de Cache prévia
    diretorio = os.path.dirname(os.path.abspath(__file__))
    caminho_cache = os.path.join(diretorio, ".temp_perfis", uuid_p, "perfil_bruto.json")
    if os.path.exists(caminho_cache):
        try:
            with open(caminho_cache, "r", encoding="utf-8") as f:
                dados_existentes = json.load(f)
                return {"status": "CACHE", "url": url_perfil, "dados": dados_existentes}
        except Exception:
            pass

    try:
        dados = extrair_perfil_olx(url_perfil)
        return {"status": "SUCESSO", "url": url_perfil, "dados": dados}
    except Exception as e:
        return {"status": "ERRO", "url": url_perfil, "erro": str(e)}


def executar_pipeline_perfis(max_tentativas=400):
    print("=" * 60)
    print(" 🛡️ INICIANDO PIPELINE DE SCRAPING DE PERFIS (ANTI-GOLPE)")
    print("=" * 60)

    links_pendentes = carregar_links_perfis_unicos()
    if not links_pendentes:
        print("Nenhum perfil único encontrado para processar.")
        return

    total_origem = len(links_pendentes)
    print(f"📋 {total_origem} perfis únicos extraídos dos anúncios.")
    print(f"⚙️ Executando com {MAX_WORKERS} thread(s) simultânea(s)...\n")

    resultados_finais = {}
    inicio_total = time.time()

    for rodada in range(1, max_tentativas + 1):
        if not links_pendentes:
            break

        print(f"🔄 --- RODADA {rodada}/{max_tentativas} (Perfis pendentes: {len(links_pendentes)}) ---")
        tarefas = [(idx, len(links_pendentes), url) for idx, url in enumerate(links_pendentes, 1)]
        falhas_rodada = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(processar_perfil_worker, tarefa) for tarefa in tarefas]
            for future in as_completed(futures):
                res = future.result()
                if res["status"] in ["SUCESSO", "CACHE"]:
                    resultados_finais[res["url"]] = res["dados"]
                else:
                    falhas_rodada.append(res["url"])

        links_pendentes = falhas_rodada
        

    tempo_total = time.time() - inicio_total
    sucessos = list(resultados_finais.values())

    relatorio = {
        "total_perfis_origem": total_origem,
        "total_processados": len(sucessos),
        "falhas_finais": len(links_pendentes),
        "tempo_execucao_segundos": round(tempo_total, 2),
        "perfis": sucessos
    }

    caminho_saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), ARQUIVO_PERFIS_SAIDA)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(" RESUMO DA EXECUÇÃO DOS PERFIS:")
    print(f" -> Perfis extraídos com sucesso: {len(sucessos)} / {total_origem}")
    print(f" -> Falhas não resolvidas: {len(links_pendentes)}")
    print(f" -> Tempo total acumulado: {round(tempo_total, 2)}s")
    print(f" -> Relatório salvo em: {caminho_saida}")
    print("=" * 60)


if __name__ == "__main__":
    executar_pipeline_perfis()
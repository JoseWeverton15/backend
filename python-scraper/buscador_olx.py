import time
import re
import os
import json
import cloudscraper
from bs4 import BeautifulSoup

NOME_ARQUIVO_JSON_PADRAO = "links_encontrados.json"

def _executar_extracao(url_busca):
    links = []
    try:
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        response = scraper.get(url_busca, timeout=1)
        if response.status_code != 200:
            return links

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Método 1: JSON embutido (__NEXT_DATA__)
        script_json = soup.find("script", id="__NEXT_DATA__")
        if script_json and script_json.string:
            try:
                data = json.loads(script_json.string)
                page_props = data.get("props", {}).get("pageProps", {})
                ads_list = page_props.get("ads", []) or page_props.get("listProps", {}).get("ads", [])

                for ad in ads_list:
                    url_anuncio = ad.get("url") or ad.get("subjectUrl")
                    if url_anuncio and url_anuncio not in links:
                        links.append(url_anuncio)
                if links:
                    return links
            except Exception:
                pass

        # Método 2: Fallback HTML
        cards = soup.find_all("a", href=True)
        for card in cards:
            href = card["href"]
            if "olx.com.br" in href and re.search(r'-\d+(\?|$)', href):
                link_limpo = href.split("?")[0]
                if link_limpo not in links:
                    links.append(link_limpo)

        return links
    except Exception:
        return links

def extrair_links_pagina_busca(url_busca, max_tentativas=3):
    """
    Tenta extrair os links da busca repetidamente até atingir o limite de tentativas.
    """
    print(f"Buscando lista de anúncios em: {url_busca}")
    
    for tentativa in range(1, max_tentativas + 1):
        links = _executar_extracao(url_busca)
        if links:
            print(f"Sucesso na tentativa {tentativa}! Extraídos {len(links)} links.")
            return links
        
        if tentativa < max_tentativas:
            print(f"⚠️ Tentativa {tentativa} falhou ou retornou vazia. Tentando novamente em 2 segundos...")
            
            
    print("❌ Falha: Não foi possível extrair os links após todas as tentativas.")
    return []
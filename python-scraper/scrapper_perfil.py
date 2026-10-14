import json
import os
import random
import re
import time
import cloudscraper
from bs4 import BeautifulSoup  # <-- Adicionado para ler o Next.js

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"
]

# =============================================================================
# 1. GERENCIAMENTO DE CACHE DE PERFIS (Mantido igual)
# =============================================================================

def extrair_uuid_da_url_perfil(url_perfil: str) -> str:
    partes = url_perfil.rstrip("/").split("/")
    return partes[-1] if partes else "sem_id"

def obter_caminho_cache_perfil(uuid_perfil: str) -> str:
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(diretorio_script, ".temp_perfis", uuid_perfil, "perfil_bruto.json")

def ler_do_cache_perfil(uuid_perfil: str) -> dict | None:
    caminho = obter_caminho_cache_perfil(uuid_perfil)
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
                dados["_origem_cache"] = True
                return dados
        except Exception:
            return None
    return None

def salvar_no_cache_perfil(uuid_perfil: str, dados: dict) -> None:
    caminho = obter_caminho_cache_perfil(uuid_perfil)
    pasta = os.path.dirname(caminho)
    os.makedirs(pasta, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# =============================================================================
# 2. CLIENTE DE REDE E PARSER DO PERFIL (Atualizado)
# =============================================================================

def buscar_html_perfil(url: str, max_retries: int = 3) -> str:
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    
    for tentativa in range(1, max_retries + 1):
        try:
            scraper.headers.update({
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
            })
            response = scraper.get(url, timeout=1) # Sugestão: aumentei para 10s para evitar timeouts prematuros
            
            if response.status_code == 200:
                return response.text
            if response.status_code == 410:
                raise Exception("Perfil removido/inexistente (HTTP 410)")

            if tentativa == max_retries:
                raise Exception(f"Erro HTTP {response.status_code} após {max_retries} tentativas")
        except Exception as e:
            if tentativa == max_retries:
                raise e
          


def parse_dados_perfil(html: str) -> dict:
    """Extrai as métricas diretamente do JSON estruturado do Next.js (__NEXT_DATA__)."""
    metadados = {
        "nickname": "Desconhecido",
        "score_description": "N/A",
        "score_value": "N/A",
        "creation_date": "N/A",
        "is_new_account": None,
        "phone_verified": False,
        "email_verified": False,
        "facebook_verified": False,
        "facematch_profile_verified": False,
        "is_pro": False,
        "key_account": False
    }

    try:
        soup = BeautifulSoup(html, "html.parser")
        script_tag = soup.find("script", id="__NEXT_DATA__")
        
        if not script_tag:
            return metadados

        data = json.loads(script_tag.string)
        
        # O caminho exato onde a OLX guarda os dados do vendedor no Next.js:
        user_info = (
            data.get("props", {})
            .get("pageProps", {})
            .get("sellerProfileData", {})
        )
        
        if not user_info:
            return metadados
        
        metadados["nickname"] = user_info.get("nickname") or user_info.get("name") or "Desconhecido"
        metadados["creation_date"] = user_info.get("creationDate", "N/A")
        metadados["is_new_account"] = user_info.get("isNewAccount", False)
        metadados["is_pro"] = user_info.get("isPro", False)
        metadados["key_account"] = user_info.get("keyAccount", False)

        # Verificações de segurança
        metadados["phone_verified"] = user_info.get("phoneVerified", False)
        metadados["email_verified"] = user_info.get("emailVerified", False)
        metadados["facebook_verified"] = user_info.get("facebookVerified", False)

        facematch = user_info.get("facematch", {})
        if isinstance(facematch, dict):
            metadados["facematch_profile_verified"] = facematch.get("profileVerified", False)

        score = user_info.get("score", {})
        if isinstance(score, dict):
            metadados["score_description"] = score.get("description", "N/A")
            metadados["score_value"] = score.get("value", "N/A")

    except Exception:
        pass

    return metadados


def extrair_perfil_olx(url_perfil: str) -> dict:
    uuid_perfil = extrair_uuid_da_url_perfil(url_perfil)

    # 1. Leitura do Cache
    cached = ler_do_cache_perfil(uuid_perfil)
    if cached:
        return cached

    # 2. Scraping HTTP
    html = buscar_html_perfil(url_perfil)
    metricas = parse_dados_perfil(html)

    resultado = {
        "uuid_perfil": uuid_perfil,
        "url_perfil": url_perfil,
        **metricas,
        "_origem_cache": False
    }

    # 3. Gravação no Cache
    salvar_no_cache_perfil(uuid_perfil, resultado)
    return resultado
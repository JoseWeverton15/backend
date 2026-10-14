import json
import os
import random
import re
import time
import cloudscraper
from anunciante import extrair_url_perfil_anunciante

# =============================================================================
# LISTA DE USER-AGENTS REAIS PARA ROTAÇÃO DERAIS
# =============================================================================
USER_AGENTS = [
    # Chrome WindowsAC
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    # Firefox Windows/Linux
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    # Edge Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    # Safari macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    # Chrome macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]

# =============================================================================
# 1. GERENCIAMENTO DE CACHE E UTILITÁRIOS
# =============================================================================

def extrair_id_da_url(url: str) -> str:
    """Extrai o ID numérico do anúncio presente na URL."""
    match = re.search(r"-(\d+)(\?|$)", url)
    return match.group(1) if match else "sem_id"


def obter_caminho_cache(id_anuncio: str) -> str:
    """Retorna o caminho absoluto do arquivo de cache para um anúncio."""
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(diretorio_script, ".temp", id_anuncio, "dados_brutos.json")


def ler_do_cache(id_anuncio: str) -> dict | None:
    """Lê os dados salvos em disco caso o cache exista."""
    caminho_cache = obter_caminho_cache(id_anuncio)
    if os.path.exists(caminho_cache):
        try:
            with open(caminho_cache, "r", encoding="utf-8") as f:
                dados = json.load(f)
                dados["_origem_cache"] = True  # Flag indicando reaproveitamento
                return dados
        except Exception:
            return None
    return None


def salvar_no_cache(id_anuncio: str, dados_anuncio: dict) -> None:
    """Salva os dados brutos do anúncio no diretório .temp/{id_anuncio}."""
    caminho_cache = obter_caminho_cache(id_anuncio)
    pasta_anuncio = os.path.dirname(caminho_cache)
    
    os.makedirs(pasta_anuncio, exist_ok=True)
    with open(caminho_cache, "w", encoding="utf-8") as f:
        json.dump(dados_anuncio, f, ensure_ascii=False, indent=2)


def formatar_preco(preco_num: float) -> str:
    """Converte o valor numérico em string formatada em Moeda (BRL)."""
    if preco_num <= 0:
        return "N/A"
    return f"R$ {preco_num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# =============================================================================
# 2. CLIENTE DE REDE COM ROTAÇÃO DE HEADERS E PARSERS
# =============================================================================

def buscar_html_anuncio(url: str, max_retries: int = 3) -> str:
    """
    Realiza a requisição HTTP aplicando Rotação de User-Agent e retentativas em erro != 200.
    """
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    for tentativa in range(1, max_retries + 1):
        try:
            # Sorteia um User-Agent dinâmico a cada tentativa
            ua_sorteado = random.choice(USER_AGENTS)
            scraper.headers.update({
                "User-Agent": ua_sorteado,
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            })

            response = scraper.get(url, timeout=1)
            
            if response.status_code == 200:
                return response.text
            
            # Se for 410 (Anúncio deletado), encerra retentativa
            if response.status_code == 410:
                raise Exception("Anúncio removido/expirado (HTTP 410)")

            # Se for 403 ou 5xx, aguarda backoff progressivo
            if tentativa < max_retries:
                tempo_espera = tentativa * 1.5
                
            else:
                raise Exception(f"Erro HTTP {response.status_code} após {max_retries} tentativas")
                
        except Exception as e:
            if tentativa == max_retries:
                raise e
            


def parse_json_ld(html: str) -> dict:
    """Extrai metadados estruturados (schema.org) contidos na tag script ld+json."""
    dados = {"titulo": None, "preco": 0.0, "descricao": None, "fotos": []}
    
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    if not match:
        return dados

    try:
        ld_data = json.loads(match.group(1))
        offer = ld_data.get("makesOffer", {})
        item = offer.get("itemOffered", {}) if offer else ld_data

        dados["titulo"] = item.get("name") or ld_data.get("name")

        raw_price = (
            offer.get("priceSpecification", {}).get("price") 
            or offer.get("price") 
            or ld_data.get("offers", {}).get("price")
        )
        if raw_price:
            dados["preco"] = float(raw_price)

        raw_desc = item.get("description") or ld_data.get("description")
        if raw_desc:
            dados["descricao"] = (
                raw_desc.replace("<br>", "\n")
                        .replace("<br/>", "\n")
                        .replace("<br />", "\n")
            )

        raw_images = item.get("image") or ld_data.get("image") or []
        if isinstance(raw_images, list):
            for img in raw_images:
                if isinstance(img, dict) and img.get("contentUrl"):
                    dados["fotos"].append(img.get("contentUrl"))
                elif isinstance(img, str):
                    dados["fotos"].append(img)
        elif isinstance(raw_images, str):
            dados["fotos"].append(raw_images)

    except Exception:
        pass

    return dados


def parse_data_layer(html: str) -> dict:
    """Extrai metadados técnicos e ficha técnica do window.dataLayer."""
    dados = {"id_anuncio": None, "titulo": None, "preco": 0.0, "detalhes": {}, "fotos": []}

    match = re.search(r'window\.dataLayer\s*=\s*(\[\{.*?\}\])\s*</script>', html, re.DOTALL)
    if not match:
        match = re.search(r'window\.dataLayer\s*=\s*(\[\{.*?\}\])', html, re.DOTALL)

    if not match:
        return dados

    try:
        raw_json = match.group(1)
        data = json.loads(raw_json)
        
        page_data = data[0].get("page", {})
        ad_detail = page_data.get("adDetail", {})
        ad_properties = page_data.get("adProperties", [])

        if ad_detail.get("listId"):
            dados["id_anuncio"] = str(ad_detail.get("listId"))

        if ad_detail.get("subject"):
            dados["titulo"] = ad_detail.get("subject")

        price_val = ad_detail.get("price") or page_data.get("detail", {}).get("price")
        if price_val:
            dados["preco"] = float(price_val)

        for p in ad_properties:
            if isinstance(p, dict) and p.get("label"):
                dados["detalhes"][p.get("label")] = p.get("value")

        if "images" in ad_detail and isinstance(ad_detail["images"], list):
            for img in ad_detail["images"]:
                if isinstance(img, dict) and img.get("original"):
                    dados["fotos"].append(img.get("original"))

    except Exception:
        pass

    return dados


def extrair_fotos_fallback_regex(html: str) -> list:
    """Busca URLs de imagens da OLX diretamente no HTML bruto via Regex."""
    return re.findall(r'https://img\.olx\.com\.br/images/\d+/\d+\.(?:jpg|webp|jpeg)', html)


# =============================================================================
# 3. ORQUESTRADOR PRINCIPAL COM CACHE
# =============================================================================

def extrair_anuncio_olx(url_anuncio: str) -> dict:
    """
    Função orquestradora:
    1. Verifica se já existe cache em disco (.temp/[ID]).
    2. Caso não exista, baixa o HTML e extrai os dados.
    3. Grava o resultado no cache e retorna.
    """
    id_temp = extrair_id_da_url(url_anuncio)

    # --- Passagem 1: Leitura do Cache ---
    dados_cached = ler_do_cache(id_temp)
    if dados_cached:
        return dados_cached

    # --- Passagem 2: Web Scraping ---
    html = buscar_html_anuncio(url_anuncio)
    
    dados_ld = parse_json_ld(html)
    dados_dl = parse_data_layer(html)
    
    id_anuncio = dados_dl["id_anuncio"] or id_temp
    titulo = dados_ld["titulo"] or dados_dl["titulo"] or "Título não encontrado"
    preco_num = dados_ld["preco"] if dados_ld["preco"] > 0 else dados_dl["preco"]
    descricao = dados_ld["descricao"] or "Descrição não encontrada"
    
    fotos_set = set(dados_ld["fotos"] + dados_dl["fotos"])
    if len(fotos_set) <= 1:
        fotos_set.update(extrair_fotos_fallback_regex(html))

    dados_perfil = extrair_url_perfil_anunciante(html)

    resultado = {
        "id_anuncio": id_anuncio,
        "url": url_anuncio,
        "titulo": titulo,
        "preco_bruto": formatar_preco(preco_num),
        "preco_numerico": preco_num,
        "vendedor_nome": dados_perfil["seller_name"],
        "vendedor_url_perfil": dados_perfil["url_perfil"],
        "descricao": descricao,
        "detalhes": dados_dl["detalhes"],
        "fotos_urls_originais": list(fotos_set)
    }

    # --- Passagem 3: Gravação do Cache ---
    salvar_no_cache(id_anuncio, resultado)
    
    return resultado
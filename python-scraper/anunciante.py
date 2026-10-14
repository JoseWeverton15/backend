import json
import re
import unicodedata

def normalizar_nome_para_slug(nome: str) -> str:
    """
    Mantido por compatibilidade caso queira exibir o nome amigável,
    mas não é mais obrigatório para a montagem da URL de perfil.
    """
    if not nome:
        return ""
    
    nome_sem_acentos = unicodedata.normalize('NFD', nome)
    nome_ascii = ''.join(c for c in nome_sem_acentos if unicodedata.category(c) != 'Mn')
    slug = nome_ascii.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    
    return slug


def extrair_url_perfil_anunciante(html: str) -> dict:
    """
    Extrai o sellerName e sellerPublicAccountId do dataLayer no HTML 
    e constrói o link público direto do perfil do anunciante usando o UUID completo.
    """
    dados_perfil = {
        "seller_name": None,
        "seller_public_account_id": None,
        "url_perfil": None
    }

    # Busca a estrutura do window.dataLayer no HTML
    match = re.search(r'window\.dataLayer\s*=\s*(\[\{.*?\}\])\s*</script>', html, re.DOTALL)
    if not match:
        match = re.search(r'window\.dataLayer\s*=\s*(\[\{.*?\}\])', html, re.DOTALL)

    if not match:
        return dados_perfil

    try:
        raw_json = match.group(1)
        data = json.loads(raw_json)
        
        page_data = data[0].get("page", {})
        ad_detail = page_data.get("adDetail", {})

        seller_name = ad_detail.get("sellerName")
        public_account_id = ad_detail.get("sellerPublicAccountId")

        dados_perfil["seller_name"] = seller_name
        dados_perfil["seller_public_account_id"] = public_account_id

        if public_account_id:
            # URL direta utilizando o UUID completo da conta do anunciante
            dados_perfil["url_perfil"] = f"https://www.olx.com.br/perfil/{public_account_id}"

    except Exception as e:
        print(f"⚠️ Erro ao gerar link do perfil: {e}")

    return dados_perfil


# =============================================================================
# TESTE ISOLADO COM O TRECHO FORNECIDO
# =============================================================================
if __name__ == "__main__":
    # HTML simulado contendo o dataLayer com os dados que você enviou
    html_exemplo = """
    <script>
    window.dataLayer = [{"page":{"pageType":"ad_detail","adDetail":{"adId":1816565165,"listId":1542567216,"sellerName":"Moacyr Maynard","sellerPublicAccountId":"f169bad7-9e03-4597-864b-b6c0a24cebb7"}}}]</script>
    """

    resultado = extrair_url_perfil_anunciante(html_exemplo)
    
    print("\n" + "="*60)
    print("🔍 EXTRAÇÃO DA URL DIRETA DO PERFIL DO ANUNCIANTE")
    print("="*60)
    print(f"👤 Nome do Vendedor:    {resultado['seller_name']}")
    print(f"🆔 UUID da Conta:     {resultado['seller_public_account_id']}")
    print(f"🔗 Link do Perfil:    {resultado['url_perfil']}")
    print("="*60)
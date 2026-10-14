package br.com.flipfacil.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.util.List;
import java.util.Map;

@Data
public class ScraperResponse {
    private String id_anuncio;
    private String url;
    private String titulo;
    private String preco_bruto;
    private Double preco_numerico;  
    private String vendedor_nome;
    private String vendedor_url_perfil;
    private String descricao;
    private Map<String, String> detalhes;

    @JsonProperty("fotos_urls_originais")
    private List<String> fotos_urls_originais;
}
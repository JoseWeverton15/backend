package br.com.flipfacil.dto;

import lombok.Data;

import java.util.List;
import java.util.Map;

@Data
public class ScraperResponse {
    private String titulo;
    private String preco_bruto;
    private Double preco_numerico;  
    private String descricao;
    private Map<String, String> detalhes;
    private List<String> fotos;
    private String url;
}
package br.com.flipfacil.dto;

import lombok.Data;
import java.util.List;

@Data
public class ScraperPaginaResponse {
    private String url_busca;
    private Integer total_links;
    private List<String> links;
}
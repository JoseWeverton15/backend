package br.com.flipfacil.dto;

import lombok.Data;
import java.util.List;

@Data
public class ScraperLoteResponse {
    private Integer total_links_origem;
    private Integer total_processados;
    private Integer falhas_finais;
    private Double tempo_execucao_segundos;
    private List<ScraperResponse> anuncios;
}
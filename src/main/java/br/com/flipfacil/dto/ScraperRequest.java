package br.com.flipfacil.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class ScraperRequest {
    @NotBlank(message = "O campo url_busca não pode estar vazio")
    private String url_busca;
}
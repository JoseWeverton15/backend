package br.com.flipfacil.dto;

import lombok.Getter;
import lombok.Setter;

import jakarta.validation.constraints.NotBlank;

@Getter
@Setter
public class ScraperPaginaRequest {
    @NotBlank(message = "O campo url_pagina não pode estar vazio")
    private String url_pagina;
}
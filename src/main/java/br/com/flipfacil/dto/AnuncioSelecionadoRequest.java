package br.com.flipfacil.dto;

import jakarta.validation.constraints.NotBlank;

import lombok.Data;

@Data
public class AnuncioSelecionadoRequest {
    @NotBlank 
    private String titulo;

    @NotBlank 
    private String preco;

    @NotBlank
    private String url;
}

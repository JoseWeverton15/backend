package br.com.flipfacil.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter 
public class FiltroAnuncioRequest {
    private String titulo;
    private String descricao;
    private Double precoMinimo;
    private Double precoMaximo;
    private String categoria;
    private String cidade;
    private String estado;

    public FiltroAnuncioRequest() {
    }
}

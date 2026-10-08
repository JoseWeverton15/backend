package br.com.flipfacil.service;

import org.springframework.stereotype.Service;
import org.springframework.cache.annotation.Cacheable;

import br.com.flipfacil.dto.AnuncioSelecionadoRequest;

@Service
public class AnaliseService {

    @Cacheable(
        value = "analises",
        key = "#anuncioSelecionadoRequest.url.concat('|').concat(#anuncioSelecionadoRequest.titulo).concat('|').concat(#anuncioSelecionadoRequest.preco)"
    )
    public AnuncioSelecionadoRequest analisar(AnuncioSelecionadoRequest anuncioSelecionadoRequest) {
        return anuncioSelecionadoRequest;
    }
}
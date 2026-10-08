package br.com.flipfacil.service;

import org.springframework.stereotype.Service;

import br.com.flipfacil.dto.AnuncioSelecionadoRequest;

@Service 
public class AnaliseService {
    public AnuncioSelecionadoRequest analisar(AnuncioSelecionadoRequest anuncioSelecionadoRequest) {
        return anuncioSelecionadoRequest;
    }
}
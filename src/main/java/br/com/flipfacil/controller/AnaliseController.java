package br.com.flipfacil.controller;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import br.com.flipfacil.dto.AnuncioSelecionadoRequest;
import br.com.flipfacil.service.AnaliseService;
import jakarta.validation.Valid;

import org.springframework.web.bind.annotation.RequestBody;

@RestController 
@RequestMapping("/api/analise")
public class AnaliseController {
    private final AnaliseService analiseService;
    
    public AnaliseController(AnaliseService analiseService) {
        this.analiseService = analiseService;
    }

    @PostMapping 
    public AnuncioSelecionadoRequest analisar(@Valid @RequestBody AnuncioSelecionadoRequest anuncioSelecionadoRequest) {
        return analiseService.analisar(anuncioSelecionadoRequest);
    }
}
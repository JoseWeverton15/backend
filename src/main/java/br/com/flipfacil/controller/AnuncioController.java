package br.com.flipfacil.controller;

import java.util.List;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.flipfacil.dto.FiltroAnuncioRequest;
import br.com.flipfacil.service.AnuncioService;
import br.com.flipfacil.entity.Anuncio;

@RestController 
@RequestMapping("/api/anuncios")
public class AnuncioController {
    private final AnuncioService anuncioService;

    public AnuncioController(AnuncioService anuncioService) {
        this.anuncioService = anuncioService;
    }
    @PostMapping ("/filtrar")
    public List<Anuncio> listarAnuncios(@RequestBody FiltroAnuncioRequest filtro) {
        return anuncioService.filtrarAnuncios(filtro);
    }
}

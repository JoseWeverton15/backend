package br.com.flipfacil.controller;

import org.springframework.web.bind.annotation.RestController;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import br.com.flipfacil.service.ScraperService;
import br.com.flipfacil.dto.ScraperRequest;
import br.com.flipfacil.dto.ScraperResponse;

import br.com.flipfacil.dto.ScraperPaginaRequest;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/scraper")
public class ScraperController{
    private final ScraperService scraperService;
    
    public ScraperController(ScraperService scraperService) {
        this.scraperService = scraperService;
    }

    @PostMapping("/anuncio") 
    public ScraperResponse scraperAnuncio(@Valid @RequestBody ScraperRequest scraperRequest){
        return scraperService.extrairAnuncio(scraperRequest);
    }

    @PostMapping("/getItems") 
    public ScraperResponse scraperPagina(@Valid @RequestBody ScraperPaginaRequest scraperRequest){
        return scraperService.extrairPagina(scraperRequest);
    }

}
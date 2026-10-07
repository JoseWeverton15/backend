package br.com.flipfacil.controller;


import org.springframework.web.bind.annotation.RestController;


import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import br.com.flipfacil.service.ScraperService;
import br.com.flipfacil.dto.ScraperRequest;
import br.com.flipfacil.dto.ScraperResponse;

@RestController
@RequestMapping("/api/scraper")
public class ScraperController{
    private final ScraperService scraperService;
    
    public ScraperController(ScraperService scraperService) {
        this.scraperService = scraperService;
    }

    @PostMapping("/anuncio") 
    public ScraperResponse scraper(@RequestBody ScraperRequest scraperRequest){
        return scraperService.extrairAnuncio(scraperRequest);
    }

}
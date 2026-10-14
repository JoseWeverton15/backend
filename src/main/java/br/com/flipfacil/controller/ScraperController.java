package br.com.flipfacil.controller;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import br.com.flipfacil.service.ScraperService;
import br.com.flipfacil.dto.ScraperRequest;
import br.com.flipfacil.dto.ScraperResponse;
import br.com.flipfacil.dto.ScraperPaginaRequest;
import br.com.flipfacil.dto.ScraperPaginaResponse;
import br.com.flipfacil.dto.ScraperLoteRequest;
import br.com.flipfacil.dto.ScraperLoteResponse;

import jakarta.validation.Valid;

import java.util.concurrent.CompletableFuture;

@RestController
@RequestMapping("/api/scraper")
public class ScraperController {

    private final ScraperService scraperService;
    
    public ScraperController(ScraperService scraperService) {
        this.scraperService = scraperService;
    }

    //Extração unitária de um anúncio específico
    @PostMapping("/anuncio") 
    public ScraperResponse scraperAnuncio(@Valid @RequestBody ScraperRequest scraperRequest) {
        return scraperService.extrairAnuncio(scraperRequest);
    }

    // Busca a lista de links da página de listagem da OLX
    @PostMapping("/getItems") 
    public CompletableFuture<ScraperPaginaResponse> scraperPagina(@Valid @RequestBody ScraperPaginaRequest scraperRequest) {
        return scraperService.buscarLinksPagina(scraperRequest);
    }

    //Recebe a lista de links selecionados e extrai o lote bruto completo
    @PostMapping("/extrair-lote")
    public CompletableFuture<ScraperLoteResponse> extrairLote(@Valid @RequestBody ScraperLoteRequest loteRequest) {
        return scraperService.extrairLoteAnuncios(loteRequest);
    }
}
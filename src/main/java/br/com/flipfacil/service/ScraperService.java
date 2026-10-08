package br.com.flipfacil.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import br.com.flipfacil.dto.ScraperRequest;
import br.com.flipfacil.dto.ScraperResponse;

import br.com.flipfacil.dto.ScraperPaginaRequest;
import br.com.flipfacil.exception.ScraperException;

import org.springframework.scheduling.annotation.Async;
import java.util.concurrent.CompletableFuture;

@Service
public class ScraperService {
    private final RestClient restClient;
    public ScraperService() {
        this.restClient = RestClient
                .builder()
                .baseUrl("http://localhost:5001")
                .build();
    }
    public ScraperResponse extrairAnuncio(ScraperRequest request) {
        try {
            return restClient
                    .post()
                    .uri("/scrape/anuncio")
                    .body(request)
                    .retrieve()
                    .body(ScraperResponse.class);
        } catch (Exception e) {
            throw new ScraperException("Erro ao extrair anúncio: " + e.getMessage(), e);
        }
    }
    
    @Async("taskExecutor")
    public CompletableFuture<ScraperResponse> extrairPagina(ScraperPaginaRequest request) {
        try {
            return CompletableFuture.completedFuture(restClient
                    .post()
                    .uri("/scrape/getItems")
                    .body(request)
                    .retrieve()
                    .body(ScraperResponse.class));
        } catch (Exception e) {
            throw new ScraperException("Erro ao extrair página: " + e.getMessage(), e);
        }
    }
}
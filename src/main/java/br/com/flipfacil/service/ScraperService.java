package br.com.flipfacil.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import br.com.flipfacil.dto.ScraperRequest;
import br.com.flipfacil.dto.ScraperResponse;

import br.com.flipfacil.exception.ScraperException;

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
}
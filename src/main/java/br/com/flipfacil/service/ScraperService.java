package br.com.flipfacil.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import br.com.flipfacil.dto.ScraperRequest;
import br.com.flipfacil.dto.ScraperResponse;

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
        return restClient
                .post()
                .uri("/scrape/anuncio")
                .body(request)
                .retrieve()
                .body(ScraperResponse.class);
    }
}